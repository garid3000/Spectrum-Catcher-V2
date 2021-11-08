cd /home/pi/Spectrum-Catcher-V2
out=$(git pull)
echo $out


if [ "$out" = "Already up to date." ]; then
    echo no reboot
else
    echo "updated"
    sudo reboot
fi;
#reboot
