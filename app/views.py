# coding: utf-8
from django.shortcuts import render
from app.models import   Assets, MonitorDatas
from app.serializer import MonitorDatasSerializer,AssetsSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from django.http.response import HttpResponse


def Index(request):
    hh = "myhomepage"        
    return render(request,'index.html',locals())


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
        
        









