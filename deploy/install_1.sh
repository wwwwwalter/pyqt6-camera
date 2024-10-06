#!/bin/bash
# Dir
rm -r ~/Bookshelf
rm -r ~/Documents
rm -r ~/Desktop
rm -r ~/Downloads
rm -r ~/Music
rm -r ~/Pictures
rm -r ~/Public
rm -r ~/Templates
rm -r ~/Videos

# apt
sudo mv /etc/apt/sources.list /etc/apt/sources.list.back
sudo cp sources.list /etc/apt/sources.list
sudo cp raspi.list /etc/apt/sources.list.d/raspi.list
sudo apt update
sudo apt install vim -y


# pip
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple



# mamba
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh
bash Miniforge3-Linux-aarch64.sh
rm ~/.condarc
cp .condarc ~


