import sys, commands
from ROOT import *

inputPATH ='/group/atlas/data/jgv7/mxoad_hgamma/h014test/mc15c.MGPy8_tHjb125_yt_plus1.MxAOD.p2815.h014pre2_jvasquez.root'
sampleName = inputPATH.split('/')[-1]

htag = 'h014test'
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
print "  %s" % subdir

status = commands.getstatusoutput('xrdcp %s %s' % (inputPATH, eosPATH))
if (status[0] == 0): print "Transfer Successful"
else:                print "Transfer Failed"
