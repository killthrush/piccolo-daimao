# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/xenial64"

  # Set this VM up so it can be visible on the network.
  # Follow prompts during 'vagrant up' to bridge to the correct interface.
  # This allows us to test applications from the network as opposed to locally.
  config.vm.network "public_network"

  # Share applications with the VM
  config.vm.synced_folder "./apps", "/usr/local/piccolo-daimao"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "3072" # This can be tweaked; I'm currently using a macbok air with not much RAM
  end

  config.vm.provision "shell", inline: <<-SHELL

    # Set up paths and directories
    SOURCE_PATH="/usr/local/piccolo-daimao"
    WRITE_PATH="/var/local/piccolo-daimao"
    DATABASE_PATH=$WRITE_PATH/sqlite
    sudo mkdir -p $DATABASE_PATH

    # Set up extra repositories
    sudo add-apt-repository ppa:pypy/ppa
    sudo apt-get update

    # Set up python runtime environment
    PYTHON_APP_PATH="$SOURCE_PATH/python-falcon"
    sudo apt-get install -y python-pip
    sudo apt-get install -y pypy
    sudo pip install --upgrade pip
    sudo pip install virtualenv
    virtualenv $PYTHON_APP_PATH
    cd $PYTHON_APP_PATH
    source ./bin/activate
    pip install -r ./requirements.txt

    # Set up SQLite
    sudo apt-get install -y sqlite3 libsqlite3-dev
    cd $DATABASE_PATH
    source $SOURCE_PATH/sqlite/run_script.sh $SOURCE_PATH/sqlite/create_database.sql

  SHELL
end
