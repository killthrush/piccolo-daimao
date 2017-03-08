# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/xenial64"

  # Set this VM up so it can be visible on the network.
  # Follow prompts during 'vagrant up' to bridge to the correct interface.
  # This allows us to test applications from the network as opposed to locally.
  config.vm.network "public_network"

  # Share applications with the VM
  config.vm.synced_folder "./apps", "/usr/local/piccolo-daimao/apps"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "3072" # This can be tweaked; I'm currently using a macbok air with not much RAM
  end

  config.vm.provision "shell", path: "install_ubuntu.sh"
  config.vm.provision "shell", path: "install_main.sh"
end
