from django.db.models import Sum
from rest_framework import serializers
from base.serializers import ErpEmployeeSerializer
from .models import Project, LandSite, Task, Subtask, SubtaskBasicInfo, SubtaskDailyProgress
from datetime import timedelta, date
import math


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class SubtaskBasicInfoSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['task_id'] = obj.subtask.task.id
        representation['task'] = obj.subtask.task.name
        representation['subtask_id'] = obj.subtask.id
        representation['subtask'] = obj.subtask.name
        return representation

    class Meta: 
        model = SubtaskBasicInfo
        exclude = ['created_at', 'updated_at']
        extra_kwargs = {
            'subtask': {'write_only': True}, 
            'land_site': {'write_only': True},
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }


class LandSiteSerializer(serializers.ModelSerializer):
    subtask_basic_infos = SubtaskBasicInfoSerializer(many=True, read_only=True)

    class Meta:
        model = LandSite
        exclude = ['created_at', 'updated_at'] 
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }


class LandSiteOverviewSerializer(serializers.ModelSerializer):
    land_site_overview = serializers.SerializerMethodField(read_only=True)

    def get_land_site_overview(self, obj):
        subatsk_basic_infos = SubtaskBasicInfo.objects.filter(land_site=obj.id)
        overall_blcd = None
        overall_td = None
        for subatsk_basic_info in subatsk_basic_infos:
            blcd = subatsk_basic_info.base_line_completion_date
            if not overall_blcd:
                overall_blcd = blcd
            else:
                if blcd and blcd > overall_blcd:
                    overall_blcd = blcd
            
            subtask_all_daily_progress = SubtaskDailyProgress.objects.filter(subtask_basic_info=subatsk_basic_info.id)
            number_of_subtask_all_daily_progress = len(subtask_all_daily_progress)
            
            if number_of_subtask_all_daily_progress == 0:
                sum_today_progress = 0
            else:
                sum_today_progress = subtask_all_daily_progress.aggregate(Sum('today_progress'))['today_progress__sum']
            balance_qty = subatsk_basic_info.bom - sum_today_progress
            
            if number_of_subtask_all_daily_progress == 0:
                avg_progress = 0 
            elif number_of_subtask_all_daily_progress < 3:
                avg_progress = sum_today_progress / number_of_subtask_all_daily_progress
            else:            
                recent_three_subtask_daily_progress = subtask_all_daily_progress[(number_of_subtask_all_daily_progress-3):]            
                today_progress_sum = 0
                for each_subtask_daily_progress in recent_three_subtask_daily_progress:
                    today_progress_sum += each_subtask_daily_progress.today_progress            
                avg_progress = today_progress_sum / 3 
            
            if avg_progress == 0: 
                target_date = None   
            else: 
                target_date = (date.today() + timedelta(days=math.ceil(balance_qty / avg_progress)))

            if not overall_td:
                overall_td = target_date
            else:
                if target_date and target_date > overall_td:
                    overall_td = target_date
        
        if not overall_td:
            overall_td = overall_blcd

        return {
            'overall_base_line_completion_date': overall_blcd and overall_blcd.strftime('%d-%m-%Y'),
            'overall_target_date': overall_td and overall_td.strftime('%d-%m-%Y')
        }

    class Meta:
        model = LandSite
        exclude = ['created_at', 'updated_at'] 
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }


class ProjectDetailsSerializer(serializers.ModelSerializer):
    project_manager = ErpEmployeeSerializer()
    site_construction_manager = ErpEmployeeSerializer()
    land_sites = LandSiteOverviewSerializer(source='landsite_set', many=True, read_only=True)
    rm_of_project_manager = serializers.SerializerMethodField()
    rm_of_site_construction_manager = serializers.SerializerMethodField()

    def get_rm_of_project_manager(self, obj):
        if obj.project_manager:
            return ErpEmployeeSerializer(obj.project_manager.manager).data
        else:
            return None

    def get_rm_of_site_construction_manager(self, obj):
        if obj.site_construction_manager:
            return ErpEmployeeSerializer(obj.site_construction_manager.manager).data
        else:
            return None

    class Meta:
        model = Project
        fields = '__all__'


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'
        extra_kwargs = {
            'task': {'write_only': True},
        }


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(source='subtask_set', many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'


class SubtaskDailyProgressSerializer(serializers.ModelSerializer):    
    class Meta:
        model = SubtaskDailyProgress 
        fields = '__all__'


class SubtaskDailyProgressDPRSerializer(serializers.ModelSerializer):
    dpr_date = serializers.SerializerMethodField()
    updated_by = ErpEmployeeSerializer()
    
    def get_dpr_date(self, obj):
        return obj.dpr_date.strftime('%d-%m-%Y')
    
    class Meta:
        model = SubtaskDailyProgress 
        exclude = ['subtask_basic_info']


class SubtaskBasicInfoDPRSerializer(serializers.ModelSerializer):
    task = serializers.CharField(source='subtask.task.name')
    subtask = serializers.CharField(source='subtask.name')
    base_line_completion_date = serializers.SerializerMethodField()
    report = serializers.SerializerMethodField() 

    def get_base_line_completion_date(self, obj):
        return obj.base_line_completion_date.strftime('%d-%m-%Y')

    def get_report(self, obj):
        date = self.context.get('date')
        permission = self.context.get('permission') 
        subtask_daily_progress = SubtaskDailyProgress.objects.filter(subtask_basic_info=obj.id, dpr_date=date)
        
        if subtask_daily_progress.exists():
            is_temporary_subtask_daily_progress = False
            subtask_daily_progress = subtask_daily_progress[0]
        else:
            if permission == 'site construction manager' and not self.context.get('is_completed'):
                is_temporary_subtask_daily_progress = True
                subtask_daily_progress = SubtaskDailyProgress(dpr_date=date, subtask_basic_info=obj)

        if subtask_daily_progress:
            subtask_all_daily_progress = SubtaskDailyProgress.objects.filter(subtask_basic_info=obj.id, dpr_date__lte=date).order_by('dpr_date')
            number_of_subtask_all_daily_progress = len(subtask_all_daily_progress)
            if number_of_subtask_all_daily_progress != 0 and is_temporary_subtask_daily_progress:
                subtask_daily_progress.status = subtask_all_daily_progress.last().status
            
            if number_of_subtask_all_daily_progress == 0:
                previous_progress = 0
            else:
                sum_today_progress = subtask_all_daily_progress.aggregate(Sum('today_progress')) 
                previous_progress = sum_today_progress['today_progress__sum'] - subtask_daily_progress.today_progress
            
            total_completed_qty = previous_progress + subtask_daily_progress.today_progress
            balance_qty = obj.bom - total_completed_qty
            percentage_completion = round(total_completed_qty / obj.bom * 100, 2)

            if number_of_subtask_all_daily_progress == 0:
                avg_progress = 0 
            elif number_of_subtask_all_daily_progress < 3:
                avg_progress = sum_today_progress['today_progress__sum'] / number_of_subtask_all_daily_progress
            else:            
                recent_three_subtask_daily_progress = subtask_all_daily_progress[(number_of_subtask_all_daily_progress-3):]            
                today_progress_sum = 0
                for each_subtask_daily_progress in recent_three_subtask_daily_progress:
                    today_progress_sum += each_subtask_daily_progress.today_progress            
                avg_progress = today_progress_sum / 3            
            
            if avg_progress == 0: 
                target_date = obj.base_line_completion_date.strftime('%d-%m-%Y')
            else: 
                target_date = (date + timedelta(days=math.ceil(balance_qty / avg_progress))).strftime('%d-%m-%Y')
            
            subtask_daily_progress_serializer = SubtaskDailyProgressDPRSerializer(subtask_daily_progress)
            return {
                'subtask_daily_progress': subtask_daily_progress_serializer.data,
                'previous_progress': previous_progress,
                'total_completed_qty': total_completed_qty, 
                'balance_qty': balance_qty,
                'target_date': target_date,
                'percentage_completion': percentage_completion 
            }
        else:
            return None
 
    class Meta: 
        model = SubtaskBasicInfo
        fields = ['id', 'task', 'subtask', 'uom', 'bom', 'base_line_completion_date', 'report']


class SubtaskDailyProgressTTVSerializer(serializers.ModelSerializer):
    dpr_date = serializers.SerializerMethodField()
    
    def get_dpr_date(self, obj):
        return obj.dpr_date.strftime('%d-%m-%Y')
    
    class Meta:
        model = SubtaskDailyProgress
        fields = ['dpr_date', 'today_progress']


class SubtaskBasicInfoTTVSerializer(serializers.ModelSerializer):
    task = serializers.CharField(source='subtask.task.name')
    subtask = serializers.CharField(source='subtask.name')
    subtask_daily_progress_summary = serializers.SerializerMethodField()

    def get_subtask_daily_progress_summary(self, obj):
        date_from = self.context.get('date_from')
        date_to = self.context.get('date_to')
        subtask_daily_progress = SubtaskDailyProgress.objects.filter(subtask_basic_info=obj.id, dpr_date__gte=date_from, dpr_date__lte=date_to).order_by('dpr_date')
        serializer = SubtaskDailyProgressTTVSerializer(subtask_daily_progress, many=True)
        number_of_subtask_daily_progress = len(subtask_daily_progress)
        if number_of_subtask_daily_progress > 0:
            average_today_progress = round(subtask_daily_progress.aggregate(Sum('today_progress'))['today_progress__sum'] / number_of_subtask_daily_progress, 2)
        else:
            average_today_progress = 0
        return {
            'subtask_all_daily_progress': serializer.data,
            'average_today_progress': average_today_progress
        }

    class Meta:
        model = SubtaskBasicInfo
        fields = ['id', 'task', 'subtask', 'uom', 'subtask_daily_progress_summary']
