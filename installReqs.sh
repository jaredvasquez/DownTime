# Install pandamonium 
install_pandamon() {
  git clone https://github.com/dguest/pandamonium.git
  newPATH="export PATH=\"$PWD/pandamonium:\$PATH\""
  echo "Adding following line to your .bashrc"
  echo $newPATH
  echo "" >> ~/.bashrc
  echo $newPATH >> ~/.bashrc
  echo ""
}

# Create downloads folder
#  --> needed to source xAODMerge
create_download() {
  mkdir pbslogs download
  cd download
  setupATLAS
  rcSetup Base,2.4.22
  rc find_packages
  rc compile
  cd ../          #return to initial dir
}
