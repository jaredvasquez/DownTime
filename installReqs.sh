# Install pandamonium 
git clone https://github.com/dguest/pandamonium.git


# Create downloads folder
#  --> needed to source xAODMerge
mkdir pbslogs downloads
cd downloads
setupATLAS
rcSetup Base,2.4.22
rc find_packages
rc compile

# Return to initial direcory
cd ../
