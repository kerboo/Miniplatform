#!/usr/bin/env  python
# -*- coding:utf-8 -*-

from __future__ import division
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import os
import sys
import re
import subprocess
import psutil
import urllib
import urllib2
import time
import MySQLdb
import ConfigParser

QPS = ''
TPS = ''
conn = ''
alive = ''
slow_q = ''
cache_u = ''
cache_h = ''
filepath = './sysconf6.ini'

def ip_info():
    regex_ip = re.compile(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}')
    regex_get = re.compile(r'([0-9]{1,3}[.]){3}(?!1$|255$).*$')
    inter_info = subprocess.Popen('ip addr',stdout=subprocess.PIPE,shell=True)
    stdout_value = inter_info.communicate()[0].decode('utf-8')
    result_ip = regex_ip.findall(stdout_value)
    final_ip = []

    for pre_ip in result_ip:
        if regex_get.search(pre_ip):
            final_ip.append(pre_ip)
    return final_ip[0]

def cpu_info():
    with open('/proc/stat','r') as cpu_file1:
        cpu_num1 = cpu_file1.read().split('\n')[0].split( )[1:]
    time.sleep(1)
    with open('/proc/stat','r') as cpu_file2:
        cpu_num2 = cpu_file2.read().split('\n')[0].split( )[1:]
    
    result_cpu_all1 = 0
    result_cpu_all2 = 0
    for pre_num1 in cpu_num1:
        result_cpu_all1 = result_cpu_all1 + int(pre_num1)
    for pre_num2 in cpu_num2:
        result_cpu_all2 = result_cpu_all2 + int(pre_num2)
    result_cpu_idle = (int(cpu_num2[3])-int(cpu_num1[3]))/(result_cpu_all2-result_cpu_all1)
    result_cpu_usage = (1 - result_cpu_idle)*100
    return ('%.2f'%result_cpu_usage)

def mem_info():
    with open('/proc/meminfo','r') as mem_file:
        mem_num = mem_file.read().split('\n')[0:4]
    pre_list = []
    for pre_mem in mem_num:
        pre_list.append(int(pre_mem.split( )[1]))
    result_mem_idle = (sum(pre_list[1:4]))/pre_list[0]
    result_mem_usage = (1 - result_mem_idle)*100
    return ('%.2f'%result_mem_usage)

def uptime_info():
    with open('/proc/uptime','r') as uptime_file:
        uptime_num = uptime_file.read().split( )[0]
    result_uptime = float(uptime_num)/3600/24
    return ('%.2f'%result_uptime)

def disk_info():
    disk_root = psutil.disk_usage('/')
    root_percent = ('%.2f'%disk_root.percent)
    disk_part = psutil.disk_partitions()
    data_percent = 'Null'
    home_percent = 'Null'
    for per_part in disk_part:
        disk_mount = per_part.mountpoint
        if disk_mount == '/data':
            disk_data = psutil.disk_usage('/data')
            data_percent = ('%.2f'%disk_data.percent)
        elif disk_mount == '/home':
            disk_home = psutil.disk_usage('/home')
            home_percent = ('%.2f'%disk_home.percent)
    if data_percent == 'Null' and home_percent == 'Null':
        disk_usage = {'root':root_percent}
    elif data_percent != 'Null' and home_percent == 'Null':
        disk_usage = {'root':root_percent,'data':data_percent}
    elif data_percent == 'Null' and home_percent != 'Null':
        disk_usage = {'root':root_percent,'home':home_percent}
    else:
        disk_usage = {'root':root_percent,'data':data_percent,'home':home_percent}
    sys_disk = disk_usage
    return sys_disk
########################################################################################
#MySQL status
def MySQL_info(Myhost,Myuser,Mypw):
    global QPS
    global TPS
    global conn
    global alive
    global slow_q
    global cache_u
    global cache_h

    alive_status = subprocess.Popen('mysqladmin -h 127.1 -u root -p'+Mypw+' ping',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    alive_result = alive_status.communicate()[0].strip( )
    if alive_result == 'mysqld is alive':
        alive = '1'
    else:
        alive = '2'
        return alive
    
    dbconn = MySQLdb.connect(Myhost,Myuser,Mypw,charset='utf8')
    cur = dbconn.cursor()
    cur.execute("""show global status where variable_name in(
                'Questions','Com_commit','Uptime','Com_rollback','Connections','Slow_queries',
                'Innodb_buffer_pool_pages_total','Innodb_buffer_pool_pages_free',
                'Innodb_buffer_pool_read_requests','Innodb_buffer_pool_reads')""")
    dbmore = cur.fetchall()
    cur.execute('show variables like "max_connections"')
    dbone = cur.fetchone()
    dbconn.close()
    
    QPS = int(dbmore[7][1])/int(dbmore[9][1])
    TPS = (int(dbmore[0][1])+int(dbmore[1][1]))/int(dbmore[9][1])
    conn = int(dbmore[2][1])/int(dbone[1])*100
    slow_q = dbmore[8][1]
    cache_u = (int(dbmore[4][1])-int(dbmore[3][1]))/int(dbmore[4][1])*100
    cache_h = (int(dbmore[5][1])-int(dbmore[6][1]))/int(dbmore[5][1])*100

    QPS = ('%.2f'%QPS)
    TPS = ('%.2f'%TPS)
    conn = ('%.2f'%conn)
    cache_u = ('%.2f'%cache_u)
    cache_h = ('%.2f'%cache_h)

    return alive,QPS,TPS,conn,slow_q,cache_u,cache_h

class ReadConfig(object):
    def __init__(self,fpath):
        self.path = fpath

    def getconfig(self):
        conf = ConfigParser.SafeConfigParser()
        conf.read(self.path)
        host = conf.get('mydb','host')
        user = conf.get('mydb','user')
        passwd = conf.get('mydb','password')
        return host,user,passwd

    def geturl(self):
        conf = ConfigParser.SafeConfigParser()
        conf.read(self.path)
        sysurl = conf.get('myurl','sysurl') 
        sqlurl = conf.get('myurl','sqlurl')
        return sysurl,sqlurl

def filejudge():
    file_result = os.path.isfile(filepath)
    if file_result == False:
        print("Config file does not exist in current directory")
        sys.exit(5)

def url_mydb():
    db_result = MySQL_info(host,user,passwd)
    if db_result == '2':
        values = { "ip":sys_ip,"alive":db_result }
    else:
        values = {
                   "ip":sys_ip,
                   "alive":db_result[0],
                   "connections":db_result[3],
                   "qps_useage":db_result[1],
                   "tps_useage":db_result[2],
                   "slow_query":db_result[4],
                   "buffer_useage":db_result[5],
                   "buffer_hitrate":db_result[6]
                  }
    url = sql_url
    register_openers()
    datagen,headers = multipart_encode(values)
    request = urllib2.Request(url,datagen,headers)
    print urllib2.urlopen(request).read()

def url_sys():
    register_openers()
    url = sys_url
    values = {
               "ip":sys_ip,
               "cpu_useage":sys_cpu,
               "memory_useage":sys_mem,
               "disk_useage":sys_disk,
               "run_status":sys_up
              }
    datagen,headers = multipart_encode(values)
    request = urllib2.Request(url,datagen,headers)
    print urllib2.urlopen(request).read()

if __name__ == "__main__":
    filejudge()
########################################################
    sys_ip = ip_info()
    sys_cpu = cpu_info()
    sys_mem = mem_info()
    sys_up = uptime_info()
    sys_disk = disk_info()
########################################################
    config = ReadConfig(filepath)
    host,user,passwd = config.getconfig()
    sys_url,sql_url = config.geturl()
########################################################
    url_sys()
    url_mydb()
