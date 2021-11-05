clear
sudo setfont /etc/console-setup/cached_Uni2-TerminusBold16.psf.gz
cd /home/pi/main2

python3 spectra_text.py -s  --optimize=normal --engine=ffmpeg --number=20

clear
sudo setfont /etc/console-setup/cached_Uni2-Terminus32x16.psf.gz
