# coding: utf-8
from app.models import MonitorDatas,Assets
from rest_framework import serializers


class AssetsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assets
        fields = '__all__'
        


class MonitorDatasSerializer(serializers.ModelSerializer):
#    hostid = AssetsSerializer(many=True)
    class Meta:
        model = MonitorDatas
        #fields = '__all__'
        fields = ('hostid','cpu_useage','memory_useage','disk_useage','run_status','date')

        