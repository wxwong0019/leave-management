import django_filters
from django import forms

from django_filters import *
from django_filters.widgets import *
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from datetime import *

from customstaff.models import *

class teacherLeaveApplicationFilter(django_filters.FilterSet):
	created_at = DateFilter(label= 'Date Created', lookup_expr='gte')
	class Meta:
		model = LeaveApplication
		fields = [
		'teachertimeofftype',
		'created_at'
		]


class nonteacherLeaveApplicationFilter(django_filters.FilterSet):
	created_at = DateFilter(label= 'Date Created', lookup_expr='gte')

	class Meta:
		model = LeaveApplication
		fields = [
		'nonteachertimeofftype',
		'created_at'
		]

class LeaveApplicationFilter(django_filters.FilterSet):
	created_at = DateFilter(label= 'Date Created', lookup_expr='gte')
	startdate = DateFilter(input_formats=('%d/%m/%Y'),label= 'Start Date', lookup_expr='gte', widget=MonthPickerInput(
            format='%d/%m/%Y',
            attrs={
                'class': 'datepicker'
            }
        ))
	

	class Meta:
		model = LeaveApplication
		fields = [
		
		'alltimeofftype',
		'stafftype',
		'user',
		'created_at',
		'startdate',
		'attachmentreceived',
		'attachmentrequired'
		]