# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/xenial64"
  config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder "./apps", "/usr/local/piccolo-daimao"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "3072"
  end

  config.vm.provision "shell", inline: <<-SHELL

    # Set up python runtime environment
    MAIN_PATH="/usr/local/piccolo-daimao"
    PYTHON_APP_PATH="$MAIN_PATH/python-falcon"
    sudo apt-get install -y python-pip
    sudo pip install --upgrade pip
    sudo pip install virtualenv
    virtualenv $PYTHON_APP_PATH
    cd $PYTHON_APP_PATH
    source ./bin/activate
    pip install -r ./requirements.txt
    
  SHELL
end
