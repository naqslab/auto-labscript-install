# Auto Labscript Install

## Getting started

Clone and navigate to this repository

```shell
cd /path/to/auto-labscript-install
```

Install:

* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://developer.hashicorp.com/vagrant/install)

Double check the `VagrantFile` suits your host enviornment

Then:

```shell
vagrant up --provision
```

This will take a while the first time running since it will download the OS image specified in the VagrantFile. I recommend doing this on the fastest internet you have, since Miniconda will also install inside the virtual machine.

To quit:

```shell
vagrant destroy
```

This will remove the VM and data inside, but keep the vagrant box so you don't need to redownload every time.
