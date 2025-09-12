# Auto Labscript Install

## Getting started

Clone and navigate to this repository

```shell
cd /path/to/auto-labscript-install
```

Install:

* [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (For windows hosts)
* [Libvirt](https://documentation.ubuntu.com/server/how-to/virtualisation/libvirt/) (For linux hosts)
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

This will take a while the first time running since it will download the OS image specified in the VagrantFile in the form of a vagrant box (~6 GB).
I recommend doing this on the fastest internet you have, since Miniconda will also install inside the virtual machine.
You can alternatively download the Miniconda installer into this repository as the Vagrantfile will share this folder with the VM. 

The guest username and password are both `vagrant`.  

Subsequent opens of the VM can be done with:

```shell
vagrant up
```

To quit and clear the VM:

```shell
vagrant destroy -f
```

This will remove the VM and data inside, but keep the vagrant box so you don't need to redownload every time.


## Goals and Steps

The idea is to have scripts that enable the following list to be automated:

- Launch a virtual machine (Windows, Linux, MacOS)
- Get python and chosen package manager (conda, pip)
- Installs the labscript-suite (editable, regular)
- Opens up each component and tests/exercises their key features (runmanager, blacs, lyse, runviewer)
- Leaves the VM in a state that can be accessed to test small perturbations and features, as well as to explore small quirks that inevitably arise during the labscript install process

## Progress

A table of current working components of the above list, assuming the item runs without intervention from `vagrant up --provision`

| Guest OS | Launch VM | Get Conda/Pip | Install Labscript (Editable/Regular) | Exercise Features | Graceful Exit |
| -------- | --------- | ------------- | ------------------------------------ | ----------------- | ------------- |
| Linux    | -[ ]      | -[ ] / -[ ]   | -[ ] / -[ ]                          | -[ ]              | -[ ]          |
| Windows  | -[x]      | -[x] / -[ ]   | -[ ] / -[ ]                          | -[ ]              | -[ ]          |
| MacOS    | -[ ]      | -[ ] / -[ ]   | -[ ] / -[ ]                          | -[ ]              | -[ ]          |
