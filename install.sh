sudo apt --assume-yes update
sudo apt --assume-yes upgrade
sudo apt --assume-yes install neovim git ranger python3-pip ffmpeg libatlas-base-dev



pip3 install numpy plotext scipy evdev Pillow
git clone https://github.com/garid3000/Spectrum-Catcher-V2
echo "python3 Spectrum-Catcher-V2/main.py" >> .bashrc


sudo rm -rf ~/LCD-show
git clone https://github.com/goodtft/LCD-show
chmod -R 755 LCD-show
cd LCD-show/
sudo LCD-show/MHS35-show

sudo reboot

