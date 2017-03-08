#!/bin/bash

# Ubuntu package installs (change this based on your linux flavor)
# Installs:
# - NTP util - allows clock syncing when vagrant VMs drift off (a common problem)
# - Erlang VM and Elixir
# - Python's pip package manager (python 2.7 is installed by default)
# - NPM - Node package manager - allows us to bootstrap a NodeJS environment
# - Redis & SQLite
sudo apt-get install ntpdate
rm erlang-solutions_*.deb || true
wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb && sudo dpkg -i erlang-solutions_1.0_all.deb
sudo apt-get update
sudo apt-get install -y esl-erlang
sudo apt-get install -y elixir
sudo apt-get install -y python-pip
sudo apt-get install -y npm
sudo apt-get install -y redis-server
sudo apt-get install -y sqlite3 libsqlite3-dev