sudo apt update
sudo apt install vsftpd -y

sudo mv /etc/vsftpd.conf /etc/vsftpd.conf.bak
sudo cp vsftpd.conf /etc/vsftpd.conf
sudo systemctl restart vsftpd

rm ~/.config/autostart/ai.desktop
mkdir -p ~/.config/autostart
cp ai.desktop ~/.config/autostart/ai.desktop
