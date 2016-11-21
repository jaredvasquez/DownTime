setupATLAS -q
lsetup root -q 
lsetup rucio -q

export PANDASTR='group.phys-higgs*cjmeyer'
voms-proxy-init -voms atlas -valid 96:00
voms-proxy-info
