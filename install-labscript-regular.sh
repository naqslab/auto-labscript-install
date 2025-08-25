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


echo "=== Appending labscript-suite to conda recognized channels ==="
conda config --env --append channels labscript-suite

echo "=== Appending labscript-suite to conda recognized channels ==="
conda install labscript-suite "pyqt<6" -y

echo "=== Creating labscript profile ==="
labscript-profile-create -c

echo "=== Installing Desktop Apps ==="
desktop-app install blacs lyse runmanager runviewer


