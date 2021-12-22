rm ~/spe.bmp
rm ~/cam.bmp
ffmpeg -hide_banner -loglevel error -i $(cat pm1/i) -t $(cat pm1/t) -vf drawbox=$(cat pm1/drawbox) -vf "transpose=1" -pix_fmt bgra -f fbdev /dev/fb0
#ffmpeg -hide_banner -loglevel error -i /dev/video0 -t 1 -pix_fmt bgra -f fbdev /dev/fb0

ffmpeg -hide_banner -loglevel error -f video4linux2 -i /dev/video0 -vframes 1 ~/spe.bmp
ffmpeg -hide_banner -loglevel error -f video4linux2 -i /dev/video2 -vframes 1 ~/cam.bmp
sleep 1
#printf '[3J'
clear
