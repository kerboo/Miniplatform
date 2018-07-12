```
Miniplatform
--------------------------------------------------------------
//环境说明:
python 2.7 + django 1.9


//部署说明:
client/
  --sysinfo6.py      客户端程序(系统为centos 6.x) 
  --sysconf6.ini     客户端配置文件(系统为centos 6.x)


---------------------------------------------------------------
//主机监控数据接口说明:
URL： http://youserver:port/getdatas/
//参数格式:
{
    "cpu_useage": "10",     //CPU使用率
    "memory_useage": "50",  //内存使用率
    "disk_useage": " {      //磁盘各分区使用率(目前仅支持/  /home  /data)  
        'home': '70', 
        'root': '60',
        'data'： '30'
        }",
    "run_status": "10"       //运行时长   
}


//数据库实例接口说明:
URL： http://youserver:port/mysqlline/
//参数格式:
{
    "alive": 1,               //存活状态(1为活动,2为停止)
    "connections": "50",      //连接数
    "qps_useage": "30",       //QPS
    "tps_useage": "70",       //TPS 
    "slow_query": "100",      //慢查询量
    "buffer_useage": "555",   //缓存使用率
    "buffer_hitrate": "66",   //缓存命中率
}
//返回参数
{ 
   "msg":"",    //消息内容
   "code":"",    //消息状态码(201 正常,400 错误)
   "status":""   //消息状态(false 失败,True 成功)
}
```
