function Migrate {
    param (
        [string]$Component
    )
    Write-Host "=== Attempting $Component Migration === "
    conda remove -f $Component
    pip install -e "$PathToFolder\$Component"
    Write-Host "=== $Component Migration Successful === "

}
$FolderName = "labscript-suite"
$PathToFolder = "$env:USERPROFILE\$FolderName"
# active env is the one with * before it
# TODO: Handle empty string -> should be case where conda doesn't exist
if (-not (conda env list | Select-String -Pattern "^\*.*$ENV_NAME")) {
    Write-Host "=== Activating Conda environment: $ENV_NAME ==="
    conda init powershell # maybe unnecessary
    conda activate $ENV_NAME
} else {
    Write-Host "=== Conda environment "$ENV_NAME" is already active. ==="
}

$labscriptList = "labscript", "runmanager", "blacs", "lyse", "runviewer", "labscript-devices", "labscript-utils"

foreach ($item in $labscriptList) {
    Migrate $item
}