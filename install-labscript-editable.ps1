# invoke with powershell.exe -File install-labscript.ps1 in anaconda powershell

$ENV_NAME = "labscript"
$GIT_REPO_OWNER = "labscript-suite"

# Attempt 1 to accept TOS
Set-Variable CONDA_PLUGINS_AUTO_ACCEPT_TOS=true

# Attempt 2
try {
    conda tos accept 
} catch {
    
    # Quit entirely if it doesn't work both times :(
    Write-Error "Failed to accept TOS: $_"
    Exit
}

# Check if environment exists
if (-not (conda env list | Select-String -Pattern "$ENV_NAME")) {
    Write-Host "=== "$ENV_NAME" environment not found, creating now. ==="
    conda create -n $ENV_NAME python=3.11 -y
} else {
    Write-Host "=== "$ENV_NAME" already exists, skipping creation. ==="
}

# active env is the one with * before it
# TODO: Handle empty string -> should be case where conda doesn't exist
if (-not (conda env list | Select-String -Pattern "^\*.*$ENV_NAME")) {
    Write-Host "=== Activating Conda environment: $ENV_NAME ==="
    conda init powershell
    conda activate $ENV_NAME
} else {
    Write-Host "=== Conda environment "$ENV_NAME" is already active. ==="
}

Write-Host "=== Attempting to install git ==="
conda install -y git

Write-Host "=== Creating labscript-suite dir ==="
New-Item -ItemType Directory -Name "labscript-suite"
Set-Location "labscript-suite"

git clone "https://github.com/$($GIT_REPO_OWNER)/labscript"
git clone "https://github.com/$($GIT_REPO_OWNER)/runmanager"
git clone "https://github.com/$($GIT_REPO_OWNER)/blacs"
git clone "https://github.com/$($GIT_REPO_OWNER)/lyse"
git clone "https://github.com/$($GIT_REPO_OWNER)/runviewer"
git clone "https://github.com/$($GIT_REPO_OWNER)/labscript-devices"
git clone "https://github.com/$($GIT_REPO_OWNER)/labscript-utils"

Write-Host "=== Appending labscript-suite to conda recognized channels === "
conda config --env --append channels labscript-suite

# "Migrating to editable install" in the docs should cover the non setuptools-conda case
Write-Host "=== Getting GUI tools === "
conda install -y setuptools-conda "pyqt<6" pip desktop-app

Write-Host "=== Apply setuptools to each component === "
setuptools-conda install-requirements labscript runmanager blacs lyse runviewer labscript-devices labscript-utils

Write-Host "=== Pip editable installing each component === "
pip install --no-build-isolation --no-deps -e labscript -e runmanager -e blacs -e lyse -e runviewer -e labscript-devices -e labscript-utils

Write-Host "=== Creating labscript profile === "
labscript-profile-create -c

Write-Host "=== Getting desktop apps === "
desktop-app install blacs lyse runmanager runviewer -y

Write-Host "=== Conda remove conda === "
conda remove conda -y
