clear
sudo setfont /etc/console-setup/cached_Uni2-TerminusBold16.psf.gz
cd /home/pi/Spectrum-Catcher-V2

#python3 spectra_text.py -s  --optimize=normal --engine=ffmpeg --number=20
python3 spectra_text.py -D $(cat pm/device) -o $(cat pm/output) -d $(cat pm/datatype) -O $(cat pm/optimize) -e $(cat pm/engine) -n $(cat pm/number) -t $(cat pm/timer) -p $(cat pm/pov) -s -M $(cat pm/optupper) -m $(cat pm/optlower) -N $(date '+%b-%d_%H%M%S')

clear
sudo setfont /etc/console-setup/cached_Uni2-Terminus32x16.psf.gz
