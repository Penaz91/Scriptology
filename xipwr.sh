#!/bin/sh
gxmessage "Are you sure you want to shut down your computer?" -center -title "Shutdown Dialog" -fon -borderless -buttons "_Cancel, _Log Out, _Reboot, _Shut Down"

case $? in
	1)
		echo "Exit";;
	2)
		openbox --exit;;
	3)
		sudo shutdown -r now;;
	4)
		sudo shutdown -h now;;
esac
