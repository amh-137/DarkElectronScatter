echo "================Running================"
echo "> Adding CVM-FS ROOT to PATH"
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.12.06/x86_64-fedora26-gcc72-opt/root/bin/thisroot.sh
echo "> Done, PATH="
echo $PATH | tr ":" "\n"
echo


# copy the DarkTridentGen file (uncompiled) to the local scratch directory
echo "Cloning DarkTridentGen to local folder"
cd $_CONDOR_SCRATCH_DIR/tmp
rm -rf DarkTridentGen # clean directory
cp ~/repo/pure/DarkTridentGen $_CONDOR_SCRATCH_DIR/tmp/DarkTridentGen -r
cd $_CONDOR_SCRATCH_DIR/tmp/DarkTridentGen

echo "===============ls================"
ls -l -a
echo



# GET THE pi0 and eta files
echo "=======Getting Neutral Meson Flux==========="
source setup.sh
echo


# Get the parameter cards
cd ~/repo/DarkElectronScatter/Noether/
cp -r scalar $_CONDOR_SCRATCH_DIR/tmp/DarkTridentGen
cp -r fermion $_CONDOR_SCRATCH_DIR/tmp/DarkTridentGen
cp -r signal_out_test $_CONDOR_SCRATCH_DIR/tmp/DarkTridentGen
cd $_CONDOR_SCRATCH_DIR/tmp/DarkTridentGen

echo
echo "!!!!====================!!!!"
echo $PWD
echo "!!!!====================!!!!"
echo

ls -l


# Compile
echo "===========Compiling==============="
./BdNMC/bin/BDNMC $1
echo "Done"

