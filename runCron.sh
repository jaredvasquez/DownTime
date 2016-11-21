
# Setup Environment 
echo "Setting Up Environment..."
source  ~/.bashrc
setupATLAS -q
lsetup root -q 
lsetup rucio -q
echo ""
echo ""

# Run Scripts
export PANDASTR='group.phys-higgs*cjmeyer'
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/checkStatus.py
