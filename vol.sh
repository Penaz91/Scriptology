#!/bin/sh

step=3%

if [[ $# -eq 1 ]]; then
    case $1 in 
        "up")
            amixer -q sset Master $step+;;
        "down")
            amixer -q sset Master $step-;;
        "toggle")
            amixer set Master toggle;;
        *)
            echo "Invalid option";;
    esac
fi

dbus-send --session --type=signal  / com.penaz.AudioChanged
