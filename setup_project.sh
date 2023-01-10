########################################################################################################################
### This shell script sets up the python environment and creates folders required to run the scripts that are not stored
### in the repo.
###
### Assumptions is that this will be run from the GitBash, this may need to be customised.
########################################################################################################################

### Setting up the python environment
source /c/ProgramData/Anaconda3/etc/profile.d/conda.sh
conda create -n MyVirEnv python=3.10 --yes
conda activate MyVirEnv
pip install -r requirements.txt

### Setting up the repo directories
mkdir input
mkdir output

## Create config.JSON for the user (copy from metadata)
cp metadata/config.json config.json

### Test repo setup
source run_pytests.sh