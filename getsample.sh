#!/bin/bash

#PBS -q hep
#PBS -l nodes=1:ppn=1,mem=8gb
#PBS -l walltime=02:00:00
#PBS -o pbslogs/$PBS_JOBNAME.o.$@
#PBS -j oe

# Prepare environment
cd $PBS_O_WORKDIR/download
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet
lsetup rucio

# Check sample exists 
NfilesGrid=$(rucio list-files $@ |& grep "\.MxAOD\.root" | wc -l)
if [ "$NfilesGrid" -eq "0" ]; then
  echo "ERROR! MxAOD $@ does not exist on grid! Check name or grid status!"
  return 1
fi

#Download sample to directory
outputDir='/group/atlas/data/jgv7/mxoad_hgamma/h014test'
cmd="rucio get --ndownloader 3 $@ --dir $outputDir"
echo $cmd
$cmd

# Check that all files were downloaded?
files=$(echo $outputDir/$@/*)
Nfiles=$(echo $files | awk '{print NF}')
echo $NfilesGrid $Nfiles
ls $outputDir/$@ 
if [ ! "$Nfiles" -eq "$NfilesGrid" ]; then
  echo "ERROR! Dataset $@ did not download all files! Files on Grid: $NfilesGrid, Files locally: $Nfiles!"
  return 1
fi

# If all files are downloaded, merge sample
echo $files

# Transfer merged sample to eos
