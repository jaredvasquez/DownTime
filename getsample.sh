#!/bin/bash

#PBS -q hep
#PBS -l nodes=1:ppn=4,mem=8gb
#PBS -l walltime=02:00:00
#PBS -o pbslogs/$PBS_JOBNAME.o${PBS_JOBID}
#PBS -j oe


# Set your output directory
downloadDir='/group/atlas/data/jgv7/mxoad_hgamma/h014test'

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
cmd="rucio get --ndownloader 3 $dsName --dir $downloadDir"
echo $cmd
$cmd


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


# If all files are downloaded, merge sample
sampleName="${dsName/group.phys-higgs./}"
sampleName="${sampleName/_MxAOD.root/.root}"
if [[ $sampleName =~ 'group.phys-higgs.data*' ]]; then
  echo "Sample is data, will not merge."
  return 1
else 
  cmd="xAODMerge $downloadDir/$sampleName $files"
  echo $cmd
  if $cmd; then
    echo -e "\t\t xAODMerge SUCCESS!\n"
  else
    echo -e "\t\t xAODMerge failed: Safe Merging... get comfortable, this takes some time.\n"
    cmd2="./SafeMerge.sh $downloadDir/$dsName"
    echo $cmd2
    $cmd2
  fi
fi

# Transfer merged sample to eos

cd ../
