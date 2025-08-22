$minicondaInstaller = "Miniconda3-latest-Windows-x86_64.exe"
$downloadUrl = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"

$minicondaPath = "C:\\Miniconda3"

if (Test-Path -Path $minicondaPath -PathType Container) {
  Write-Host "The directory '$minicondaPath' exists. Skipping install"
} else {
  Write-Host "The directory '$minicondaPath' does not exist. Installing now."
  Invoke-WebRequest -Uri $downloadUrl -OutFile "$env:TEMP\\$minicondaInstaller"
  # /S for silent mode
  # /InstallationType=JustMe (recommended) or AllUsers
  # /AddToPath=1 (adds to PATH)
  # /D=<install_path> (destination path, must be last argument)
  Start-Process -FilePath "$env:TEMP\\$minicondaInstaller" -ArgumentList "/S /InstallationType=JustMe /AddToPath=1 /D=C:\\Miniconda3" -Wait -PassThru #
}