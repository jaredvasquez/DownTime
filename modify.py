import sys, pickle

__downloadDB = 'logdls.pkl'

operation  = sys.argv[1]
samplename = sys.argv[2]

samplename = samplename.replace('_MxAOD.root','')
if samplename[-1] != '/':
  samplename += '/'

#print 'Will run %s for sample %s' % (operation,samplename)
try:
  downloads = pickle.load( open( __downloadDB, 'rb' ) )
except IOError:
  downloads = {}

dlsamples = { downloads[k][1]: k for k in downloads }

def findSample( samplename ):
  if samplename in dlsamples: return True
  return False

if operation == 'find':
  if not findSample(samplename):
    print 'Sample %s not found.' % samplename

if operation == 'remove':
  if findSample(samplename):
    del downloads[dlsamples[samplename]]
    del dlsamples[samplename]
    if not findSample(samplename):
      print 'Removed %s successfully.' % samplename
      pickle.dump( downloads, open( __downloadDB, 'wb' ) )
  else:
    print 'Not Found: %s' % samplename

