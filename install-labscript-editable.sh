ENV_NAME='labscript'
GIT_REPO_OWNER='labscript-suite'

# check if env exists in conda list
if ! conda info --envs | grep -q "$ENV_NAME"; then
	echo === "'$ENV_NAME' environment not found, creating now. ==="
	conda create -n "$ENV_NAME" python=3.11
else
	echo === "'$ENV_NAME' already exists, skipping creation ==="
fi

# active env is the one with * before it
if ! conda info --envs | grep -q "^\\*.*$ENV_NAME"; then
	echo "=== Activating Conda environment: $ENV_NAME ==="
	eval "$(conda shell.bash hook)"
	conda activate $ENV_NAME
else
	echo "=== Conda environment '$ENV_NAME' is already active ==="
fi

echo "=== Attempting to install git ==="
conda install git -y
echo "=== Attemping conda init ==="
conda init


echo "=== Creating labscript-suite dir ==="
mkdir ~/labscript-suite
cd labscript-suite


git clone https://github.com/$ENV_NAME/labscript
git clone https://github.com/$ENV_NAME/runmanager
git clone https://github.com/$ENV_NAME/blacs
git clone https://github.com/$ENV_NAME/lyse
git clone https://github.com/$ENV_NAME/runviewer
git clone https://github.com/$ENV_NAME/labscript-devices
git clone https://github.com/$ENV_NAME/labscript-utils


echo "=== Appending labscript-suite to conda recognized channels ==="
conda config --env --append channels labscript-suite

echo "=== Getting GUI tools ==="
conda install -y setuptools-conda "pyqt<6" pip desktop-app 

echo "=== Apply setuptools to each component ==="
setuptools-conda install-requirements labscript runmanager blacs lyse runviewer labscript-devices labscript-utils

echo "=== Pip editable installing each component ==="
pip install --no-build-isolation --no-deps -e labscript -e runmanager -e blacs -e lyse -e runviewer -e labscript-devices -e labscript-utils

echo "=== Creating labscript profile ==="
labscript-profile-create

echo "=== Getting desktop apps ==="
desktop-app install blacs lyse runmanager runviewer

echo "=== Conda remove conda ==="
conda remove conda
