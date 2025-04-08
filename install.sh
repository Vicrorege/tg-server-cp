#!/usr/bin/bash

echo "Instalation started..."
if [ "$EUID" -ne 0 ]; then
    exec sudo "$0" "$@"
    exit $?
fi
echo "Generating venv.."
python3 -m venv venv
echo "Venv generated succsessful!"
echo "Required libs installing..."
./venv/bin/pip3 install pyTelegramBotAPI
echo "Libs installed succsessful!"

nano ./tgcp.service
cp ./tgcp.service /etc/systemd/system/tgcp.service

nano ./config.json
echo "Press any button to continue"
pause
systemctl enable tgcp
systemctl start tgcp
echo "Complited!"
