#!/bin/bash

if ping -c 1 google.com &> /dev/null; then
	echo "Все ОК!"
else
	echo "Сайт не доступен." >> /home/andrei/devops_learning/02_Linux/05_scripts/alert.log
fi
