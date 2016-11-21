import sys
import pickle
import commands

# Use pandamonium to check job status
keys = ['status','jobid','percent','name']
status = commands.getstatusoutput('pandamon group.phys-higgs*cjmeyer')[1]
jobs = [ dict(zip(keys,jobstat.split())) for jobstat in status.splitlines() ]
print status
print ""

# Get list of previous downloaded JobIDs or create new list
try:
  downloads = pickle.load( open( 'downloads.pkl', 'rb' ) )
except IOError:
  downloads = {}

proxystatus = commands.getstatusoutput('voms-proxy-info')
if not proxystatus[0] == 0:
  print "FATAL ERROR: need valid voms proxy to start downloads"; sys.exit()

# Check list for new jobs with 'done' status
for job in jobs:
  if job['status'] == 'done':
    jobID = int(job['jobid'])
    if jobID in downloads:
      print "Already downloaded job %d" % jobID
      ### Submit batchjob to download job
      ###   --> how to setup proxy without giving away secrets?
    else:
      downloads[jobID] = job['name']

pickle.dump( downloads, open( 'downloads.pkl', 'wb' ) )
