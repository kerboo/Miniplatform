# coding: utf-8
from django.shortcuts import render
from app.models import   Assets, MonitorDatas,MysqlInfo
from app.serializer import MonitorDatasSerializer,AssetsSerializer,MysqlInfoSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from django.http.response import HttpResponse
from django.utils.timezone import now, timedelta
from django.db.models import Q
import json
import datetime
from pytz import timezone
from datetime import date



def Index(request):
    host_total_count=Assets.objects.all().count()
    host_physical_count=Assets.objects.filter(host_style=1).count()
    host_vtrul_count=Assets.objects.filter(host_style=2).count()
    net_hardware_count=Assets.objects.filter(host_style=2).count()
    rep_data = Assets.objects.all()
    return render(request,'index.html',locals()) 

"""
    result = {}
    rows = []
    limit = int(request.GET.get('ps'))
    pageNumber = int(request.GET.get('cp'))
    print limit,pageNumber
    start_index = (pageNumber-1)*limit
    end_index = start_index + (int(limit)-1)
    rep_data = Assets.objects.all().values()[start_index:end_index]
    print rep_data[0]
    for item in rep_data:
        temp_dict = {}
        temp_dict['id'] = item['id']
        temp_dict['ip'] = item['ipaddr']
        temp_dict['hstyle'] = item['host_style']
        temp_dict['sysver'] = item['sys_version']
        temp_dict['cpu'] =  item['cpu']
        temp_dict['disk'] =  item['disk']
        temp_dict['mem'] =   item['memory']
        temp_dict['status'] = item['status']
        temp_dict['addtime'] = item['date_added'].strftime('%Y-%m-%d %H:%M:%S')
        temp_dict['context'] = item['comment']
        rows.append(temp_dict)
    result['total'] = Assets.objects.all().count()
    result['rows'] = rows
    result['page'] = result['total']/limit + 1
    result = json.dumps(result)    
"""
   
   

@api_view(['GET','POST'])
def assets_list(request):
    if request.method == 'GET':
        assets_data = Assets.objects.all()
        serializer = AssetsSerializer(assets_data,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = AssetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
         
@api_view(['GET','POST'])
def data_list(request):    
    if request.method == 'GET':
        mdata = MonitorDatas.objects.all()
        serializer = MonitorDatasSerializer(mdata,many=True)
        return Response(serializer.data)

    
    elif request.method == 'POST':
        req_data = request.data
        if req_data['ip']:
            host_id = Assets.objects.filter(ipaddr=req_data['ip'])[0].id
            req_data.pop('ip')
            req_data['hostid'] =  host_id          
        else:
            return HttpResponse("POST argments is errors")
        
        serializer = MonitorDatasSerializer(data=req_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
@api_view(['GET','POST'])
def dbstat_list(request):
    if request.method == 'GET':
        mdata = MysqlInfo.objects.all()
        serializer = MysqlInfoSerializer(mdata,many=True)
        return Response(serializer.data)    


    if request.method == 'POST':
        req_data = request.data
        print req_data
        if req_data['ip'] and req_data['alive']:
            host_id = Assets.objects.filter(ipaddr=req_data['ip'])[0].id
            req_data.pop('ip')
            req_data['hostid'] =  host_id          
        else:
            return HttpResponse("POST argments is errors")
                
        serializer = MysqlInfoSerializer(data=req_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

def Host_details(request,hid):
    if not hid:        
        return HttpResponse("parm wrong")    
    host_infos = Assets.objects.filter(id=hid)[0]
    obj_dict = {}  
    monitor_data_obj = MonitorDatas.objects.filter(hostid_id=hid).latest('id')  
    if monitor_data_obj:
        obj_dict['id'] = monitor_data_obj.hostid_id
        obj_dict['cpu'] = monitor_data_obj.cpu_useage
        obj_dict['memory'] = monitor_data_obj.memory_useage
        obj_dict['disk'] = monitor_data_obj.disk_useage
        obj_dict['uptime'] = monitor_data_obj.run_status
        obj_dict['record_time'] = monitor_data_obj.date
    return render(request,'detailed.html',locals())
  
def get_history_data(request,hid,interval):
    result = { 
        "time_rs": [],
        "cpu_rs" : [],
        "mem_rs" : [],
        "disk":{ 
            "root_rs" : [],
            "home_rs" : [],
            "data_rs" : []
            }
        }
    
    hid = int(hid)
    if not interval:
        interval = 7
    else:
        interval = int(interval)
    start = now()
    if interval == 1:
        endtime = start - timedelta(hours=24)
    if interval == 7:    
        endtime = start - timedelta(days=7)
    if interval == 30:
        endtime = start - timedelta(days=30)
    if interval == 90:
        endtime = start - timedelta(days=90)
    if interval == 180:
        endtime = start - timedelta(days=180)        
    select_datas = MonitorDatas.objects.filter(Q(hostid=hid) & Q(date__gt=endtime)).values()    
    if select_datas:
        for item in select_datas:
            result['time_rs'].append(item['date'].strftime('%Y-%m-%d %H:%M:%S'))
            result['cpu_rs'].append(item['cpu_useage'])
            result['mem_rs'].append(item['memory_useage'])
            tmp_disk_dict = eval(item['disk_useage']) 
            result['disk']['root_rs'].append(tmp_disk_dict['root'])
            if 'home' in tmp_disk_dict.keys():
                result['disk']['home_rs'].append(tmp_disk_dict['home'])
            if 'data' in tmp_disk_dict.keys():
                result['disk']['data_rs'].append(tmp_disk_dict['data'])
            print result      
    result = json.dumps(result)      
    return HttpResponse(result)


def get_table_test(request,hid):
    if not hid:
        hid = 1
    limit = int(request.GET.get('ps'))
    pageNumber = int(request.GET.get('cp'))
    start_index = (pageNumber-1)*limit
    end_index = start_index + (int(limit)-1)
    result = {}
    newlist = []
    all_res = MonitorDatas.objects.filter(hostid_id=hid).count()
    monitor_data_obj = MonitorDatas.objects.filter(hostid_id=hid).values('cpu_useage','disk_useage','memory_useage','date','run_status')[start_index:end_index]
    for item in  monitor_data_obj:
        obj_dict = {} 
        obj_dict['cpu'] = item['cpu_useage']
        obj_dict['memory'] = item['memory_useage']
        obj_dict['disk'] = item['disk_useage']
        obj_dict['uptime'] = item['run_status']
        obj_dict['record_time'] = item['date'].strftime('%Y-%m-%d %H:%M:%S')        
        newlist.append(obj_dict)
    result['total'] = all_res
    result['rows'] = newlist
    result['page'] =  all_res/limit + 1
    result = json.dumps(result)
    return HttpResponse(result)    
    
    


