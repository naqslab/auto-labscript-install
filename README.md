# Auto Labscript Install

## Getting started

Clone and navigate to this repository

```shell
cd /path/to/auto-labscript-install
```

Install:

* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Libvirt](https://documentation.ubuntu.com/server/how-to/virtualisation/libvirt/)
* [Vagrant](https://developer.hashicorp.com/vagrant/install)

Using `vagrant plugin install`, get the following plugins:
```text
vagrant-libvirt (0.12.2, global)
winrm (2.3.9, global)
winrm-elevated (1.2.3, global)

```

Double check the `Vagrantfile` suits your desired host-guest environment.

Then:

```shell
vagrant up --provision --provider=libvirt &> vagrant_up.log
```

This will take a while the first time running since it will download the OS image specified in the VagrantFile.
I recommend doing this on the fastest internet you have, since Miniconda will also install inside the virtual machine.
You can alternatively download the Miniconda installer into this repository as the Vagrantfile will share this folder with the VM. 

Subsequent opens of the VM can be done with:

```shell
vagrant up
```

To quit and clear the VM:

```shell
vagrant destroy -f
```

This will remove the VM and data inside, but keep the vagrant box so you don't need to redownload every time.
