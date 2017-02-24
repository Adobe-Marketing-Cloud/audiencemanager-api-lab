#!/bin/bash

echo
#set -e

if ! type "brew" > /dev/null; then
    echo ">> homebrew was not found. Installing homebrew..."
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    echo
fi

if ! type "python" > /dev/null; then
    echo ">> python was not found. Installing python..."
    brew install python
    echo
fi

echo ">> Upgrading pip..."
sudo pip install --upgrade pip
echo

echo ">> Installing python dependencies..."
sudo pip install -r requirements.txt
echo

echo ">> Done."
echo
