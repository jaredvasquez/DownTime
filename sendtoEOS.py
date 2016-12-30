import os, sys, commands, fnmatch
from ROOT import *

def transferFile(input, output):
  cmd = 'xrdcp %s %s' % (input, output)
  print cmd
  status = commands.getstatusoutput(cmd)
  if (status[0] == 0): print "Transfer Successful"
  else:
    print "Transfer Failed";
    if (status[0] == 13824):
      print "File already exists on eos. Must delete before transfering."
    else:
      print status


inputPATH = sys.argv[1]
sampleName = inputPATH.split('/')[-1]

htag = 'h014'
EOSdir = 'root://eosatlas.cern.ch//eos/atlas/atlascerngroupdisk/phys-higgs/HSG1/MxAOD/%s_stageJV' % htag
EOSdir = 'root://eosatlas.cern.ch//eos/atlas/user/j/jvasquez/public/MxAOD/%s_stageJV' % htag
#if ( htag == '' ):
#  EOSdir='root://eosatlas.cern.ch//eos/atlas/atlascerngroupdisk/phys-higgs/HSG1/MxAOD/%s_stage' % htag

isdata = fnmatch.fnmatch(sampleName, 'data1[0-9]_13TeV.*')
#if (isdata): print "Does not currently support data."; sys.exit()
#htag = sampleName.split('.')[-2].replace('_MxAOD','')
#print htag

subdir  = '/mc_25ns'
subdirs = {
  'MxAODAllSys' : '/AllSys',
  'PhotonSys'   : '/PhotonSys',
  'Detailed'    : '/Detailed',
  'JetSysCorr1' : '/JetSysCorr1',
  'JetSysCorr1' : '/JetSysCorr2',
  'JetSysCorr3' : '/JetSysCorr3',
  'JetSysCorr4' : '/JetSysCorr4',
  '_50ns'       : '/mc_50ns'
}

for key in subdirs:
  if key in sampleName:
    subdir = subdirs[key]
    break

if isdata:
  subdir = '/data_25ns/runs'
  if '_50ns' in sampleName:
    subdir = '/data_50ns/runs'

subPATH = subdir+'/'+sampleName
eosPATH = EOSdir+subPATH

print "Transfering sample to eos:"
print "  %s" % subPATH

if os.path.isfile(inputPATH):
  # Transfer merged file
  transferFile( inputPATH, eosPATH )

elif os.path.isdir(inputPATH):
  # Transfer directory
  print "Transfering directory", inputPATH
  sampleFiles = [f for f in os.listdir(inputPATH) if os.path.isfile(os.path.join(inputPATH,f))]
  for file in sampleFiles:
    print " -->", file
    transferFile( inputPATH+"/"+file, eosPATH+"/"+file )

else:
  print "ERROR: InputPath is not file or directory"
  print "InputPath: ", inputPATH

print ""
