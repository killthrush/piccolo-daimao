#!/bin/bash

# Set up paths and directories
SOURCE_PATH="/usr/local/piccolo-daimao/apps"
WRITE_PATH="/var/local/piccolo-daimao"
DATABASE_PATH=$WRITE_PATH/sqlite
sudo mkdir -p $DATABASE_PATH

# Set up python runtime environment
PYTHON_APP_PATH="$SOURCE_PATH/python-falcon"
sudo pip install --upgrade pip
sudo pip install virtualenv
cd $PYTHON_APP_PATH
pip install -r ./requirements.txt
virtualenv $PYTHON_APP_PATH
source ./bin/activate

# Set up phoenix/elixir runtime environment
ELIXIR_APP_PATH="$SOURCE_PATH/elixir-phoenix"
cd $ELIXIR_APP_PATH
mix local.hex --force
mix archive.install --force https://github.com/phoenixframework/archives/raw/master/phoenix_new.ez
mix deps.get --force
mix local.rebar --force

# Set up nodejs runtime environment
NODE_APP_PATH="$SOURCE_PATH/node"
npm upgrade
sudo npm install -g n
sudo npm install -g nodemon
sudo n latest
cd $NODE_APP_PATH
npm install

# Set up database
cd $DATABASE_PATH
source $SOURCE_PATH/sqlite/run_script.sh $SOURCE_PATH/sqlite/create_database.sql
sudo chmod -R a+w $DATABASE_PATH