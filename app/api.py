# coding: utf-8
from app.models import  Assets, MonitorDatas,MysqlInfo
from app.serializer import MonitorDatasSerializer,AssetsSerializer,MysqlInfoSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status



@api_view(['GET','POST','DELETE'])
def assets_list(request):
  
    if request.method == 'GET':
        assets_data = Assets.objects.all()
        serializer = AssetsSerializer(assets_data,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        result = {"msg":"error","code":status.HTTP_400_BAD_REQUEST,"status":"False"}
        ip = request.data['ipaddr']
        check_ip = Assets.objects.filter(ipaddr=ip)
        if check_ip:
            result["msg"] = "主机已存在"
            result["status"] = "False"
            result["code"] = status.HTTP_201_CREATED
        else:         
            serializer = AssetsSerializer(data=request.data)
            if serializer.is_valid():                        
                serializer.save()
                result['code'] = status.HTTP_201_CREATED
                result["msg"] = "添加成功"
                result["status"] = "True"                    
        return Response(result)        

    if request.method == 'DELETE':
        hid = request.data['hid']
        Assets.objects.filter(id=hid).delete()
        result["msg"] = "删除成功"
        result["code"] = status.HTTP_201_CREATED
        result["status"] = "True"
        return Response(result)
            
    
    
      
@api_view(['GET','POST'])
def data_list(request):    
    if request.method == 'GET':
        mdata = MonitorDatas.objects.all()
        serializer = MonitorDatasSerializer(mdata,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        result = {"msg":"error","code":status.HTTP_400_BAD_REQUEST,"status":"False"}
        req_data = request.data
        if req_data['ip']:
            host_id = Assets.objects.filter(ipaddr=req_data['ip'])[0].id
            req_data.pop('ip')
            req_data['hostid'] =  host_id                  
            serializer = MonitorDatasSerializer(data=req_data)
            if serializer.is_valid():
                serializer.save()
                result['msg'] = "成功"
                result["code"] = status.HTTP_201_CREATED
                result["status"] = "True"
        else:
            result["msg"] = "失败"            
        return Response(result)
                
@api_view(['GET','POST'])
def dbstat_list(request):
    if request.method == 'GET':
        mdata = MysqlInfo.objects.all()
        serializer = MysqlInfoSerializer(mdata,many=True)
        return Response(serializer.data)    


    if request.method == 'POST':
        result = {"msg":"error","code":status.HTTP_400_BAD_REQUEST,"status":"False"}
        req_data = request.data
        """
                       判断该主机是否有数据库实例
        """
        if req_data['ip'] and req_data['alive']:
            host_id = Assets.objects.filter(ipaddr=req_data['ip'])[0].id
            req_data.pop('ip')
            req_data['hostid'] =  host_id                          
            serializer = MysqlInfoSerializer(data=req_data)
            if serializer.is_valid():
                serializer.save()
                result['msg'] = "成功"
                result["code"] = status.HTTP_201_CREATED
                result["status"] = "True"                
        else:
            result['msg'] = "失败"
        return Response(result) 


