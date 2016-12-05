#!/bin/bash

#PBS -q hep
#PBS -l nodes=1:ppn=3,mem=4gb
#PBS -l walltime=06:00:00
#PBS -o pbslogs/$PBS_JOBNAME.o${PBS_JOBID}
#PBS -j oe


nCPU=2

# Set your output directory
downloadDir='/group/atlas/data/jgv7/mxoad_hgamma/h014'

if [ ! -d "$downloadDir" ]; then
  echo 'specified download directory $downloadDir does not exist! Please create/change.'
  return 1
fi



# Prepare environment
cd $PBS_O_WORKDIR
cd download
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet
rcSetup -q
lsetup rucio



# Check sample exists 
dsName=$1
echo -e "\nChecking that sample $dsName exists..."
NfilesGrid=$(rucio list-files $dsName |& grep "\.MxAOD\.root" | wc -l)
if [ "$NfilesGrid" -eq "0" ]; then
  echo "ERROR! MxAOD $dsName does not exist on grid! Check name or grid status!"
  return 1
fi
echo -e "\t\t SUCCESS! Download will now start.\n"



#Download sample to directory
cmd="rucio get --ndownloader $nCPU $dsName --dir $downloadDir"
echo $cmd
$cmd



# Check that directory exists
if [[ ! -d "$downloadDir/$dsName" ]]; then
  echo "Dataset directory does not exist! $downloadDir/$dsName not found"
  return 1
fi



# Check that all files were downloaded?
echo -e "\nChecking that all files were downloaded..."
files=$(echo $downloadDir/$dsName/*)
Nfiles=$(echo $files | awk '{print NF}')
ls $downloadDir/$dsName 
if [ ! "$Nfiles" -eq "$NfilesGrid" ]; then
  echo "ERROR! Dataset $dsName did not download all files! Files on Grid: $NfilesGrid, Files locally: $Nfiles!"
  return 1
fi
echo -e "\t\t SUCCESS!\n"
chgrp -hR hep $downloadDir/*



# If all files are downloaded, merge sample
sampleName="${dsName/group.phys-higgs./}"
sampleName="${sampleName/_MxAOD.root/.root}"

mergeMxAOD() {
  cmd="xAODMerge $downloadDir/$sampleName $files"
  echo $cmd
  if $cmd; then
    echo -e "\t\t xAODMerge SUCCESS!\n"
  else
    echo -e "\t\t AODMerge failed: Safe Merging... get comfortable, this takes some time.\n"
    cmd2="./SafeMerge.sh $downloadDir/$dsName"
    echo $cmd2
    $cmd2
  fi
}


mergeMC() {
  if [[ "$Nfiles" -gt "1" ]]; then
    if [[ "$dsName" =~ "MxAODAllSys" || "$dsName" =~ "PhotonSys" \
       || "$dsName" =~ "JetSys" || "$dsName" =~ "2DP20_100-165_3jets" ]]; then
      
      outputDS_size=$(du -s $downloadDir/$dsName/ | awk '{print $1}')
      if [[ "$outputDS_size" -le 7000000 ]]; then # 7GB sounds like a reasonable single file size?
        mergeMxAOD || return 1
        echo "Output file: $downloadDir/$sampleName"
      else
        i=$(( 1 ))
        echo "Large (> 7 GB) AllSys/PhotonSys/JetSys/MxAOD file detected! Will only rename files"
        mkdir $downloadDir/$sampleName
        for f in $files; do
          inputNo=$(printf "%03d" $i)
          AllSysDSname=${sampleName%.root}.${inputNo}.root
          cp $f $downloadDir/$sampleName/${AllSysDSname}
          i=$(( $i + 1 ))
        done
        echo "Output folder: $downloadDir/$sampleName"
      fi
    else
      mergeMxAOD || return 1
      echo "Output file: $downloadDir/$sampleName"
    fi
  elif [[ "$Nfiles" -eq "1" ]]; then
    # no need to merge if it's 1 file
    echo "Only one file, no need to merge. Will rename file"
    cp $downloadDir/$dsName/* ${downloadDir}/$sampleName
    echo "Output file: $downloadDir/$sampleName"
  else
    echo "Number of files = 0? check if MxAOD $sampleName downloaded correctly"
  fi
}


if [[ $sampleName =~ 'group.phys-higgs.data*' ]]; then
  if [[ "$Nfiles" -eq "1" ]]; then
    # no need to merge if it's 1 file
    echo "Only one file, no need to merge. Will rename file"
    cp $downloadDir/$dsName/* ${downloadDir}/$sampleName
  else
    mergeMxAOD
  fi
else 
  mergeMC
fi


# Transfer merged sample to eos
cd ../
kinit jvasquez@CERN.CH -l 5d -k -t jvasquez.keytab
klist
echo ''

if klist -s; then
  if [[ -n "klist | grep CERN.CH" ]]; then 
    echo "Found valid CERN kerberos ticket."
    python sendtoEOS.py $downloadDir/$sampleName
  fi
else
  echo "No valid kerberos ticket. Can not transfer to EOS."
  return 1
fi
chgrp -hR hep $downloadDir/*


echo "Finished."


