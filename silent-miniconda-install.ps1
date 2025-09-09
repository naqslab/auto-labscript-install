param (
    [switch]$Online
)

$minicondaInstaller = "Miniconda3-latest-Windows-x86_64.exe"
$downloadUrl = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"

$minicondaPath = "C:\Miniconda3"
$syncedFolderPath = "C:\vagrant"
$installerPath = "$env:TEMP\$minicondaInstaller"

if (Test-Path -Path $minicondaPath -PathType Container) {
    Write-Output "The directory '$minicondaPath' exists. Skipping install."
}
else {
    Write-Output "The directory '$minicondaPath' does not exist. Installing now."

    try {
        if ($Online) {
            Write-Output "Downloading Miniconda installer..."
            Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing -ErrorAction Stop
        }
        else {
            Write-Output "Using local Miniconda installer from synced folder..."
            $installerPath = Join-Path $syncedFolderPath $minicondaInstaller
            if (!(Test-Path $installerPath)) {
                throw "Installer not found at $installerPath"
            }
        }

        Write-Output "Running Miniconda installer silently..."
        $installargs = @(
            "/S"
            "/InstallationType=JustMe"
            "/AddToPath=1"
            "/D=$minicondaPath"
        )

        $proc = Start-Process -FilePath $installerPath -ArgumentList $installargs -Wait -PassThru -ErrorAction Stop

        if ($proc.ExitCode -ne 0) {
            throw "Installer exited with code $($proc.ExitCode)"
        }

        Write-Output "Miniconda installed successfully in $minicondaPath."
    }
    catch {
        Write-Error "Failed to install Miniconda: $_"
        exit 1
    }
    try {
        conda init powershell
    }
    catch {
        Write-Error "Failed to init Miniconda powershell: $_"
    }
}
