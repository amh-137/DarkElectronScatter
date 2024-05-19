# DarkElectronScatter
Analysis of the Monte Carlo Generated Data for Dark Matter - Electron Scattering at MicroBooNE


# Noether
## Setup
1) Use the notebooks such as gen_param_cards.ipynb to make parameter cards for BdNMC to use
2) edit condor/jobsub.sh to use these parameter cards
3) Push the parameter cards and jobsub.sh to a branch of this repo

To run this on noether:
```
$ cd ~ && mkdir repo/pure && cd repo/pure
$ git clone https://github.com/lmlepin9/DarkTridentGen.git && cd DarkTridentGen
$ git swtich ElectronScatter
$ cd ~/repo
$ git clone https://github.com/SuchAgoodDoge/DarkElectronScatter.git && cd DarkElectronScatter/condor
$ source jobsub.sh
```
