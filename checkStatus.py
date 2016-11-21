import os, sys, pickle, datetime, commands

def fatal(error): print 'FATAL ERROR: %s' % error; sys.exit()

# Check for string in environment variables
if not 'PANDASTR' in os.environ: fatal('Must set env var PANDASTR')
PANDASTR = os.environ['PANDASTR']
print "Will search for jobs with string %s" % PANDASTR
print "Job last ran on", datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
print ""

# Use pandamonium to check job status
keys = ['status','jobid','percent','name']
status = commands.getstatusoutput('pandamon %s' % PANDASTR)[1]
jobs = [ dict(zip(keys,jobstat.split())) for jobstat in status.splitlines() ]
print status
print ""

# Get list of previous downloaded JobIDs or create new list
try:
  downloads = pickle.load( open( 'downloads.pkl', 'rb' ) )
except IOError:
  downloads = {}

proxystatus = commands.getstatusoutput('voms-proxy-info')
if proxystatus[0]: fatal('need valid voms proxy to start downloads')

# Check list for new jobs with 'done' status
print "Submitting jobs:"
for job in jobs:
  if job['status'] == 'done':
    jobID = int(job['jobid'])
    if jobID in downloads:
      pass
      ### Submit batchjob to download job
    else:
      print "\t", job['name']
      downloads[jobID] = job['name']

# Save download list
pickle.dump( downloads, open( 'downloads.pkl', 'wb' ) )
print ""
