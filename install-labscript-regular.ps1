# invoke with powershell.exe -File install-labscript.ps1 in anaconda powershell

$ENV_NAME = "labscript"
# $GIT_REPO_OWNER = "labscript-suite"
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

Write-Host "=== Appending labscript-suite to conda recognized channels === "
conda config --env --append channels labscript-suite

# active env is the one with * before it
# TODO: Handle empty string -> should be case where conda doesn't exist
if (-not (conda env list | Select-String -Pattern "^\*.*$ENV_NAME")) {
    
    # conda init powershell # maybe unnecessary
    Write-Host "=== Activating Conda environment: $ENV_NAME ==="
    conda activate $ENV_NAME
} else {
    Write-Host "=== Conda environment "$ENV_NAME" is already active. ==="
}

# Write-Host "=== Attempting to install git ==="
# conda install -y git

Write-Host "=== Creating labscript-suite dir ==="
$FolderName = "labscript-suite"
$PathToFolder = "$env:USERPROFILE\$FolderName"
New-Item -Path $PathToFolder -ItemType Directory 
Set-Location "$PathToFolder"

Write-Host "=== Conda install labscript-suite ==="
conda install labscript-suite "pyqt<6" -y

Write-Host "=== Creating labscript profile === "
labscript-profile-create -c

Write-Host "=== Getting desktop apps === "
desktop-app install blacs lyse runmanager runviewer -y

Write-Host "=== Getting pip === "
conda install pip -y