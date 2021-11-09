#rm ~/spe.bmp
#rm ~/cam.bmp

cd /home/pi/Spectrum-Catcher-V2

ffmpeg -hide_banner -loglevel error -i $(cat pm1/i) -t $(cat pm1/t) -vf drawbox=$(cat pm1/drawbox) -pix_fmt bgra -f fbdev /dev/fb0


python3 spectra_text.py -D $(cat pm/device) -o $(cat pm/output) -d $(cat pm/datatype) -O $(cat pm/optimize) -e $(cat pm/engine) -n 1 -t $(cat pm/timer) -p $(cat pm/pov) -s -M $(cat pm/optupper) -m $(cat pm/optlower) -N $(date '+%b-%d_%H%M%S')


clear
