#!/bin/bash
before_reboot(){
# install dependencies
    sudo apt-get install python-pyaudio python3-pyaudio
    sudo apt-get install flac
# install google voice bindings
    sudo pip install SpeechRecognition

# install media jack for Ubuntu to solve error
    sudo apt-get install multimedia-jack
    sudo dpkg-reconfigure -p high jackd2
    sudo adduser $(whoami) audio
    echo "Ubuntu must restart for media jack updates to take effect"
}

after_reboot(){
# This will run upon startup and solve the jack server error
    pulseaudio --kill
    jack_control start
}

# Split the script into two parts: before & after update
if [ -f /var/run/audio-update ]; then
    after_reboot
    rm /var/run/audio-update
    update-rc.d myupdate remove
    echo "SpeechRecognition should now function without media jack errors"
else
    before_reboot
    touch /var/run/audio-update
    update-rc.d myupdate defaults
# media jack updates require reboot
    while true; do
        read -p "Do you wish to restart Ubuntu now?" yn
        case $yn in
            [Yy]* ) sudo reboot; break;;
            [Nn]* ) exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done
fi
