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

    # Set up extra repositories & NTP
    sudo apt-get install ntpdate
    rm erlang-solutions_*.deb || true
    wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb && sudo dpkg -i erlang-solutions_1.0_all.deb
    sudo apt-get update

    # Set up python runtime environment
    PYTHON_APP_PATH="$SOURCE_PATH/python-falcon"
    sudo apt-get install -y python-pip
    sudo pip install --upgrade pip
    sudo pip install virtualenv
    cd $PYTHON_APP_PATH
    pip install -r ./requirements.txt
    virtualenv $PYTHON_APP_PATH
    source ./bin/activate

    # Set up phoenix/elixir runtime environment
    ELIXIR_APP_PATH="$SOURCE_PATH/elixir-phoenix"
    sudo apt-get install -y esl-erlang
    sudo apt-get install -y elixir
    cd $ELIXIR_APP_PATH
    mix local.hex --force
    mix archive.install --force https://github.com/phoenixframework/archives/raw/master/phoenix_new.ez
    mix deps.get --force
    mix local.rebar --force

    # Set up nodejs runtime environment
    NODE_APP_PATH="$SOURCE_PATH/node"
    sudo apt-get install -y npm
    npm upgrade
    sudo npm install -g n
    sudo npm install -g nodemon
    sudo n latest
    cd $NODE_APP_PATH
    npm install

    # Set up SQLite & redis
    sudo apt-get install -y redis-server
    sudo apt-get install -y sqlite3 libsqlite3-dev
    cd $DATABASE_PATH
    source $SOURCE_PATH/sqlite/run_script.sh $SOURCE_PATH/sqlite/create_database.sql

  SHELL
end
