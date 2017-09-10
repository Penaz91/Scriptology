#!/bin/sh
if [[ $# -eq 1 ]]; then
	case $1 in
		"up")
			xbacklight +3;;
		"down")
			xbacklight -3;;
		*)
			echo "Invalid Option";;
	esac
fi

dbus-send --session --type=signal / com.penaz.BrightnessChanged
