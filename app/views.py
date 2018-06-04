# coding: utf-8
from django.shortcuts import render
from app.models import   Assets, MonitorDatas,MysqlInfo
from app.serializer import MonitorDatasSerializer,AssetsSerializer,MysqlInfoSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from django.http.response import HttpResponse




def Index(request):
    host_total_count=Assets.objects.all().count()
    host_physical_count=Assets.objects.filter(host_style=1).count()
    host_vtrul_count=Assets.objects.filter(host_style=2).count()
    net_hardware_count=Assets.objects.filter(host_style=2).count()
    rep_data = Assets.objects.all()
    return render(request,'index.html',locals())


def Host_details(request):
    rep_data = Assets.objects.all()
    obj_list = []  
    for x in rep_data:
        obj_dict = {}
        obj_dict['ip'] = x.ipaddr
        monitor_data_obj = MonitorDatas.objects.filter(hostid_id=x.id).latest('id')
        if monitor_data_obj:
            obj_dict['cpu'] = monitor_data_obj.cpu_useage
            obj_dict['memory'] = monitor_data_obj.memory_useage

            obj_dict['uptime'] = monitor_data_obj.run_status
            obj_dict['record_time'] = monitor_data_obj.date
        else:
            obj_dict['cpu'] = 'None'
            obj_dict['memory'] = 'None'
            obj_dict['uptime'] = 'None'
            obj_dict['record_time'] = 'None'
            
        obj_list.append(obj_dict)  

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



