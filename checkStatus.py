import os, sys, pickle, time, datetime, commands

__downloadDB = 'logdls.pkl'

def fatal(error): print 'FATAL ERROR: %s' % error; sys.exit()

# Check for string in environment variables
PANDASTRs = [
    'group.phys-higgs.*mc15*h014*_*cjmeyer',
    'group.phys-higgs.*mc15*h014*_*jvasquez',
    'group.phys-higgs.*mc15*h014*_*zhangyu',
    'group.phys-higgs.*data*13TeV*h014*_*cjmeyer',
    'group.phys-higgs.*data*13TeV*h014*_*jvasquez',
    'group.phys-higgs.*data*13TeV*h014*_*zhangyu',
    'group.phys-higgs.*mc15*h014b_*JV',
    'group.phys-higgs.*mc15*h014_JGV',
]
if len(PANDASTRs) < 1: fatal('Must specify search strings PANDASTRs')

# Use pandamonium to check job status
status = ''
keys = ['status','jobid','percent','name']
for PANDASTR in PANDASTRs:
  status += (commands.getstatusoutput('pandamon %s' % PANDASTR)[1] + '\n')
jobs = [ dict(zip(keys,jobstat.split())) for jobstat in status.splitlines() ]
print status
print ""

# Get list of previous downloaded JobIDs or create new list
try:
  downloads = pickle.load( open( __downloadDB, 'rb' ) )
except IOError:
  downloads = {}

proxystatus = commands.getstatusoutput('voms-proxy-info')
if proxystatus[0]: fatal('need valid voms proxy to start downloads')

# Check list for new jobs with 'done' status
print "Submitting jobs:"
for job in jobs:
  if not job: continue
  if job['status'] == 'done':
    jobID = int(job['jobid'])
    if jobID in downloads: pass
    else:
      print "\t", job['name']
      downloads[jobID] = (time.time(), job['name'])
      cmd = 'qsub -q hep getsample.sh -F %s_MxAOD.root' % job['name'].replace('/','')
      substat = commands.getstatusoutput( cmd )
      if substat[0]:
        print "Batch job failed, returned value", substat[0]
      # Save file to log of downloads
      txtlog = open("log_downloads.txt", "a")
      txtlog.write( "{d:<22} {n}\n".format(d=time.strftime("%Y-%m-%d %H:%M"), n=job['name']) )
      txtlog.close()

# Save download list
pickle.dump( downloads, open( __downloadDB, 'wb' ) )
print ""
