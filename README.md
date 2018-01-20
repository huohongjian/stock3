# stock3

## Install Freebsd
1. pkg install python36
2. python3.6 -m ensurepip
3. pkg install libxml2 libxslt py36-libxml2
4. pip3 install lxml
5. pip3 install numpy pandas xlrd requests bs4 tushare

6. ln -s /usr/local/bin/python3.6 /usr/local/bin/python
7. pip3 install tqdm colorama

## Install in Freebsd venv


## Install in Linux


## Upgrade
pip3 install tushare --upgrade

## setup crontab
crontab -l  	#显示用户crontab文件内容
crontab -e		#编辑用户crontab文件内容
0 16 * * mon-fri /home/hhj/stock3/bin/fetch.py

## 解决方向键乱码问题
sudo ln -s /usr/local/bin/bash /bin/bash	-- For FreeBSD
sudo pip3 install readline
import readline

