import os, sys, commands
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

htag = 'h014pre2'
EOSdir = 'root://eosatlas.cern.ch//eos/atlas/atlascerngroupdisk/phys-higgs/HSG1/MxAOD/%s_stage' % htag
if ( htag == '' ):
  EOSdir='root://eosatlas.cern.ch//eos/atlas/atlascerngroupdisk/phys-higgs/HSG1/MxAOD/%s_stage' % htag

isdata = 'data' in sampleName.split('.')[2]
if (isdata):
  print "Does not currently support data."
  sys.exit()

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
subPATH = subdir+'/'+sampleName
eosPATH = EOSdir+subPATH

print "Transfering sample to eos:"
print "  %s" % subPATH

if os.path.isfile(inputPATH):
  # Transfer merged file
  transferFile( inputPATH, eosPATH )
  """
  cmd = 'xrdcp %s %s' % (inputPATH, eosPATH)
  print cmd
  status = commands.getstatusoutput(cmd)
  if (status[0] == 0): print "Transfer Successful"
  else:
    print "Transfer Failed";
    if (status[0] == 13824):
      print "File already exists on eos. Must delete before transfering."
    else:
      print status
  """

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

"""
  if [[ "$isFolder" == "false"  ]]; then
    xrdcp $downloadDir/$newDSname $EOSdir/$newDSname
    #echo "xrdcp $downloadDir/$newDSname $EOSdir/$newDSname"
  else
    files=$(echo $downloadDir/$newDSname/*)
    i=$(( 1 ))
    for f in $files; do
        inputNo=$(printf "%03d" $i)
        SysDSname=${newDSname%.root}.${inputNo}.root
        xrdcp $f $EOSdir/$newDSname/${SysDSname}
        #echo "xrdcp $f $EOSdirAllSys/$newDSname/${AllSysDSname}"
        i=$(( $i + 1 ))
    done
  fi
"""
