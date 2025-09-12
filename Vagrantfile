# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  ## TODO: Can these be moved into provider conditionals?
  #config.vm.box = "dstoliker/windows11" # virtualbox vagrantbox
  config.vm.box = "tonyclemmey/windows11" # libvirt vagrantbox
  #config.vm.box_version = "1.0.0" # commented out to skip check, which forces download

  config.vm.communicator = "winrm"
  config.winrm.username = "vagrant"
  config.winrm.password = "vagrant"
  config.vm.guest = :windows # Need this even though box is win11
  config.vm.provider "libvirt" do |lv|
    lv.memory = "16384"
    lv.cpus = "4"
  end
  config.vm.provider "virtualbox" do |vb|
    vb.gui = true # Need gui to see labscript components
    vb.memory = "16384"
    vb.cpus = "4"
  end
  config.winrm.port = 5985 # Default WinRM port
  config.winrm.timeout = 1800
  # config.winrm.retry_limit = 300 # 300 retries
  # config.winrm.retry_delay = 2

  #config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  config.vm.synced_folder ".", "/vagrant"

  # SHELL
  if config.vm.guest == :windows
    config.vm.provision "shell", path: "./silent-miniconda-install.ps1"
    config.vm.provision "shell", path: "./prep-labscript-env.ps1"
    config.vm.provision "shell", path: "./install-labscript-regular.ps1"
    # config.vm.provision "shell", path: "./migrate-install.ps1"
  elsif config.vm.guest == :linux
    config.vm.provision "shell", path: "./silent-miniconda-install.sh"
    config.vm.provision "shell", path: "./install-labscript-editable.sh"
  end

  # TODO: Provision the python scripts here 
end
