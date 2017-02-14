#!/bin/bash

#set -e
echo ">> Installing homebrew..."
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
echo
echo ">> Installing python..."
brew install python
echo
echo ">> Upgrading pip..."
pip install --upgrade pip
echo
echo ">> Installing python dependencies..."
pip install -r requirements.txt
echo
echo ">> Cleaning up..."
brew cleanup
echo
echo ">> Done."
echo
