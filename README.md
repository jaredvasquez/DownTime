# Automated Downloading for MxAODs 
This package has some scripts for monitoring MxAOD production jobs and then, when finished, submitting batch jobs to download the needed samples. 

## Installation
The scripts require [pandamonium](https://github.com/dguest/pandamonium) to be installed as well as a directory with AnalysisRelease setup for you. This will all be setup for you by simply running the command:
```
source installReqs.sh 
```
The install script will also append a job to your crontab file, which will be ran once every minute.

## User Configuration
Within the `runCron.sh` file, there are two parameters to configure:
```
export GRID_USER_NAME="Jared Vasquez"
export PANDASTR='group.phys-higgs*h014pre2'
```

The `PANDASTR` variable specifies the search criteria for monitoring. You can limit your search to a specific user by setting the `GRID_USER_NAME` variable, which should reflect your name as appears on bigpanda. You can also comment out this variable to search for jobs from all users. 

Within the `getsample.sh` file, you should set the output path for downloaded samples.
```
outputDir='/PATH/TO/DIR'
```

## Running
Currently, these scripts are engineered to use a Torque batch system to schedule jobs for download and merge the results. In a future update, samples will also be transfered to eos automatically.

For the batch jobs to work properly, it is important they have access to your voms proxy session. 
To pass your proxy session to the batch system, make sure your `.bash.rc` file sets an environment variable similar to:
```
export X509_USER_PROXY=$HOME/.globus/proxy
```

Since jobs usually take longer than the standard 12 hour proxy session, it is recommend you extend the validity of your proxy to the maximimum (4 days). A valid proxy session needs to be configured before the cronjobs will begin your downloads.
```
setupATLAS -q
lsetup rucio -q
voms-proxy-init -voms atlas -valid 96:00
```

