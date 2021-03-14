from django import forms
from django.db.models import Q
from django.forms import ModelForm, Textarea, Select
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from customstaff.models import *
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django.core.exceptions import ValidationError
from django.contrib import messages
from datetime import *
# class UserRegisterForm(UserCreationForm):
# 	email = forms.EmailField()

# 	class Meta:
# 		model = User
# 		fields = [
# 			'username',
# 			'email',
# 			'password1',
# 			'password2',
# 		]
TIME_FORMAT = '%I:%M %p'
first = '1st'
second = '2nd'
third = '3rd'
forth = '4th'
fifth = '5th'
sixth = '6th'
seventh = '7th'
eighth = '8th'
ninth = '9th'
class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = [
			'image',
		]
class ProfileApproveForm(forms.ModelForm):
	# finalcomment = forms.CharField(required=False,label =  "Cancel reason", widget=forms.TextInput(attrs={'placeholder' : "Reason"}) )
	class Meta:
		model = LeaveApplication
		fields = [
			# 'firststatus',
			# 'secondstatus',
			# 'finalstatus'
		]


class TeachingStaffUpdateForm(forms.ModelForm):

	class Meta:
		model = TeachingStaffDetail
		fields = ['sickleave', 'casualleave']

class NonTeachingStaffUpdateForm(forms.ModelForm):

	class Meta:
		model = NonTeachingStaffDetail
		fields = ['sickleave', 'annualleave', 'compensatedleave']

	# def clean(self):
 #    	modify = self.cleaned_data['duration']
 #    	if obj.user.teachertimeofftype == sickleave:
 #    		sickleave = sickleave - modify

	# 	return super(NonTeachingStaffUpdateForm, self).clean()

class TeacherApplyForm(forms.ModelForm):
	
	startdate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'From Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	starttime = forms.TimeField(required=False, label= 'From Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class' : 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)

	enddate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'To Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	endtime = forms.TimeField(required=False ,label= 'To Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)
	# teachertimeofftype = forms.ChoiceField(required=False, choices = TEACHER_TIMEOFF_CHOICES)

	reason	= forms.CharField(required=True,
		widget=forms.Textarea(
			attrs={
				"cols" : 50,
				"rows" : 3
		}))	
	PERIOD_CHOICES = [
		# ("first" ,'1st'),
		# ("second", '2nd'),
		# ("third" ,'3rd'),
		# ("forth" ,'4th'),
		# ("fifth" ,'5th'),
		# ("sixth" ,'6th'),
		# ("seventh", '7th'),
		# ("eighth", '8th'),
		# ("ninth" ,'9th'),
		# ("allday", 'allday')

		(first ,'1st'),
		(second, '2nd'),
		(third ,'3rd'),
		(forth ,'4th'),
		(fifth ,'5th'),
		(sixth ,'6th'),
		(seventh, '7th'),
		(eighth, '8th'),
		(ninth ,'9th')
	]

	period = forms.MultipleChoiceField(required=False,choices = PERIOD_CHOICES)
	pickvp = forms.ModelChoiceField(required=False,label ="Choose VP",queryset = User.objects.filter(is_viceprincipal = True))

	class Meta:
		model = LeaveApplication
		fields = [
			'teachertimeofftype',
			'pickvp',
			'period',
			'startdate',
			'starttime',
			'enddate',
			'endtime',
			'reason'
			]
		widgets={
			'teachertimeofftype': Select(attrs={"onChange":"showDiv('hidden_div', this)"}),
		}

	# def __init__(self,*args, **kwargs):
	#     super(TeacherApplyForm, self).__init__(*args, **kwargs)
	#     self.fields['teachertimeofftype'].choices =  [('', '---Please select your color---')] + LeaveApplication.TEACHER_TIMEOFF_CHOICES

	def clean(self):
		startdate = self.cleaned_data.get('startdate')
		enddate = self.cleaned_data.get('enddate')
		starttime = self.cleaned_data.get('starttime')
		endtime = self.cleaned_data.get('endtime')
		if starttime != None and endtime != None:
			
			if startdate.day < enddate.day and startdate.month == enddate.month:
				print('111111111')
				
			elif startdate.month < enddate.month:
				print('22222222')
				return endtime
			elif startdate.year < enddate.year:
					return endtime
			elif startdate.month == enddate.month and startdate.day == enddate.day:
				if starttime.minute  >=  endtime.minute and starttime.hour  >=  endtime.hour:
					raise forms.ValidationError(("End date must be later than start date"))
				elif starttime.hour  >  endtime.hour:
					raise forms.ValidationError(("End date must be later than start date"))
			else:
				print('4444444444')
				raise forms.ValidationError(("End date must be later than start date"))
	
		elif starttime == None and endtime == None:
			if startdate.day <= enddate.day and startdate.month == enddate.month:
				print('5555555')
				return endtime
			elif startdate.month < enddate.month:
				print('666666666')
				return endtime
			elif startdate.year < enddate.year:
					return endtime
			else:
				print('7777777')
				raise forms.ValidationError(("End date must be later than start date"))
		else:
			raise forms.ValidationError(("End date must be later than start date"))
class NonTeacherApplyForm(forms.ModelForm):
	
	# date_range_picker = fields.DateRangeField(
	# 	input_formats=['%d/%m/%Y'],
	# 	widget=widgets.DateRangeWidget(
	# 		format='%d/%m/%Y'
	# 		)
	# )

	startdate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'From Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	starttime = forms.TimeField(required=False, label= 'From Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)

	enddate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'To Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	endtime = forms.TimeField(required=False, label= 'To Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)
	# nonteachertimeofftype = forms.CharField(required=False)

	
	reason	= forms.CharField(required=True,
		widget=forms.Textarea(
			attrs={
				"cols" : 50,
				"rows" : 3
		}))

	pickvp = forms.ModelChoiceField(required=False,label ="Please Select Vice-Principal",queryset = User.objects.filter(is_viceprincipal = True))
	pickmanager = forms.ModelChoiceField(required=False, label ="Please Select Supervisor(s)",queryset = User.objects.filter(Q(is_supervisor = True) | Q(is_viceprincipal = True)))
	
	PERIOD_CHOICES = [

		(first ,'1st'),
		(second, '2nd'),
		(third ,'3rd'),
		(forth ,'4th'),
		(fifth ,'5th'),
		(sixth ,'6th'),
		(seventh, '7th'),
		(eighth, '8th'),
		(ninth ,'9th')
	]

	period = forms.MultipleChoiceField(required=False,choices = PERIOD_CHOICES) 
	class Meta:
		model = LeaveApplication
		fields = [
			'nonteachertimeofftype',
			'pickvp',
			'pickmanager',
			'startdate',
			'starttime',
			'enddate',
			'endtime',
			'period',
			'reason',
			'file'
		]
		widgets={
				'nonteachertimeofftype': Select(attrs={
					"onload":"showDiv('hidden_div', this)",
					"onChange":"showDiv('hidden_div', this)"
					}),
			}

		
	def clean(self):
		startdate = self.cleaned_data.get('startdate')
		enddate = self.cleaned_data.get('enddate')
		starttime = self.cleaned_data.get('starttime')
		endtime = self.cleaned_data.get('endtime')
		if starttime != None and endtime != None:
			if startdate.day < enddate.day and startdate.month == enddate.month:
				print('111111111')
				# return endtime
			elif startdate.month < enddate.month:
				print('22222222')
				return endtime
			elif startdate.year < enddate.year:
				return endtime
			elif startdate.month == enddate.month and startdate.day == enddate.day:
				if starttime.minute  >=  endtime.minute and starttime.hour  >=  endtime.hour:
					raise forms.ValidationError(("End Time must be later than start Time"))
				elif starttime.hour  >  endtime.hour:
					raise forms.ValidationError(("End Time must be later than start Time"))
			else:
				print('4444444444')
				raise forms.ValidationError(("End date must be later than start date"))
			
		elif starttime == None and endtime == None:
			if startdate.day <= enddate.day and startdate.month == enddate.month:
				print('5555555')
				# return endtime
			elif startdate.month < enddate.month:
				print('666666666')
				# return endtime
			elif startdate.year < enddate.year :
				# return endtime
				print('666666666')
			else:
				print('7777777')
				raise forms.ValidationError(("End date must be later than start date"))
			
		else:
			raise forms.ValidationError(("End date must be later than start date"))
class GroupApplyForm(forms.ModelForm):
	
	startdate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'From Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	starttime = forms.TimeField(required=False, label= 'From Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)

	enddate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'To Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	endtime = forms.TimeField(required=False ,label= 'To Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)
	teachertimeofftype = forms.CharField(required=False)
	nonteachertimeofftype = forms.CharField(required=False)

	reason	= forms.CharField(required=True,
		widget=forms.Textarea(
			attrs={
				"cols" : 50,
				"rows" : 3
		}))
	PERIOD_CHOICES = [
		(first ,'1st'),
		(second, '2nd'),
		(third ,'3rd'),
		(forth ,'4th'),
		(fifth ,'5th'),
		(sixth ,'6th'),
		(seventh, '7th'),
		(eighth, '8th'),
		(ninth ,'9th'),
		# (allday, 'Whole Day')
	]

	period = forms.MultipleChoiceField(required=False,choices = PERIOD_CHOICES) 
	users = forms.ModelMultipleChoiceField(label ="Applying for: (Include yourself if applicable)",queryset = User.objects.exclude(Q(is_principal = True ) | Q(is_secretary = True)).order_by('username'),widget=forms.SelectMultiple(attrs={
						"onChange":"showSelectedValues(this)"
						})
					)	 
	class Meta:
		model = LeaveApplication
		fields = [
			'teachertimeofftype',
			"nonteachertimeofftype",
			"users",
			"officialtype",
			'startdate',
			'starttime',
			'enddate',
			'endtime',
			'period',
			'reason',
		]
	

	def clean(self):
		cleaned_data = super().clean()
		startdate = cleaned_data.get('startdate')
		enddate = cleaned_data.get('enddate')
		starttime = cleaned_data.get('starttime')
		endtime = cleaned_data.get('endtime')
		if starttime != None and endtime != None:
			if startdate.day < enddate.day and startdate.month == enddate.month:
				print('111111111')
				# return endtime
			elif startdate.month < enddate.month:
				print('22222222')
				# return endtime
			elif startdate.year < enddate.year:
				# return endtime
				print('22222222')
			elif startdate.month == enddate.month and startdate.day == enddate.day:
				if starttime.minute  >=  endtime.minute and starttime.hour  >=  endtime.hour:
					raise forms.ValidationError(("End Time must be later than start Time"))
				elif starttime.hour  >  endtime.hour:
					raise forms.ValidationError(("End Time must be later than start Time"))
			else:
				print('4444444444')
				raise forms.ValidationError(("End date must be later than start date"))
			
		elif starttime == None and endtime == None:
			if startdate.day <= enddate.day and startdate.month == enddate.month:
				print('5555555')
				return endtime
			elif startdate.month < enddate.month:
				print('666666666')
				return endtime
			elif startdate.year < enddate.year :
				return endtime
			else:
				print('7777777')
				raise forms.ValidationError(("End date must be later than start date"))
			
		else:
			raise forms.ValidationError(("End date must be later than start date"))

class ApplyForForm(forms.ModelForm):
	
	startdate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'From Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	starttime = forms.TimeField(required=False, label= 'From Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)

	enddate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'To Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	endtime = forms.TimeField(required=False ,label= 'To Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)
	teachertimeofftype = forms.CharField(required=False)
	nonteachertimeofftype = forms.CharField(required=False)
	firststatus = forms.CharField(required=False)
	secondstatus = forms.CharField(required=False)
	finalstatus = forms.CharField(required=False)

	reason	= forms.CharField(required=True,
		widget=forms.Textarea(
			attrs={
				"cols" : 50,
				"rows" : 3
		}))
	PERIOD_CHOICES = [
		(first ,'1st'),
		(second, '2nd'),
		(third ,'3rd'),
		(forth ,'4th'),
		(fifth ,'5th'),
		(sixth ,'6th'),
		(seventh, '7th'),
		(eighth, '8th'),
		(ninth ,'9th'),
		# (allday, 'Whole Day')
	]

	period = forms.MultipleChoiceField(required=False,choices = PERIOD_CHOICES)		 
	class Meta:
		model = LeaveApplication
		fields = [
			'teachertimeofftype',
			"nonteachertimeofftype",
			'emergencytype',
			"firststatus",
			"secondstatus",
			'finalstatus',
			'startdate',
			'starttime',
			'enddate',
			'endtime',
			'period',
			'reason',
			'file'
		]

	def clean(self):
		startdate = self.cleaned_data.get('startdate')
		enddate = self.cleaned_data.get('enddate')
		starttime = self.cleaned_data.get('starttime')
		endtime = self.cleaned_data.get('endtime')
		if starttime != None and endtime != None:
			
			if startdate.day < enddate.day and startdate.month == enddate.month:
				print('111111111')
				
			elif startdate.month < enddate.month:
				print('22222222')
				return endtime
			elif startdate.month == enddate.month and startdate.day == enddate.day:
				if starttime.minute  >=  endtime.minute and starttime.hour  >=  endtime.hour:
					raise forms.ValidationError(("End Time must be later than start Time"))
				elif starttime.hour  >  endtime.hour:
					raise forms.ValidationError(("End Time must be later than start Time"))
			elif startdate.year < enddate.year:
					return endtime
			else:
				print('4444444444')
				raise forms.ValidationError(("End date must be later than start date"))
	
		elif starttime == None and endtime == None:
			if startdate.day <= enddate.day and startdate.month == enddate.month:
				print('5555555')
				return endtime
			elif startdate.month < enddate.month:
				print('666666666')
				return endtime
			elif startdate.year < enddate.year:
					return endtime
			else:
				print('7777777')
				raise forms.ValidationError(("End date must be later than start date"))
		else:
			raise forms.ValidationError(("End date must be later than start date"))

class ApplyForForm2(forms.ModelForm):
	
	startdate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'From Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	starttime = forms.TimeField(required=False, label= 'From Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)

	enddate = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'To Date',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'start-time',
			 'placeholder' : "Pick a Date!",
			 })
			)
						
	endtime = forms.TimeField(required=False ,label= 'To Time',widget=TimePickerInput(
		options={"stepping" : 5,
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'class': 'starttime',
			 'placeholder' : "Pick a Time!",
			 })
			)
	teachertimeofftype = forms.CharField(required=False)
	nonteachertimeofftype = forms.CharField(required=False)
	firststatus = forms.CharField(required=False)
	secondstatus = forms.CharField(required=False)
	finalstatus = forms.CharField(required=False)

	reason	= forms.CharField(required=True,
		widget=forms.Textarea(
			attrs={
				"cols" : 50,
				"rows" : 3
		}))
	PERIOD_CHOICES = [
		(first ,'1st'),
		(second, '2nd'),
		(third ,'3rd'),
		(forth ,'4th'),
		(fifth ,'5th'),
		(sixth ,'6th'),
		(seventh, '7th'),
		(eighth, '8th'),
		(ninth ,'9th'),
		# (allday, 'Whole Day')
	]

	period = forms.MultipleChoiceField(required=False,choices = PERIOD_CHOICES)	 
	class Meta:
		model = LeaveApplication
		fields = [
			'teachertimeofftype',
			"nonteachertimeofftype",
			'alltimeofftype',
			"firststatus",
			"secondstatus",
			'finalstatus',
			'startdate',
			'starttime',
			'enddate',
			'endtime',
			'period',
			'reason',
			'file'
		]

	def clean(self):
		startdate = self.cleaned_data.get('startdate')
		enddate = self.cleaned_data.get('enddate')
		starttime = self.cleaned_data.get('starttime')
		endtime = self.cleaned_data.get('endtime')
		if starttime != None and endtime != None:
			
			if startdate.day < enddate.day and startdate.month == enddate.month:
				print('111111111')
				
			elif startdate.month < enddate.month:
				print('22222222')
				return endtime
			elif startdate.year < enddate.year:
					return endtime
			elif startdate.month == enddate.month and startdate.day == enddate.day:
				if starttime.minute  >=  endtime.minute and starttime.hour  >=  endtime.hour:
					raise forms.ValidationError(("End Time must be later than start Time"))
				elif starttime.hour  >  endtime.hour:
					raise forms.ValidationError(("End Time must be later than start Time"))
			else:
				print('4444444444')
				raise forms.ValidationError(("End date must be later than start date"))
	
		elif starttime == None and endtime == None:
			if startdate.day <= enddate.day and startdate.month == enddate.month:
				print('5555555')
				return endtime
			elif startdate.month < enddate.month:
				print('666666666')
				return endtime
			elif startdate.year < enddate.year:
					return endtime
			else:
				print('7777777')
				raise forms.ValidationError(("End date must be later than start date"))
		else:
			raise forms.ValidationError(("End date must be later than start date"))


class PickerForm(forms.ModelForm):
	pickuser = forms.ModelMultipleChoiceField(label ="Applying for",queryset = User.objects.exclude(Q(is_principal = True ) | Q(is_secretary = True)),widget=forms.SelectMultiple(attrs={
						"onChange":"showSelectedValues(this)"
						})
					)

	class Meta:
			model = Picker
			fields = [
				'pickuser'
			]
			
class UpdateFileForm(forms.ModelForm):
	# firststatus = forms.
	class Meta:
			model = LeaveApplication
			fields = [
				'file',
				# 'firststatus'
			]
class FirstValidate(forms.ModelForm):

	class Meta:
		model = LeaveApplication
		fields = [
			'firststatus',
			'firstcomment'
		]

class SecondValidate(forms.ModelForm):


	pickvp = forms.ModelChoiceField(required=False,label ="Assigned Vice Principal",queryset = User.objects.filter(is_viceprincipal = True))

	class Meta:
		model = LeaveApplication
		fields = [
			'pickvp',
			'secondstatus',
			'secondcomment'
		]

class SecretaryValidate(forms.ModelForm):
	finalduration = forms.DecimalField(required=False,label = "Modified duration (Optional)", widget=forms.TextInput(attrs={'placeholder' : "Hour for OT, Days for Leave"}) )

	class Meta:
		model = LeaveApplication
		fields = [
			'nonteacherchangetimeofftype',
			'teacherchangetimeofftype',
			'secretarystatus',
			'finalcomment',
			'finalduration',
			'attachmentrequired',
			'attachmentreceived'
		]

class FinalValidate(forms.ModelForm):
	finalduration = forms.DecimalField(required=False,label = "Modified duration (Optional)", widget=forms.TextInput(attrs={'placeholder' : "Hour for OT, Days for Leave"}) )

	class Meta:
		model = LeaveApplication
		fields = [
			'nonteacherchangetimeofftype',
			'teacherchangetimeofftype',
			'finalstatus',
			'finalcomment',
			'finalduration'
			
		]

class IncrementAllForm(forms.ModelForm):
	created_at = forms.DateField(input_formats=('%d/%m/%Y', ),label= 'Date Added',widget=DatePickerInput(
		format='%d/%m/%Y',
		options={
				"toolbarPlacement" : 'top',
				},
		attrs={
			 'placeholder' : "Pick a Date!",
			 })
			)
	class Meta:
			model = IncrementAll
			fields = [
				'created_at'
			]

class DocumentForm(forms.ModelForm):
	class Meta:
		model = LeaveApplication
		fields = [
			'attachmentrequired',
			'attachmentreceived',
			'secretarycomment'
		]
class CalendarForm(forms.ModelForm):
	class Meta:
		model = LeaveApplication
		fields = [
			'calendarcheck',
			'secretarycomment'
		]


class CancelForm(forms.ModelForm):
	finalcomment = forms.CharField(required=False,label =  "Cancel reason", widget=forms.TextInput(attrs={'placeholder' : "Reason"}) )
	class Meta:
		model = LeaveApplication
		fields = [
			'finalcomment',
		]
class UserCancelForm(forms.ModelForm):
	reason = forms.CharField(required=True,label =  "Cancel reason", widget=forms.TextInput(attrs={'placeholder' : "Reason"}) )
	class Meta:
		model = LeaveApplication
		fields = [
			'reason',
		]
