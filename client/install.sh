#!/bin/sh
#install client
#定义环境

WORKDIR="/home/scripts"
CLIENTIP="10.1.5.14"
SERVERIP="10.1.5.8"

yum -y install epel-release
yum -y install python-pip
pip install poster
#pip install psutil

check_mysql=`rpm -qa|grep mysql|grep devel|wc -l`
if [ $check_mysql -gt 0 ];then
   pip install mysql-python
fi

if [ -f "$WORKDIR/psutil-5.4.5.tar.gz" ];then    
tar -zxf psutil-5.4.5.tar.gz &&  cd psutil-5.4.5 &&  python setup.py install
else
   echo "psutil install faild" >>$WORKDIR/run.log
fi  

cd  $WORKDIR

cat <<EOF >>run.sh
#!/bin/bash

cd  /home/scripts
python sysinfo6.py  2>&1 >>run.log
EOF
chmod +x run.sh

cat <<EOF >>sysconf.ini
[mydb]
host = 127.0.0.1
user = root
password = 123456

[myurl]
sysurl = http://$SERVERIP:4000/getdatas/
sqlurl = http://$SERVERIP:4000/mysqlline/

[myip]
ip=$CLIENTIP

EOF
echo "*/3 * * * *  /home/scripts/run.sh 2>&1 >/dev/null" >>/var/spool/cron/root
ls -l  $WORKDIR
crontab -l

