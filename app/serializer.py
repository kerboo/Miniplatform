# coding: utf-8
from app.models import MonitorDatas,Assets,MysqlInfo
from rest_framework import serializers


class AssetsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assets
        fields = '__all__'
        


class MonitorDatasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorDatas
        #fields = '__all__'
        fields = ('hostid','cpu_useage','memory_useage','disk_useage','run_status','date')


class MysqlInfoSerializer(serializers.ModelSerializer): 
    class Meta:
        model =  MysqlInfo
        fields = ('hostid','alive','connections','qps_useage','tps_useage','slow_query','buffer_useage','buffer_hitrate','date')  
        
         