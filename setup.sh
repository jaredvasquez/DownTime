setupATLAS -q
lsetup root -q 
lsetup rucio -q
voms-proxy-init -voms atlas -valid 96:00
voms-proxy-info
