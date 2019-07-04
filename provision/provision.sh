#!/bin/bash

# Encourage not to prompt for stuff
export DEBIAN_FRONTEND=noninteractive
export DEBIAN_PRIORITY=critical

# Add the Neo4j debian repository so we can install it
wget -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.org/repo stable/' | sudo tee /etc/apt/sources.list.d/neo4j.list

# Update the package cache
apt-get -qy update
# Upgrade currently installed packages
apt-get -qy -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold" upgrade
apt-get -qy autoclean

# Stuff we want installed
GENERAL_PKGS="ack curl tree vim wget"
PYTHON_PKGS="python3 python3-pip python3-virtualenv virtualenvwrapper"
NEO_PKGS="openjdk-11-jre neo4j"
# Install them
apt-get -qy install $GENERAL_PKGS $PYTHON_PKGS $NEO_PKGS
