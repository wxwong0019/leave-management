from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from datetime import *
from django.core.exceptions import ValidationError
from django.contrib.auth import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.core.mail import send_mail
from .filters import *
from .forms import *
from customstaff.models import *
from django.http import HttpResponse 
import csv
import decimal
from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('/login/')
    return response


def logout_view(request):
    logout(request)
    return redirect("login")



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })

@login_required
def profile(request):
	useri = request.user


	test = LeaveApplication.objects.filter(Q(user=request.user) | Q(users__in=[request.user]))
	# groupapplieduser = LeaveApplication.objects.filter(users__in=[request.user])
	if request.user.is_secretary:
		userid = SecretaryDetail.objects.get(user = request.user)
	elif request.user.is_nonteacher and not request.user.is_supervisor:
		userid = NonTeachingStaffDetail.objects.get(user = request.user)
	elif request.user.is_supervisor:
		userid = SupervisorDetail.objects.get(user = request.user)
	elif request.user.is_viceprincipal:
		userid = VicePrincipalDetail.objects.get(user = request.user)
	else:
		userid = TeachingStaffDetail.objects.get(user = request.user)
	
	if request.user.is_nonteacher:
		myFilter = nonteacherLeaveApplicationFilter(request.GET, queryset=test)
		applicant = myFilter.qs
	else:
		myFilter = teacherLeaveApplicationFilter(request.GET, queryset=test)
		applicant = myFilter.qs
	
	context = {
		'applicant':test,
		'userid':userid,
		'myFilter' : myFilter,
		'user' : useri,
		# 'groupapplieduser' : groupapplieduser
	}
	return render(request, 'users/profile.html', context)


def profiledetail(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)
	if obj.groupapplystatus:
		userid= obj.appliedby
	else:
		userid=obj.user

	if userid.is_secretary:
		applicant = SecretaryDetail.objects.get(user = userid)
	elif userid.is_nonteacher:
		applicant = NonTeachingStaffDetail.objects.get(user = userid)
	elif userid.is_supervisor:
		applicant = SupervisorDetail.objects.get(user = userid)
	elif userid.is_viceprincipal:
		applicant = VicePrincipalDetail.objects.get(user = userid)
	else:
		applicant = TeachingStaffDetail.objects.get(user = userid)

	

	if request.method == 'POST':
		if request.user.is_nonteacher:
			form = NonTeacherApplyForm(request.POST, instance=obj)
			print("nonteacher")
		else:
			form = TeacherApplyForm(request.POST, instance=obj)	
			print("teacher")

		u_form = UserCancelForm(request.POST, instance=obj)
		
		if 'modify' in request.POST and form.is_valid() :
			form.save()
			# p = pickform.save(commit=False)
			obj.startdate = form.cleaned_data.get('startdate')
			obj.enddate = form.cleaned_data.get('enddate')
			obj.starttime = form.cleaned_data.get('starttime')
			obj.endtime = form.cleaned_data.get('endtime')
			obj.reason = form.cleaned_data.get('reason')
			obj.pickvp = form.cleaned_data.get('pickvp')
			obj.pickmanager = form.cleaned_data.get('pickmanager')
			user = request.user
			

			if request.user.is_nonteacher:

				#///////////////////////
				superv = SupervisorDetail.objects.filter(user__username=request.user.NonTeachingStaffDetail.supervisor)
				viceprincipal = VicePrincipalDetail.objects.filter(user__username=request.user.NonTeachingStaffDetail.viceprincipal)

				if obj.pickmanager == None and not user.is_supervisor and superv!=None and not viceprincipal:
					for stuff in superv:
						obj.pickmanager = User.objects.get(username = stuff.user)
														
				elif obj.pickmanager == None and not user.is_supervisor and not superv and viceprincipal !=None:
					for stuff in viceprincipal:
						pickvp = User.objects.get(username = stuff.user)
				elif user.is_supervisor:
					obj.pickmanager = None
					#//////////////////
				obj.nonteachertimeofftype = form.cleaned_data.get('nonteachertimeofftype')
				obj.alltimeofftype = obj.nonteachertimeofftype
					
				
			else:
				obj.teachertimeofftype = form.cleaned_data.get('teachertimeofftype')
				obj.alltimeofftype = obj.teachertimeofftype
			obj.period = form.cleaned_data.get('period')
			
			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(obj.startdate), date_format)
			end_date = datetime.datetime.strptime(str(obj.enddate), date_format)

			if obj.starttime == None and obj.endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif obj.starttime != None and obj.endtime != None:
				start_time = obj.starttime.hour + obj.starttime.minute/60
				end_time = obj.endtime.hour + obj.endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/8
				hr = (end_date - start_date).days*24 + end_time-start_time
	
			if obj.alltimeofftype == 'Overtime':
				obj.duration = decimal.Decimal(hr) * applicant.ratio
			elif obj.alltimeofftype == 'Overtime Compensatory Leave':
				obj.duration = decimal.Decimal(hr)
			else:
				obj.duration = my_round(dur)
						
			obj.save()
			messages.success(request, f'Modified!')
			return redirect('profile')	
		elif u_form.is_valid() and 'cancel' in request.POST:
			if obj.finalstatus == "Pending" and obj.secondstatus == "Pending" and obj.firststatus == "Pending":

				obj.firststatus = "Canceled"
				obj.secondstatus = "Canceled"
				obj.finalstatus = "Canceled"
				u_form.save()
				obj.save()
				messages.success(request, f'Success')
				return redirect('profile')	
	else:
		u_form = UserCancelForm(instance=obj)
		if request.user.is_nonteacher:
			form = NonTeacherApplyForm( instance=obj)
		else:
			form = TeacherApplyForm( instance=obj)
	context = {
		'obj' : obj,
		'u_form' : u_form,
		'applicant' :applicant,
		'form' : form
	}
	return render(request, 'users/profiledetail.html', context)

def profileapprove(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)
	if request.method == 'POST':	
		u_form = ProfileApproveForm(request.POST,request.FILES)
								# instance=request.user)
		
		if u_form.is_valid():
			obj.firststatus = 'Approved'
			obj.secondstatus = 'Approved'
			obj.secretarystatus = 'Pending'
			obj.finalstatus = 'Pending'
			# u_form.save()
			obj.save()
			messages.success(request, f'Success')
			return redirect('profile')
	
	else:
		u_form = ProfileApproveForm()


		context = {
			'obj' : obj
		}
		return render(request, 'users/profileapprove.html', context)

@login_required
def login_success(request):
	"""
	Redirects users based on whether they are in the admins group
	"""
	if request.user.type == User.Types.NONTEACHINGSTAFF and request.user.type != User.Types.SECRETARY:
		# user is an admin
		messages.success(request, f'Welcome')
		return redirect("nonteacherapply")
	elif request.user.type == User.Types.SECRETARY:
		messages.success(request, f'Welcome')
		return redirect("secretarylistview")
	elif request.user.type == User.Types.SUPERVISOR and request.user.is_teacher:
		# user is an admin
		messages.success(request, f'Welcome')
		return redirect("teacherapply")
	elif request.user.type == User.Types.SUPERVISOR and request.user.is_nonteacher:
		# user is an admin
		messages.success(request, f'Welcome')
		return redirect("nonteacherapply")
	elif request.user.type == User.Types.VICEPRINCIPAL:
		# user is an admin
		messages.success(request, f'Welcome')
		return redirect("vplistview")
	elif request.user.type == User.Types.PRINCIPAL:
		# user is an admin
		messages.success(request, f'Welcome')
		return redirect("plistview")
	else:
		messages.success(request, f'Welcome')
		return redirect("teacherapply")

@login_required
def nonteacherapply(request):
	if request.user.is_secretary:
		userid = SecretaryDetail.objects.get(user = request.user)
	elif request.user.is_supervisor and request.user.is_nonteacher:
		userid = SupervisorDetail.objects.get(user = request.user)
	else:
		userid = NonTeachingStaffDetail.objects.get(user = request.user)

	if request.method == 'POST':
		form = NonTeacherApplyForm(request.POST, request.FILES)
		
		if form.is_valid():


			a_form = form.save(commit=False)
			user = request.user
			startdate = form.cleaned_data.get('startdate')
			enddate = form.cleaned_data.get('enddate')
			starttime = form.cleaned_data.get('starttime')
			endtime = form.cleaned_data.get('endtime')
			reason = form.cleaned_data.get('reason')
			nonteachertimeofftype = form.cleaned_data.get('nonteachertimeofftype')
			pickmanager = form.cleaned_data.get('pickmanager')
			pickvp = form.cleaned_data.get('pickvp')
			period = form.cleaned_data.get('period')
			superv = SupervisorDetail.objects.filter(user__username=request.user.NonTeachingStaffDetail.supervisor)
			viceprincipal = VicePrincipalDetail.objects.filter(user__username=request.user.NonTeachingStaffDetail.viceprincipal)
			period_list = "";
			for stuff in period:
				period_list+= stuff + ", ";

			if pickmanager == None and not user.is_supervisor and superv!=None and not viceprincipal:
				for stuff in superv:
					pickmanager = User.objects.get(username = stuff.user)
					print("pickmanagersafsafsfw")
					print(pickmanager)
					send_mail(
					'Leave Application Confirmation' ,
					'Hello '+pickmanager.username+ '. There is an application needs your attention. Please login and check under Manage Pending Application http://a.kachi.edu.hk/managerlistview/',
					'test@gmail.com',
					[pickmanager.email],
					)											
			elif pickmanager == None and not user.is_supervisor and not superv and viceprincipal !=None:
				
				for stuff in viceprincipal:
					pickvp = User.objects.get(username = stuff.user)
					print("pickmanagersafsafsfw")
					print(pickvp)
					send_mail(
					'Leave Application Confirmation' ,
					'Hello '+pickvp.username+ '. There is an application needs your attention. Please login and check under Manage Pending Application http://a.kachi.edu.hk/vplistview/',
					'test@gmail.com',
					[pickvp.email],
					)	

			elif pickmanager != None and not user.is_supervisor and not viceprincipal:
				send_mail(
				'Leave Application Confirmation' ,
				'Hello '+pickmanager.username+ '. There is an application needs your attention. Please login and check under Manage Pending Application http://a.kachi.edu.hk/managerlistview/',
				'test@gmail.com',
				[pickmanager.email],
				)
			elif pickmanager != None and not user.is_supervisor and not superv:
				send_mail(
				'Leave Application Confirmation' ,
				'Hello '+pickmanager.username+ '. There is an application needs your attention. Please login and check under Manage Pending Application http://a.kachi.edu.hk/vplistview/',
				'test@gmail.com',
				[pickmanager.email],
				)
			elif user.is_supervisor:
				pickmanager = None
			# print("Picked manager is "+ str(pickmanager))
			# pickvp = form.cleaned_data.get('pickvp')
			stafftype = "Nonteacher"
			
			template = render_to_string('users/email_staffapply.html', {
				'username':request.user.username,
				'type':nonteachertimeofftype,
				'startdate':startdate,
				'starttime':starttime,
				'endtime':endtime,
				'enddate':enddate,
				'period':period_list,
				'reason':reason
				})
			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(startdate), date_format)
			end_date = datetime.datetime.strptime(str(enddate), date_format)
			# start_date = startdate.day
			# end_date = enddate.day
			

			if starttime == None and endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif starttime != None and endtime != None:
				start_time = starttime.hour + starttime.minute/60
				end_time = endtime.hour + endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/8
				hr = (end_date - start_date).days*24 + end_time-start_time
			
			if nonteachertimeofftype == 'Overtime':
				duration = decimal.Decimal(hr) * userid.ratio
			elif nonteachertimeofftype == 'Overtime Compensatory Leave':
				duration = decimal.Decimal(hr)
			else:
				duration = my_round(dur)
				

			a_form = LeaveApplication.objects.create(startdate=startdate, enddate=enddate, starttime=starttime, endtime=endtime, nonteachertimeofftype=nonteachertimeofftype, alltimeofftype=nonteachertimeofftype,reason=reason, user=user, stafftype=stafftype, pickvp=pickvp, pickmanager=pickmanager, duration=duration, period = period)
			a_form.save()			
			form.save_m2m()
			messages.success(request, f'Successfully Applied')
			send_mail(
				'Leave Application Confirmation' ,
				template,
				'test@gmail.com',
				[request.user.email],
				)
			
			return redirect('success')
	else:
		form = NonTeacherApplyForm()
		
	return render(request, "users/apply.html", {'form': form, 'userid':userid})

@login_required
def teacherapply(request):
	if request.user.is_supervisor and request.user.is_teacher:
		userid = SupervisorDetail.objects.get(user = request.user)
		firststatus = "Approved"
		secondstatus = "Pending"
	elif request.user.is_viceprincipal:
		userid = VicePrincipalDetail.objects.get(user = request.user)
		firststatus = "Approved"
		secondstatus = "Approved"
	elif request.user.is_teacher:
		userid = TeachingStaffDetail.objects.get(user = request.user)
		firststatus = "Approved"
		secondstatus = "Pending"
	
	if request.method == 'POST':
		form = TeacherApplyForm(request.POST)
		print(request.POST['startdate'])
		if form.is_valid():

			a_form = form.save(commit=False)
			user = request.user
			startdate = form.cleaned_data.get('startdate')
			enddate = form.cleaned_data.get('enddate')
			starttime = form.cleaned_data.get('starttime')
			endtime = form.cleaned_data.get('endtime')
			reason = form.cleaned_data.get('reason')
			teachertimeofftype = form.cleaned_data.get('teachertimeofftype')
			pickvp = form.cleaned_data.get('pickvp')
			period = form.cleaned_data.get('period')
			stafftype = "Teacher"

			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(startdate), date_format)
			end_date = datetime.datetime.strptime(str(enddate), date_format)
			# start_date = startdate.day
			# end_date = enddate.day
			

			if starttime == None and endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif starttime != None and endtime != None:
				start_time = starttime.hour + starttime.minute/60
				end_time = endtime.hour + endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/9
				hr = (end_date - start_date).days*24 + end_time-start_time
			
			duration = my_round(dur)

			a_form = LeaveApplication.objects.create(startdate=startdate, enddate=enddate, starttime=starttime, endtime=endtime, teachertimeofftype=teachertimeofftype, alltimeofftype=teachertimeofftype, reason=reason, firststatus = firststatus, secondstatus = secondstatus, user=user, stafftype=stafftype, pickvp=pickvp,duration=duration, period=period)
			a_form.save()	

			period_list = "";
			for stuff in period:
				period_list+= stuff + ", ";
			messages.success(request, f'Successfully Applied')
			template = render_to_string('users/email_teachingstaffapply.html', {
				'username':request.user.username,
				'type':teachertimeofftype,
				'startdate':startdate,
				'starttime':starttime,
				'endtime':endtime,
				'enddate':enddate,
				'period':period_list,
				'reason':reason
				})
			send_mail(
				'Leave Application Confirmation' ,
				template,
				'test@gmail.com',
				[request.user.email],
				)

			return redirect('success')
			

		else:
			messages.warning(request, f'Start date/time must be less than or equal to End date/time!!!')
	else:
		form = TeacherApplyForm()
		
	return render(request, "users/apply.html", {'form': form, 'userid':userid})

@login_required
def supervisorapply(request, *args, **kwargs):
	if request.user.is_supervisor:
		userid = SupervisorDetail.objects.get(user = request.user)
		firststatus = "Approved"
		secondstatus = "Pending"
	elif request.user.is_viceprincipal:
		userid = VicePrincipalDetail.objects.get(user = request.user)
		firststatus = "Approved"
		secondstatus = "Approved"
	elif request.user.is_teacher:
		userid = TeachingStaffDetail.objects.get(user = request.user)
		firststatus = "Pending"
		secondstatus = "Pending"
	elif request.user.is_nonteacher:
		userid = NonTeachingStaffDetail.objects.get(user = request.user)
		firststatus = "Pending"
		secondstatus = "Pending"
	else:
		userid = SecretaryDetail.objects.get(user = request.user)
		firststatus = "Pending"
		secondstatus = "Pending"

	if request.method == 'POST':
		form = GroupApplyForm(request.POST)
		
		if form.is_valid():		
			f = form.save(commit=False)

			startdate = form.cleaned_data.get('startdate')
			enddate = form.cleaned_data.get('enddate')
			starttime = form.cleaned_data.get('starttime')
			endtime = form.cleaned_data.get('endtime')
			reason = form.cleaned_data.get('reason')
			teachertimeofftype = form.cleaned_data.get('officialtype')
			nonteachertimeofftype = form.cleaned_data.get('officialtype')
			pickvp = form.cleaned_data.get('pickvp')
			if(teachertimeofftype == None):
				alltimeofftype = nonteachertimeofftype;
			else:
				alltimeofftype = teachertimeofftype;
			
			alluser = form.cleaned_data.get('users')
			appliedby = request.user
			period = form.cleaned_data.get('period')

			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(startdate), date_format)
			end_date = datetime.datetime.strptime(str(enddate), date_format)

			if starttime == None and endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif starttime != None and endtime != None:
				start_time = starttime.hour + starttime.minute/60
				end_time = endtime.hour + endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/8
				hr = (end_date - start_date).days*24 + end_time-start_time
			duration = my_round(dur)
			# Removed user = request.user to avoid double entry for profile page with group apply for the same user
			f = LeaveApplication.objects.create(startdate=startdate, enddate=enddate, starttime=starttime, endtime=endtime, alltimeofftype=nonteachertimeofftype, reason=reason, firststatus = firststatus, secondstatus = secondstatus,appliedby=request.user, duration = duration ,groupapplystatus=True, pickvp=pickvp, period=period)
			f.users.set(alluser)
			f.save()			
			
			period_list = "";
			for stuff in period:
				period_list+= stuff + ", ";
			my_list = "";
			for stuff in alluser:
				my_list+=stuff.username + ", ";
			
			template = render_to_string('users/email_groupapply.html', {
				'username':my_list,
				'type':alltimeofftype,
				'startdate':startdate,
				'enddate':enddate,
				'starttime':starttime,
				'endtime':endtime,
				'period':period_list,
				'reason':reason,
				'applied_by':request.user.username
				})

			
			for stuff in alluser:
				send_mail(
					'Leave Application Confirmation' ,
					template,
					'test@gmail.com',
					[stuff.email],
					)
			send_mail(
				'iLeave Confirmation' ,
				'Thank you '+request.user.username+ '! You applied '+alltimeofftype+' for '+my_list,
				'test@gmail.com',
				[request.user.email],
				)
			messages.success(request, f' {my_list} : Successfully Applied')
			
			return redirect('successgroupapply')
	else:
		form = GroupApplyForm()
		# pickform = PickerForm()

	return render(request, "users/supervisorapply.html", {'form':form})
@login_required
def groupapplylistview(req):

	queryset = LeaveApplication.objects.filter(appliedby = req.user) # list of objects
	context = {
		"objec_list" : queryset
	}
	return render(req, "users/groupapplylistview.html", context)

@login_required
def groupapplychangeview(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)
	
	if obj.groupapplystatus:
		userid= obj.appliedby
	else:
		userid=obj.user

	if userid.is_secretary:
		applicant = SecretaryDetail.objects.get(user = userid)
	elif userid.is_nonteacher:
		applicant = NonTeachingStaffDetail.objects.get(user = userid)
	elif userid.is_supervisor:
		applicant = SupervisorDetail.objects.get(user = userid)
	elif userid.is_viceprincipal:
		applicant = VicePrincipalDetail.objects.get(user = userid)
	else:
		applicant = TeachingStaffDetail.objects.get(user = userid)
	if request.method == 'POST':
		# pickform = PickerForm(request.POST)
		form = GroupApplyForm(request.POST, instance=obj)
		# userid = request.POST['users']
		# user_objects = User.objects.filter(id=userid)
		# alluser = ""
		if form.is_valid():		
			form.save()
			# p = pickform.save(commit=False)
			obj.startdate = form.cleaned_data.get('startdate')
			obj.enddate = form.cleaned_data.get('enddate')
			obj.starttime = form.cleaned_data.get('starttime')
			obj.endtime = form.cleaned_data.get('endtime')
			obj.reason = form.cleaned_data.get('reason')
			obj.teachertimeofftype = form.cleaned_data.get('officialtype')
			obj.nonteachertimeofftype = form.cleaned_data.get('officialtype')
			if(obj.teachertimeofftype == None):
				obj.alltimeofftype = obj.nonteachertimeofftype;
			else:
				obj.alltimeofftype = obj.teachertimeofftype;
			
			obj.alluser = form.cleaned_data.get('users')
			obj.appliedby = request.user
			obj.period = form.cleaned_data.get('period')
			obj.pickvp = form.cleaned_data.get('pickvp')
			
			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(obj.startdate), date_format)
			end_date = datetime.datetime.strptime(str(obj.enddate), date_format)

			if obj.starttime == None and obj.endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif obj.starttime != None and obj.endtime != None:
				start_time = obj.starttime.hour + obj.starttime.minute/60
				end_time = obj.endtime.hour + obj.endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/8
				hr = (end_date - start_date).days*24 + end_time-start_time
			obj.duration = my_round(dur)
			
			# f = LeaveApplication.objects.update(startdate=startdate, enddate=enddate, starttime=starttime, endtime=endtime, alltimeofftype=nonteachertimeofftype, reason=reason, firststatus = firststatus, secondstatus = secondstatus, user= request.user,appliedby=request.user, duration = duration ,groupapplystatus=True, period=period)
			# f.users.set(alluser)
						
			obj.save()

			period_list = "";
			for stuff in obj.period:
				period_list+= stuff + ", ";
			my_list = "";
			for stuff in obj.alluser:
				my_list+=stuff.username + ", ";
			template = render_to_string('users/email_groupapply.html', {
				'username':my_list,
				'type':obj.alltimeofftype,
				'startdate':obj.startdate,
				'enddate':obj.enddate,
				'period':period_list,
				'reason':obj.reason,
				'applied_by':request.user.username
				})

			
			for stuff in obj.alluser:
				send_mail(
					'Leave Application Confirmation' ,
					template,
					'test@gmail.com',
					[stuff.email],
					)
			send_mail(
				'iLeave Confirmation' ,
				'Thank you '+request.user.username+ '! You applied '+obj.alltimeofftype+' for '+my_list,
				'test@gmail.com',
				[request.user.email],
				)
			messages.success(request, f' {my_list} : Successfully Modified')
			
			return redirect('successgroupapply')
	else:
		form = GroupApplyForm(instance= obj)

	return render(request, "users/groupapplychangeview.html", {'form':form,'obj' : obj})

@login_required
def applyforapply(request, *args, **kwargs):
	if request.user.is_supervisor:
		userid = SupervisorDetail.objects.get(user = request.user)
	elif request.user.is_viceprincipal:
		userid = VicePrincipalDetail.objects.get(user = request.user)
	elif request.user.is_secretary:
		userid = SecretaryDetail.objects.get(user = request.user)
	if request.method == 'POST':
		pickform = PickerForm(request.POST)
		form = ApplyForForm(request.POST)
		userid = request.POST['pickuser']
		user = User.objects.filter(id=userid)
		# userid = list(User.objects.filter(username=request.POST['pickuser']).values('pickuser'))
		if form.is_valid() and pickform.is_valid():		
			f = form.save(commit=False)
			p = pickform.save(commit=False)
			startdate = form.cleaned_data.get('startdate')
			enddate = form.cleaned_data.get('enddate')
			starttime = form.cleaned_data.get('starttime')
			endtime = form.cleaned_data.get('endtime')
			reason = form.cleaned_data.get('reason')
			emergencytype = form.cleaned_data.get('emergencytype')
			firststatus = 'Approved'
			secondstatus = 'Approved'
			secretarystatus = 'Pending'
			finalstatus = 'Pending'
			teachertimeofftype = emergencytype
			nonteachertimeofftype = emergencytype
			alluser = pickform.cleaned_data.get('pickuser')
			appliedby = request.user
			emergencystatus = True
			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(startdate), date_format)
			end_date = datetime.datetime.strptime(str(enddate), date_format)
			# start_date = startdate.day
			# end_date = enddate.day
			

			if starttime == None and endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif starttime != None and endtime != None:
				start_time = starttime.hour + starttime.minute/60
				end_time = endtime.hour + endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/8
				hr = (end_date - start_date).days*24 + end_time-start_time
			
			if nonteachertimeofftype == 'Overtime' :
				duration = decimal.Decimal(hr) * userid.ratio
			elif nonteachertimeofftype == 'Overtime Compensatory Leave':
				duration = decimal.Decimal(hr)
			else:
				duration = my_round(dur)

			
				

			my_list = "";
			for stuff in alluser:
				if stuff.is_nonteacher:
					f = LeaveApplication.objects.create(emergencystatus=emergencystatus,startdate=startdate, enddate=enddate, starttime=starttime, endtime=endtime, firststatus=firststatus, secondstatus=secondstatus,secretarystatus= secondstatus, finalstatus=finalstatus, nonteachertimeofftype=nonteachertimeofftype, alltimeofftype=nonteachertimeofftype,appliedby = appliedby,reason=reason, user=stuff, stafftype = "Nonteacher",duration=duration)
					f.save()			
					messages.success(request, f'Successfully Applied')
				elif stuff.is_viceprincipal or stuff.is_teacher or stuff.is_principal or stuff.is_supervisor:	
					if duration <= 1 :
						firststatus = 'Action Required'
						secondstatus = 'Action Required'
						secretarystatus = 'Action Required'
						finalstatus = 'Action Required'
					f = LeaveApplication.objects.create(emergencystatus=emergencystatus,startdate=startdate, enddate=enddate, starttime=starttime, endtime=endtime, firststatus=firststatus, secondstatus=secondstatus,secretarystatus= secondstatus, finalstatus=finalstatus, teachertimeofftype=teachertimeofftype, alltimeofftype=teachertimeofftype,appliedby = appliedby,reason=reason, user=stuff, stafftype = "Teacher",duration=duration)
					f.save()			
					messages.success(request, f'Successfully Applied')

				my_list+=stuff.username + ", ";
				send_mail(
				'iLeave Confirmation' ,
				'Hello '+stuff.username+ '! ' + request.user.username + ' has submitted an application for '+emergencytype+' on your behalf!' ,
				'test@gmail.com',
				[stuff.email],
				)
			send_mail(
				'iLeave Confirmation' ,
				'Thank you '+request.user.username+ '! You application '+emergencytype+' for '+my_list,
				'test@gmail.com',
				[request.user.email],
				)
			return redirect('success')
	else:
		form = ApplyForForm()
		pickform = PickerForm()

	return render(request, "users/applyforapply.html", {'form':form, 'pickform':pickform, 'userid':userid})

@login_required
def applyforapply2(request, *args, **kwargs):
	if request.user.is_supervisor:
		userid = SupervisorDetail.objects.get(user = request.user)
	elif request.user.is_viceprincipal:
		userid = VicePrincipalDetail.objects.get(user = request.user)
	elif request.user.is_secretary:
		userid = SecretaryDetail.objects.get(user = request.user)
	if request.method == 'POST':
		pickform = PickerForm(request.POST)
		form = ApplyForForm2(request.POST)
		userid = request.POST['pickuser']
		user = User.objects.filter(id=userid)
		# userid = list(User.objects.filter(username=request.POST['pickuser']).values('pickuser'))
		if form.is_valid() and pickform.is_valid():		
			f = form.save(commit=False)
			p = pickform.save(commit=False)
			startdate = form.cleaned_data.get('startdate')
			enddate = form.cleaned_data.get('enddate')
			starttime = form.cleaned_data.get('starttime')
			endtime = form.cleaned_data.get('endtime')
			reason = form.cleaned_data.get('reason')
			alltimeofftype = form.cleaned_data.get('alltimeofftype')
			firststatus = 'Pending'
			secondstatus = 'Pending'
			finalstatus = 'Pending'
			teachertimeofftype = alltimeofftype
			nonteachertimeofftype = alltimeofftype
			alluser = pickform.cleaned_data.get('pickuser')

			pickmanager = form.cleaned_data.get('pickmanager') 

			appliedby = request.user
			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(startdate), date_format)
			end_date = datetime.datetime.strptime(str(enddate), date_format)
			# start_date = startdate.day
			# end_date = enddate.day
			

			if starttime == None and endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif starttime != None and endtime != None:
				start_time = starttime.hour + starttime.minute/60
				end_time = endtime.hour + endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/8
				hr = (end_date - start_date).days*24 + end_time-start_time
			
			if nonteachertimeofftype == 'Overtime' :
				duration = decimal.Decimal(hr) * userid.ratio
			elif nonteachertimeofftype == 'Overtime Compensatory Leave':
				duration = decimal.Decimal(hr)
			else:
				duration = my_round(dur)

			my_list = "";
			for stuff in alluser:
				if stuff.is_nonteacher:
					if pickmanager == None and not stuff.is_supervisor:
						superv = SupervisorDetail.objects.get(user__username=stuff.NonTeachingStaffDetail.supervisor)
						pickmanager = User.objects.get(username = superv.user)
					else:
						pickmanager = None
					f = LeaveApplication.objects.create(pickmanager=pickmanager,startdate=startdate, enddate=enddate, starttime=starttime, endtime=endtime, firststatus=firststatus, secondstatus=secondstatus, finalstatus=finalstatus, nonteachertimeofftype=alltimeofftype, alltimeofftype=alltimeofftype,appliedby = appliedby,reason=reason, user=stuff, stafftype = "Nonteacher",duration=duration)
					f.save()			
					messages.success(request, f'Successfully Applied')
				elif stuff.is_viceprincipal or stuff.is_teacher or stuff.is_principal or stuff.is_supervisor and stuff.is_teacher:	
					f = LeaveApplication.objects.create(startdate=startdate, enddate=enddate, starttime=starttime, endtime=endtime, firststatus=firststatus, secondstatus=secondstatus, finalstatus=finalstatus, teachertimeofftype=alltimeofftype, alltimeofftype=alltimeofftype,appliedby = appliedby,reason=reason, user=stuff, stafftype = "Teacher",duration=duration)
					f.save()			
					messages.success(request, f'Successfully Applied')
				my_list+=stuff.username + ", ";
				send_mail(
				'iLeave Confirmation' ,
				'Hello '+stuff.username+ '! ' + request.user.username + ' has submitted an application for '+alltimeofftype+' on your behalf!' ,
				'test@gmail.com',
				[stuff.email],
				)
			send_mail(
				'iLeave Confirmation' ,
				'Thank you '+request.user.username+ '! You application '+alltimeofftype+' for '+my_list,
				'test@gmail.com',
				[request.user.email],
				)
			return redirect('success')
	else:
		form = ApplyForForm2()
		pickform = PickerForm()

	return render(request, "users/applyforapply2.html", {'form':form, 'pickform':pickform, 'userid':userid})

@login_required
def incrementallview(request, *args, **kwargs):
	
	if request.method == 'POST':

		form = IncrementAllForm(request.POST)
		userall = User.objects.exclude(is_principal = True)
		# userid = list(User.objects.filter(username=request.POST['pickuser']).values('pickuser'))
		if form.is_valid():		
			f = form.save(commit=False)
						
			for stuff in userall:
				if stuff.is_supervisor:
					supervisordetail = SupervisorDetail.objects.get(user=stuff)

					num = supervisordetail.sickleave + supervisordetail.increment
					if (num > supervisordetail.maxsickleave):
						supervisordetail.sickleave = supervisordetail.maxsickleave
					else:
						supervisordetail.sickleave = num

					created_at = form.cleaned_data.get('created_at')

					f = IncrementAll.objects.create(created_at=created_at, added = supervisordetail.increment, user = stuff)
					supervisordetail.save()
					f.save()			
				elif stuff.is_viceprincipal and stuff.is_teacher:
					viceprincipaldetail = VicePrincipalDetail.objects.get(user=stuff)

					num = viceprincipaldetail.sickleave + viceprincipaldetail.increment
					if (num > viceprincipaldetail.maxsickleave):
						viceprincipaldetail.sickleave = viceprincipaldetail.maxsickleave
					else:
						viceprincipaldetail.sickleave = num

					created_at = form.cleaned_data.get('created_at')
					f = IncrementAll.objects.create(created_at=created_at, added = viceprincipaldetail.increment, user = stuff)
					viceprincipaldetail.save()
					f.save()			

				elif stuff.is_nonteacher and not stuff.is_secretary and not stuff.is_supervisor:
					nonteacherdetail = NonTeachingStaffDetail.objects.get(user=stuff)
					num = nonteacherdetail.sickleave + nonteacherdetail.increment
					if (num > nonteacherdetail.maxsickleave):
						nonteacherdetail.sickleave = nonteacherdetail.maxsickleave
					else:
						nonteacherdetail.sickleave = num

					created_at = form.cleaned_data.get('created_at')
					f = IncrementAll.objects.create(created_at=created_at, added = nonteacherdetail.increment, user = stuff)
					nonteacherdetail.save()
					f.save()			

				elif stuff.is_teacher:
					teacherdetail = get_object_or_404(TeachingStaffDetail, user = stuff)

					num = teacherdetail.sickleave + teacherdetail.increment
					if (num > teacherdetail.maxsickleave):
						teacherdetail.sickleave = teacherdetail.maxsickleave
					else:
						teacherdetail.sickleave = num

					created_at = form.cleaned_data.get('created_at')
					f = IncrementAll.objects.create(created_at=created_at, added = teacherdetail.increment, user = stuff)
					teacherdetail.save()
					f.save()			
						
			messages.success(request, f'Timeoff added for all users')
			return redirect('incrementallview')
	else:
		form = IncrementAllForm(request.POST)
		

	return render(request, "users/incrementall.html", {'form':form})

@login_required
def incrementlistview(req):

	queryset = IncrementAll.objects.all() # list of objects
	context = {
		"objec_list" : queryset
	}
	return render(req, "users/incrementlistview.html", context)




@login_required
def success(req):
	obj = LeaveApplication.objects.all()
	context = {"object" : obj
	}
	return render(req,"users/success.html",context)

@login_required
def successgroupapply(req):
	obj = LeaveApplication.objects.all()
	context = {"object" : obj
	}
	return render(req,"users/successgroupapply.html",context)

@login_required
def managerlistview(req):
	user_manager = req.user
	userid =  req.user.SupervisorDetail.overseeing.all()
	queryset = LeaveApplication.objects.filter(Q(user__id__in=userid.all()) | Q(pickmanager__id=user_manager.id))
	managerpicked = LeaveApplication.objects.filter(pickmanager__id=user_manager.id) # list of objects
	
	context = {
		"objec_list" : queryset,
		'user_manager' : user_manager,
		'managerpicked': managerpicked
	}
	return render(req, "users/managerlistview.html", context)

@login_required
def managerapprove(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)
	
	if obj.groupapplystatus:
		userid= obj.appliedby
	else:
		userid=obj.user

	if userid.is_secretary:
		applicant = SecretaryDetail.objects.get(user = userid)
	elif userid.is_nonteacher:
		applicant = NonTeachingStaffDetail.objects.get(user = userid)
	elif userid.is_supervisor:
		applicant = SupervisorDetail.objects.get(user = userid)
	elif userid.is_viceprincipal:
		applicant = VicePrincipalDetail.objects.get(user = userid)
	else:
		applicant = TeachingStaffDetail.objects.get(user = userid)

	if request.method == 'POST':	
		u_form = FirstValidate(request.POST, instance=obj)
		if u_form.is_valid():
			f = u_form.save(commit=False)
			obj.firststatus = u_form.cleaned_data.get('firststatus')
			obj.firstcomment = u_form.cleaned_data.get('firstcomment')
			obj.firstapprovedby = request.user
			obj.save()
			messages.success(request, f'DONE')


			if (obj.pickmanager != None and u_form.cleaned_data.get('firststatus') == "Denied"):
				send_mail(
						'iLeave Confirmation' ,
						'Hello '+obj.user.username+ '! You application for Official leave is denied by '+request.user.username+', please reach out!',
						'test@gmail.com',
						[obj.user.email],
						)

			if (obj.pickvp != None and u_form.cleaned_data.get('firststatus') == "Approved"):
				vpdetail = VicePrincipalDetail.objects.get(user__username=obj.pickvp)
				pickedvp = User.objects.get(username = vpdetail.user)
				send_mail(
				'Leave Application Confirmation' ,
				'Hello '+pickedvp.username+ '. There is an application needs your attention. Please login and check under Manage Pending Application http://a.kachi.edu.hk/vplistview/',
				'test@gmail.com',
				[pickedvp.email],
				)

			if (obj.pickvp == None and u_form.cleaned_data.get('firststatus') == "Approved"):
				pickedvp = User.objects.filter(is_viceprincipal = True)
				for stuff in pickedvp:

					send_mail(
					'Leave Application Confirmation' ,
					'Hello '+stuff.username+ '. There is an application needs your attention. Please login and check under Manage Pending Application http://a.kachi.edu.hk/vplistview/',
					'test@gmail.com',
					[stuff.email],
					)


			return redirect('managerlistview')

	else:
		u_form = FirstValidate(instance=obj)



		context = {
			'u_form':u_form,
			'obj' : obj,
			'applicant' : applicant
		}
	# context = {
	# 	"objec" : obj
	# }
	return render(request, "users/approve.html", context)

@login_required
def vplistview(req):
	useri =  req.user
	userid =  req.user.VicePrincipalDetail.allvp.all()
	queryset = LeaveApplication.objects.exclude(user__id__in=userid.all()) # list of objects
	context = {
		"objec_list" : queryset,
		"user" : useri
	}
	return render(req, "users/vplistview.html", context)

@login_required
def vpapprove(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)
	if obj.groupapplystatus:
		userid= obj.appliedby
	else:
		userid=obj.user

	if userid.is_secretary:
		applicant = SecretaryDetail.objects.get(user = userid)
	elif userid.is_nonteacher:
		applicant = NonTeachingStaffDetail.objects.get(user = userid)
	elif userid.is_supervisor:
		applicant = SupervisorDetail.objects.get(user = userid)
	elif userid.is_viceprincipal:
		applicant = VicePrincipalDetail.objects.get(user = userid)
	else:
		applicant = TeachingStaffDetail.objects.get(user = userid)
	

	if request.method == 'POST':
		u_form = SecondValidate(request.POST, instance=obj)
		
		if u_form.is_valid():
			if  obj.secondstatus == 'Pending' and obj.pickvp == request.user:	
				u_form.save()
				messages.warning(request, f'Please select a Decision')
				return redirect(request.get_full_path())		
			f = u_form.save(commit=False)
			obj.pickvp = u_form.cleaned_data.get('pickvp')
			obj.secondstatus = u_form.cleaned_data.get('secondstatus')
			obj.secondcomment = u_form.cleaned_data.get('secondcomment')
			obj.secondapprovedby = request.user


			obj.save()
			
			messages.success(request, f'Saved')
			if obj.pickvp != request.user and obj.pickvp != None:
				pickedvp = User.objects.filter(username=obj.pickvp)
				print(obj.pickvp)
				print("testing picked vp")
				for stuff in pickedvp:

					send_mail(
					'Leave Application Confirmation' ,
					'Hello '+stuff.username+ '. There is an application needs your attention. Please login and check under Manage Pending Application http://a.kachi.edu.hk/vplistview/',
					'test@gmail.com',
					[stuff.email],
					)

			return redirect('vplistview')
	else:
		u_form = SecondValidate(instance=obj)


		context = {
			'u_form':u_form,
			'obj' : obj,
			'applicant' : applicant
		}

	return render(request, "users/vpapprove.html", context)

@login_required
def secretarylistview(req):
	queryset = LeaveApplication.objects.all().order_by('startdate')# list of objects

	context = {
		"objec_list" : queryset,
	}
	return render(req, "users/secretarylistview.html", context)

@login_required
def secretaryapprove(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)
	
	if obj.groupapplystatus:
		userid= obj.appliedby
	else:
		userid=obj.user

	if userid.is_secretary:
		applicant = SecretaryDetail.objects.get(user = userid)
	elif userid.is_nonteacher:
		applicant = NonTeachingStaffDetail.objects.get(user = userid)
	elif userid.is_supervisor:
		applicant = SupervisorDetail.objects.get(user = userid)
	elif userid.is_viceprincipal:
		applicant = VicePrincipalDetail.objects.get(user = userid)
	else:
		applicant = TeachingStaffDetail.objects.get(user = userid)
	if request.method == 'POST':	
		u_form = SecretaryValidate(request.POST, instance=obj)
		if u_form.is_valid():
			if  obj.secretarystatus == 'Pending':	
				u_form.save()
				messages.warning(request, f'Please select a Decision')
				return redirect(request.get_full_path())
			if obj.finalduration is None:
				modify = obj.duration
				u_form.save()
				obj.finalduration = modify
				obj.updated_at = datetime.datetime.now()
				obj.save()
				messages.success(request, f'Sucessfully Approved')

				

				return redirect('secretarylistview')
			else:
				modify = obj.finalduration
				u_form.save()
				obj.period = u_form.cleaned_data.get('period');
				obj.finalduration = modify
				obj.updated_at = datetime.datetime.now()
				obj.save()
				messages.success(request, f'Sucessfully Approved')
				return redirect('secretarylistview')
			
	else:
		u_form = SecretaryValidate(instance=obj)


		context = {
			'u_form':u_form,
			'obj' : obj,
			'applicant' : applicant
		}
	return render(request, "users/secretaryapprove.html", {
			'u_form':u_form,
			'obj' : obj,
			'applicant' : applicant
		})

@login_required
def plistview(req):
	if req.user.is_principal or req.user.is_secretary:	
		userid = req.user
	queryset = LeaveApplication.objects.all() # list of objects
	context = {
		"objec_list" : queryset,
		"userid" : userid
	}
	return render(req, "users/plistview.html", context)

@login_required
def papprove(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)
	if request.user.is_principal or request.user.is_secretary:	
		getpid = request.user

	if obj.groupapplystatus:
		userid= obj.appliedby
	else:
		userid=obj.user

	if userid.is_secretary:
		applicant = SecretaryDetail.objects.get(user = userid)
	elif userid.is_nonteacher:
		applicant = NonTeachingStaffDetail.objects.get(user = userid)
	elif userid.is_supervisor:
		applicant = SupervisorDetail.objects.get(user = userid)
	elif userid.is_viceprincipal:
		applicant = VicePrincipalDetail.objects.get(user = userid)
	else:
		applicant = TeachingStaffDetail.objects.get(user = userid)

	if request.method == 'POST' :
		u_form = FinalValidate(request.POST, instance=obj)
		duration = u_form.data['finalduration']
		if u_form.is_valid() and obj.finalstatus == 'Approved':
			if obj.user != None:			
				if u_form.is_valid() and obj.user.is_nonteacher:
					if obj.nonteacherchangetimeofftype is None:
						if obj.nonteachertimeofftype == 'Annual Leave':
							if obj.finalduration is None:
								modify = obj.duration
								applicant.annualleave = applicant.annualleave - abs(modify)
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')

								

							else:
								modify = obj.finalduration
								applicant.annualleave = applicant.annualleave - abs(modify)
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')

								


						elif obj.nonteachertimeofftype == 'Sick Leave':
							if obj.finalduration is None:
								modify = obj.duration
								applicant.sickleave = applicant.sickleave - abs(modify)
								applicant.sickleavecounter = applicant.sickleavecounter + abs(modify)
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
							else:
								modify = obj.finalduration
								applicant.sickleave = applicant.sickleave - abs(modify)
								applicant.sickleavecounter = applicant.sickleavecounter + abs(modify)
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
						elif obj.nonteachertimeofftype == 'Overtime':
							if obj.finalduration is None:
								modify = obj.duration
								applicant.compensatedleave = applicant.compensatedleave + modify
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
							else:
								modify = obj.finalduration
								applicant.compensatedleave = applicant.compensatedleave + modify
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
						elif obj.nonteachertimeofftype == 'Overtime Compensatory Leave':
							if obj.finalduration is None:
								modify = obj.duration
								applicant.compensatedleave = applicant.compensatedleave - modify
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
							else:
								modify = obj.finalduration
								applicant.compensatedleave = applicant.compensatedleave - modify
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
						else:
							u_form.save()
							messages.success(request, f'Sucessfully Approved')
					elif obj.nonteacherchangetimeofftype == 'Annual Leave':  #change leave type for non teacher

						if obj.finalduration is None:
								modify = obj.duration
								applicant.annualleave = applicant.annualleave - abs(modify)
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
						else:
							modify = obj.finalduration
							applicant.annualleave = applicant.annualleave - abs(modify)
							u_form.save()
							applicant.save()
							obj.finalduration = modify
							obj.updated_at = datetime.datetime.now()
							obj.save()
							messages.success(request, f'Sucessfully Approved')
					elif obj.nonteacherchangetimeofftype == 'Overtime Compensatory Leave':  #change leave type for non teacher
					
						if obj.finalduration is None:
								modify = obj.duration
								applicant.compensatedleave = applicant.compensatedleave - modify
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
						else:
							modify = obj.finalduration
							applicant.compensatedleave = applicant.compensatedleave - modify
							u_form.save()
							applicant.save()
							obj.finalduration = modify
							obj.updated_at = datetime.datetime.now()
							obj.save()
							messages.success(request, f'Sucessfully Approved')
					elif obj.nonteacherchangetimeofftype == 'No-Pay Leave':  #change leave type for non teacher
					
						if obj.finalduration is None:
								modify = obj.duration
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
						else:
							modify = obj.finalduration
							u_form.save()
							applicant.save()
							obj.finalduration = modify
							obj.updated_at = datetime.datetime.now()
							obj.save()
							messages.success(request, f'Sucessfully Approved')
				elif u_form.is_valid() and obj.user.is_teacher:
					if obj.teacherchangetimeofftype is None:	
						if obj.teachertimeofftype == 'Casual Leave':
							if obj.finalduration is None:
								modify = obj.duration
								applicant.casualleave = applicant.casualleave - abs(modify)
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
							else:
								modify = obj.finalduration
								applicant.casualleave = applicant.casualleave - abs(modify)
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')

						elif obj.teachertimeofftype == 'Sick Leave':
							if obj.finalduration is None:
								modify = obj.duration
								applicant.sickleave = applicant.sickleave - abs(modify)
								applicant.sickleavecounter = applicant.sickleavecounter + abs(modify)
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
							else:
								modify = obj.finalduration
								applicant.sickleave = applicant.sickleave - abs(modify)
								u_form.save()
								applicant.save()
								obj.finalduration = modify
								obj.updated_at = datetime.datetime.now()
								obj.save()
								messages.success(request, f'Sucessfully Approved')
						else:
							u_form.save()
							messages.success(request, f'Sucessfully Approved')
					elif obj.teacherchangetimeofftype == 'No-Pay Leave':  #change leave type for non teacher
						if obj.finalduration is None:
							modify = obj.duration
							u_form.save()
							applicant.save()
							obj.finalduration = modify
							obj.updated_at = datetime.datetime.now()
							obj.save()
							messages.success(request, f'Sucessfully Approved')
						else:
							modify = obj.finalduration
							u_form.save()
							applicant.save()
							obj.finalduration = modify
							obj.updated_at = datetime.datetime.now()
							obj.save()
							messages.success(request, f'Sucessfully Approved')
			else:
				u_form.save()
				messages.success(request, f'Sucessfully Approved')
		elif u_form.is_valid() and obj.finalstatus == 'Denied':	
			if u_form.is_valid():
				u_form.save()
				messages.success(request, f'LeaveApplication Denied')
		elif u_form.is_valid() and obj.finalstatus == 'Pending':	
			if u_form.is_valid():
				u_form.save()
				messages.warning(request, f'Please select a Decision')
				return redirect(request.get_full_path())
		elif u_form.is_valid() and obj.finalstatus == 'Canceled':	
			if u_form.is_valid():
				u_form.save()
				messages.success(request, f'LeaveApplication Canceled')
				return redirect(request.get_full_path())

		period_list = "";
		if obj.period is not None:
			for stuff in obj.period:
				period_list+= stuff + ", ";
		# messages.success(request, f'Successfully Applied')
		

		if obj.users != None and obj.user == None:
			for stuff in obj.users.all():
				template = render_to_string('users/email_principalapprove.html', {
				'username':stuff.username,
				'type':obj.alltimeofftype,
				'startdate':obj.startdate,
				'starttime':obj.starttime,
				'endtime': obj.endtime,
				'enddate':obj.enddate,
				'period':period_list,
				'finalduration':obj.finalduration,
				'finalstatus':obj.finalstatus,
				'reason':obj.reason
				})
				send_mail(
					'Leave Application Confirmation' ,
					template,
					'test@gmail.com',
					[stuff.email],
					)
		if obj.user != None:
			template = render_to_string('users/email_principalapprove.html', {
					'username':obj.user.username,
					'type':obj.alltimeofftype,
					'startdate':obj.startdate,
					'starttime':obj.starttime,
					'endtime': obj.endtime,
					'enddate':obj.enddate,
					'period':period_list,
					'finalduration':obj.finalduration,
					'finalstatus':obj.finalstatus,
					'reason':obj.reason
					})
			send_mail(
				'Result of Leave Application',
				template,
				'test@gmail.com',
				[obj.user.email],
				)
		return redirect('plistview') 
	else:
		u_form = FinalValidate(instance=obj)


		# context = {
		# 	'u_form':u_form,
		# 	'obj' : obj, 
		# 	'applicant' : applicant
		# }
	return render(request, "users/papprove.html", {	'getpid':getpid,
													'u_form':u_form,
													'obj' : obj, 
													'applicant' : applicant})

@login_required
def plistviewdecided(req):
	if req.user.is_principal or req.user.is_secretary:	
		userid = req.user
	
	queryset = LeaveApplication.objects.all() # list of objects
	context = {
		"objec_list" : queryset,
		"userid":userid
	}
	return render(req, "users/plistviewdecided.html", context)

@login_required
def papprovedecided(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)
	
	if request.user.is_principal or request.user.is_secretary:	
		getpid = request.user

	if obj.groupapplystatus:
		userid= obj.appliedby
	else:
		userid=obj.user

	if request.user.is_principal or request.user.is_secretary:	
		myuserid = request.user
	
	if userid.is_secretary:
		applicant = SecretaryDetail.objects.get(user = userid)
	
	elif userid.is_supervisor:
		applicant = SupervisorDetail.objects.get(user = userid)
	elif userid.is_nonteacher:
		applicant = NonTeachingStaffDetail.objects.get(user = userid)
	elif userid.is_viceprincipal:
		applicant = VicePrincipalDetail.objects.get(user = userid)
	else:
		applicant = TeachingStaffDetail.objects.get(user = userid)
	if request.method == 'POST' :
		u_form = CancelForm(request.POST, instance=obj)
		if u_form.is_valid() and obj.user.is_nonteacher:
			if obj.nonteachertimeofftype == 'Annual Leave':
				applicant.annualleave = applicant.annualleave + abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistviewdecided')

			elif obj.nonteachertimeofftype == 'Sick Leave':
				applicant.sickleave = applicant.sickleave + abs(obj.finalduration)
				applicant.sickleavecounter = applicant.sickleavecounter - abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistviewdecided')
			elif obj.nonteachertimeofftype == 'Overtime':
				applicant.compensatedleave = applicant.compensatedleave - abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistviewdecided')
			elif obj.nonteachertimeofftype == 'Overtime Compensatory Leave':
				applicant.compensatedleave = applicant.compensatedleave + abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistviewdecided')
			else:
				u_form.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistviewdecided')
		elif u_form.is_valid() and obj.user.is_supervisor:
			if obj.teachertimeofftype == 'Casual Leave':
				applicant.casualleave = applicant.casualleave + abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistview')
			elif obj.teachertimeofftype == 'Sick Leave':
				applicant.sickleave = applicant.sickleave + abs(obj.finalduration)
				applicant.sickleavecounter = applicant.sickleavecounter - abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistview')
			else:
				u_form.save()
				messages.success(request, f'supervisor DONE')
				return redirect('plistview')	

		elif u_form.is_valid() and obj.user.is_viceprincipal:
			if obj.teachertimeofftype == 'Casual Leave':
				applicant.casualleave = applicant.casualleave + abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistview')
			elif obj.teachertimeofftype == 'Sick Leave':
				applicant.sickleave = applicant.sickleave + abs(obj.finalduration)
				applicant.sickleavecounter = applicant.sickleavecounter - abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistview')
			else:
				u_form.save()
				messages.success(request, f'supervisor DONE')
				return redirect('plistview')		

		elif u_form.is_valid() and obj.user.is_teacher:
			if obj.teachertimeofftype == 'Casual Leave':
				applicant.casualleave = applicant.casualleave + abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistview')
			elif obj.teachertimeofftype == 'Sick Leave':
				applicant.sickleave = applicant.sickleave + abs(obj.finalduration)
				applicant.sickleavecounter = applicant.sickleavecounter - abs(obj.finalduration)
				obj.finalstatus = "Canceled"
				u_form.save()
				applicant.save()
				obj.save()
				messages.success(request, f'Sucessfully Canceled')
				return redirect('plistview')
			else:
				u_form.save()
				messages.success(request, f'supervisor DONE')
				return redirect('plistview')	
	else:
		u_form = CancelForm(instance=obj)
	return render(request, "users/papprovedecided.html", {
			'obj' : obj, 
			'applicant' : applicant,
			'u_form' : u_form,
			'myuserid':myuserid
			})

@login_required
def userlistview(req):
	queryset = User.objects.exclude(is_principal = True) # list of objects
	
	# myFilter = teacherLeaveApplicationFilter(request.GET, queryset=queryset)
	# queryset = myFilter.qs

	context = {
		"objec_list" : queryset
	}
	return render(req, "users/userlistview.html", context)

@login_required
def userdetailview(request, myid):
	obj = get_object_or_404(User, id =myid)
	obj = User.objects.get(id=myid)
	 
	annualleavetaken = None
	if obj.is_secretary:
		userInfo = SecretaryDetail.objects.get(user = obj)
		annualleavetaken = userInfo.maxannualleave - userInfo.annualleave
	elif obj.is_supervisor:
		userInfo = SupervisorDetail.objects.get(user = obj)
	elif obj.is_nonteacher:
		userInfo = NonTeachingStaffDetail.objects.get(user = obj)
		annualleavetaken = userInfo.maxannualleave - userInfo.annualleave
	elif obj.is_viceprincipal:
		userInfo = VicePrincipalDetail.objects.get(user = obj)
	else:
		userInfo = TeachingStaffDetail.objects.get(user = obj)

	

	applicant = LeaveApplication.objects.filter(Q(user=obj.user) | Q(users__in=[obj.user]))
	
	return render(request, "users/userdetailview.html", {
			'obj' : obj, 
			'applicant' : applicant,
			'userInfo' : userInfo,
			'annualleavetaken' : annualleavetaken
			})
@login_required
def alllistview(req):
	# allteacher = User.objects.filter(is_teacher = True)
	# allnonteacher = User.objects.filter(is_nonteacher = True)

	# teacherqueryset = LeaveApplication.objects.filter(user = allteacher) # list of objects
	# nonteacherqueryset = LeaveApplication.objects.filter(user = allnonteacher)

	queryset = LeaveApplication.objects.all().order_by('startdate')
	myFilter = LeaveApplicationFilter(req.GET, queryset=queryset)

	queryset = myFilter.qs

	if req.method == 'POST':
		response = HttpResponse(content_type='text/csv') 

		response['Content-Disposition'] = 'attachment; filename="LeaveExport.csv"' 
		response.write(u'\ufeff'.encode('utf8'))
		writer = csv.writer(response) 
		writer.writerow(['Apply Date/Time', 'Name', 'Leave Type', 'From Date', 'From Time', 'To Date', 'To Time','Duration' ,'Supervisor Decision', 'Vice Principal Decision', 'Principal Decision','Date Approved', 'Remark', 'Reason']) 
		instance = queryset 



		for row in instance:

			userlist = ""
			first_status = str(row.firststatus)+" by "+str(row.firstapprovedby)
			second_status = str(row.secondstatus)+" by "+str(row.secondapprovedby)
			if not row.groupapplystatus:
				userlist = row.user.username
			else:
				for stuff in row.users.all():
					userlist += str(stuff)+ " "
			
			writer.writerow([row.created_at_date, userlist, row.alltimeofftype, row.startdate, row.starttime, row.enddate, row.endtime, row.finalduration, first_status, second_status, row.finalstatus, row.updated_at, row.finalcomment, row.reason]) 
		return response 
	context = {
		"myFilter" : myFilter,
		"objec_list" : queryset,
	}
	return render(req, "users/alllistview.html", context)


@login_required
def alldetailview(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)

	if obj.groupapplystatus:
		userid= obj.appliedby
	else:
		userid=obj.user

	if userid.is_secretary:
		applicant = SecretaryDetail.objects.get(user = obj.user)
	
	elif userid.is_supervisor:
		applicant = SupervisorDetail.objects.get(user = obj.user)
	elif userid.is_nonteacher:
		applicant = NonTeachingStaffDetail.objects.get(user = obj.user)
	elif userid.is_viceprincipal:
		applicant = VicePrincipalDetail.objects.get(user = obj.user)
	else:
		applicant = TeachingStaffDetail.objects.get(user = obj.user)

	if request.method == 'POST':
		nonteacherform = NonTeacherApplyForm(request.POST, instance=obj)
		teacherform = TeacherApplyForm(request.POST, instance=obj)
		if obj.user.is_nonteacher:
			form = NonTeacherApplyForm(request.POST, instance=obj)
		else:
			form = TeacherApplyForm(request.POST, instance=obj)	
		g_form = GroupApplyForm(request.POST, instance=obj)
		u_form = UserCancelForm(request.POST, instance=obj)
		
		if 'cancel' in request.POST: 

			if obj.finalstatus == "Approved" and obj.finalduration != None:
				if obj.alltimeofftype == "Annual Leave":
					applicant.annualleave = applicant.annualleave + abs(obj.finalduration)
				elif obj.alltimeofftype == "Sick Leave":
					applicant.sickleave = applicant.sickleave + abs(obj.finalduration)
				elif obj.alltimeofftype == "Casual Leave":
					applicant.casualleave = applicant.casualleave + abs(obj.finalduration)
				elif obj.alltimeofftype == "Overtime":
					applicant.casualleave = applicant.casualleave - abs(obj.finalduration)
				elif obj.alltimeofftype == "Overtime Compensatory Leave":
					applicant.casualleave = applicant.casualleave + abs(obj.finalduration)

			obj.firststatus = "Canceled"
			obj.secondstatus = "Canceled"
			obj.finalstatus = "Canceled"


			obj.save()
			applicant.save()
			messages.success(request, f'Sucessfully Approved')
			return redirect('alllistview')
		if obj.user.is_nonteacher and nonteacherform.is_valid() and 'modify' in request.POST:
			nonteacherform.save()
			# p = pickform.save(commit=False)
			obj.startdate = nonteacherform.cleaned_data.get('startdate')
			obj.enddate = nonteacherform.cleaned_data.get('enddate')
			obj.starttime = nonteacherform.cleaned_data.get('starttime')
			obj.endtime = nonteacherform.cleaned_data.get('endtime')
			obj.reason = nonteacherform.cleaned_data.get('reason')
			obj.pickvp = nonteacherform.cleaned_data.get('pickvp')

			
			obj.nonteachertimeofftype = nonteacherform.cleaned_data.get('nonteachertimeofftype')
			obj.pickmanager = nonteacherform.cleaned_data.get('pickmanager')
		
			obj.alltimeofftype = obj.nonteachertimeofftype
			obj.period = nonteacherform.cleaned_data.get('period')
			
			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(obj.startdate), date_format)
			end_date = datetime.datetime.strptime(str(obj.enddate), date_format)

			if obj.starttime == None and obj.endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif obj.starttime != None and obj.endtime != None:
				start_time = obj.starttime.hour + obj.starttime.minute/60
				end_time = obj.endtime.hour + obj.endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/8
				hr = (end_date - start_date).days*24 + end_time-start_time

			# check if the principal had approved the application, if so, reverse the time off balance
			if obj.finalstatus == "Approved" and obj.finalduration != None  and obj.nonteacherchangetimeofftype == None:
				if obj.alltimeofftype == "Annual Leave":
					applicant.annualleave = applicant.annualleave + abs(obj.finalduration)
				elif obj.alltimeofftype == "Sick Leave":
					applicant.sickleave = applicant.sickleave + abs(obj.finalduration)
					applicant.sickleavecounter = applicant.sickleavecounter - abs(obj.finalduration)
				elif obj.alltimeofftype == "Overtime":
					applicant.compensatedleave = applicant.compensatedleave - abs(obj.finalduration)
				elif obj.alltimeofftype == "Overtime Compensatory Leave":
					applicant.compensatedleave = applicant.compensatedleave + abs(obj.finalduration)
			elif  obj.finalstatus == "Approved" and obj.finalduration != None  and obj.nonteacherchangetimeofftype != None:
				if obj.nonteacherchangetimeofftype == "Annual Leave":
					applicant.annualleave = applicant.annualleave + abs(obj.finalduration)
				elif obj.nonteacherchangetimeofftype == "Overtime Compensatory Leave":
					applicant.compensatedleave = applicant.compensatedleave + abs(obj.finalduration)


			obj.finalstatus = "Pending"
			obj.secretarystatus = "Pending"

			applicant.save()
			obj.duration = my_round(dur)	
			obj.save()
			messages.success(request, f'Redirects to Approval page for this application')
			return redirect('secretaryapprove', myid=myid)
		if obj.user.is_teacher and teacherform.is_valid() and 'modify' in request.POST:
			teacherform.save()
			# p = pickform.save(commit=False)
			obj.startdate = teacherform.cleaned_data.get('startdate')
			obj.enddate = teacherform.cleaned_data.get('enddate')
			obj.starttime = teacherform.cleaned_data.get('starttime')
			obj.endtime = teacherform.cleaned_data.get('endtime')
			obj.reason = teacherform.cleaned_data.get('reason')
			obj.pickvp = teacherform.cleaned_data.get('pickvp')

			
			obj.teachertimeofftype = teacherform.cleaned_data.get('teachertimeofftype')		
			obj.alltimeofftype = obj.teachertimeofftype
			obj.period = teacherform.cleaned_data.get('period')
			
			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(obj.startdate), date_format)
			end_date = datetime.datetime.strptime(str(obj.enddate), date_format)

			if obj.starttime == None and obj.endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif obj.starttime != None and obj.endtime != None:
				start_time = obj.starttime.hour + obj.starttime.minute/60
				end_time = obj.endtime.hour + obj.endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/8
				hr = (end_date - start_date).days*24 + end_time-start_time

			# check if the principal had approved the application, if so, reverse the time off balance
			if obj.finalstatus == "Approved" and obj.finalduration != None  and obj.teacherchangetimeofftype == None:
				if obj.alltimeofftype == "Annual Leave":
					applicant.annualleave = applicant.annualleave + abs(obj.finalduration)
				elif obj.alltimeofftype == "Sick Leave":
					applicant.sickleave = applicant.sickleave + abs(obj.finalduration)
					applicant.sickleavecounter = applicant.sickleavecounter - abs(obj.finalduration)
				elif obj.alltimeofftype == "Casual Leave":
					applicant.casualleave = applicant.casualleave + abs(obj.finalduration)
				
			elif  obj.finalstatus == "Approved" and obj.finalduration != None  and obj.teacherchangetimeofftype != None:
				if obj.teacherchangetimeofftype == "Casual Leave":
					applicant.casualleave = applicant.casualleave + abs(obj.finalduration)
			
			obj.finalstatus = "Pending"
			obj.secretarystatus = "Pending"

			applicant.save()
			obj.duration = my_round(dur)	
			obj.save()
			messages.success(request, f'Redirects to Approval page for this application')
			return redirect('secretaryapprove', myid=myid)
		if g_form.is_valid() and 'modifygroup' in request.POST:	
			g_form.save()
			# p = pickform.save(commit=False)
			obj.startdate = form.cleaned_data.get('startdate')
			obj.enddate = form.cleaned_data.get('enddate')
			obj.starttime = form.cleaned_data.get('starttime')
			obj.endtime = form.cleaned_data.get('endtime')
			obj.reason = form.cleaned_data.get('reason')
			obj.teachertimeofftype = form.cleaned_data.get('officialtype')
			obj.nonteachertimeofftype = form.cleaned_data.get('officialtype')
			if(obj.teachertimeofftype == None):
				obj.alltimeofftype = obj.nonteachertimeofftype;
			else:
				obj.alltimeofftype = obj.teachertimeofftype;
			
			obj.alluser = form.cleaned_data.get('users')
			obj.appliedby = request.user
			obj.period = form.cleaned_data.get('period')
			
			def my_round(x):
				return math.ceil(x*2)/2
			date_format = "%Y-%m-%d"
			start_date = datetime.datetime.strptime(str(obj.startdate), date_format)
			end_date = datetime.datetime.strptime(str(obj.enddate), date_format)

			if obj.starttime == None and obj.endtime == None:
				dur = (end_date - start_date).days + 1
				hr = ((end_date - start_date).days+ 1) * 24
			elif obj.starttime != None and obj.endtime != None:
				start_time = obj.starttime.hour + obj.starttime.minute/60
				end_time = obj.endtime.hour + obj.endtime.minute/60
				dur = (end_date - start_date).days + (end_time-start_time)/8
				hr = (end_date - start_date).days*24 + end_time-start_time
			obj.duration = my_round(dur)
			obj.save()
	else:
		nonteacherform = NonTeacherApplyForm(instance=obj)
		teacherform = TeacherApplyForm(instance=obj)
		g_form = GroupApplyForm(instance=obj)
		u_form = UserCancelForm(instance=obj)
		if request.user.is_nonteacher:
			form = NonTeacherApplyForm( instance=obj)
		else:
			form = TeacherApplyForm( instance=obj)
	context = {
		'obj' : obj,
		'u_form' : u_form,
		'form' : form,
		'g_form': g_form,
		'applicant':applicant,
		'nonteacherform':nonteacherform,
		'teacherform':teacherform
	}
	return render(request, 'users/alldetailview.html', context)

@login_required
def documentlistview(req):
	# allteacher = User.objects.filter(is_teacher = True)
	# allnonteacher = User.objects.filter(is_nonteacher = True)

	# teacherqueryset = LeaveApplication.objects.filter(user = allteacher) # list of objects
	# nonteacherqueryset = LeaveApplication.objects.filter(user = allnonteacher)

	queryset = LeaveApplication.objects.filter(Q(attachmentrequired=True) & Q(attachmentreceived=False)).order_by('startdate')
	# myFilter = LeaveApplicationFilter(req.GET, queryset=queryset)

	# queryset = myFilter.qs

	context = {
		# "myFilter" : myFilter,
		"objec_list" : queryset,
	}
	return render(req, "users/documentlistview.html", context)


@login_required
def documentdetailview(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)

	if request.method == 'POST':
		u_form = DocumentForm(request.POST, instance=obj)
		if u_form.is_valid(): 	
			u_form.save()
			messages.success(request, f'Sucessfully Saved')
			return redirect('documentlistview')
	
	else:
		u_form = DocumentForm(instance=obj)
	context = {
		'obj' : obj,
		'u_form' : u_form
	}
	return render(request, 'users/documentdetailview.html', context)

@login_required
def calendarlistview(req):
	queryset = LeaveApplication.objects.filter(Q(calendarcheck=False) & ~Q(nonteachertimeofftype="Overtime")).order_by('startdate')
	# myFilter = LeaveApplicationFilter(req.GET, queryset=queryset)

	# queryset = myFilter.qs

	context = {
		# "myFilter" : myFilter,
		"objec_list" : queryset,
	}
	return render(req, "users/calendarlistview.html", context)

@login_required
def calendardetailview(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)

	if request.method == 'POST':
		u_form = CalendarForm(request.POST, instance=obj)
		if u_form.is_valid(): 	
			u_form.save()
			messages.success(request, f'Sucessfully Saved')
			return redirect('calendarlistview')
	
	else:
		u_form = CalendarForm(instance=obj)
	context = {
		'obj' : obj,
		'u_form' : u_form
	}
	return render(request, 'users/calendardetailview.html', context)

@login_required
def prependinglistview(req):
	queryset = LeaveApplication.objects.filter(finalstatus = 'Action Required') # list of objects
	context = {
		"objec_list" : queryset
	}
	return render(req, "users/prependinglistview.html", context)

@login_required
def prependingdetailview(request, myid):
	obj = get_object_or_404(LeaveApplication, id =myid)
	obj = LeaveApplication.objects.get(id=myid)
	if request.method == 'POST':	
		u_form = ProfileApproveForm(request.POST)
								# instance=request.user)
		# Emergency Approved 
		if u_form.is_valid():
			obj.firststatus = 'Approved'
			obj.secondstatus = 'Approved'
			obj.secretarystatus = 'Pending'
			obj.finalstatus = 'Pending'
			# u_form.save()
			obj.save()
			messages.success(request, f'Success')
			return redirect('prependinglistview')
	
	else:
		u_form = ProfileApproveForm()


		context = {
			'obj' : obj
		}
		return render(request, 'users/prependingdetailview.html', context)
