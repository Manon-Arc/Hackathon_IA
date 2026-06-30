dnf install ollama 

ollama run phi3.5
dnf install firewalld 

systemctl start firewalld 
systemctl enable firewalld 

firewall-cmd --add-port=11434/tcp --permanent