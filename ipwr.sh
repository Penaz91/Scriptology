#!/bin/sh
# Un semplice script per il controllo granulare
# dello spegnimento e del riavvio del sistema
while test $# -gt 0; do
	case "$1" in
		-h|--help)
			echo "Usage:"
			echo " "
			echo "-s|--shutdown -> Perform System Halt"
			echo "-r|--reboot   -> Perform System Reboot"
			exit 0
			;;
		-s|--shutdown)
			echo "This will perform a full System halt, do you want to continue? [y/N]"
			read A
			case "$A" in
				y|yes|Yes|Y)
					shutdown -h now
					exit 0
					;;
				n|no|No|N)
					echo "Shutdown cancelled"
					exit 0
					;;
				*)
					echo "Invalid answer, assuming 'no'"
					break
					;;
			esac
			;;
		-r|--reboot)
			echo "This will perform a System reboot, do you want to continue? [y/N]"
			read A
			case "$A" in
				y|yes|Yes|Y)
					shutdown -r now
					exit 0
					;;
				n|no|No|N)
					echo "Reboot cancelled"
					exit 0
					;;
				*)
					echo "Invalid answer, assuming 'no'"
					break
					;;
			esac
			;;
		*)
			break
			;;
	esac
done
