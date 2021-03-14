from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import datetime 
import math
class MyUserManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user



class User(AbstractBaseUser):
	USERNAME_FIELD = 'email'
	email = models.EmailField(verbose_name='email',max_length=255,unique=True)
	username = models.CharField(max_length= 100, default = '',unique=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_teacher = models.BooleanField('teacher status', default=False)
	is_nonteacher = models.BooleanField('Non teaching staff status', default=False)
	is_supervisor = models.BooleanField('Supervisor status', default=False)
	is_viceprincipal = models.BooleanField('Viceprincipal status', default=False)
	is_principal = models.BooleanField('Principal status', default=False)
	is_secretary = models.BooleanField('Secretary status', default=False)

	REQUIRED_FIELDS = ['username']
	objects = MyUserManager()


	class Types(models.TextChoices):
		TEACHINGSTAFF = 'teachingstaff', 'teachingstaff'
		NONTEACHINGSTAFF = 'nonteachingstaff', 'nonteachingstaff'
		SUPERVISOR = 'supervisor', 'supervisor'
		VICEPRINCIPAL = 'viceprincipal', 'viceprincipal'
		PRINCIPAL = 'principal', 'principal'
		SECRETARY = 'secretary', 'secretary'
	base_type = Types.NONTEACHINGSTAFF
	
	type = models.CharField(_("Types"), max_length=50, choices=Types.choices)

	def save(self, *args, **kwargs):
			if self.type == User.Types.TEACHINGSTAFF:
				self.is_teacher = True
				self.is_nonteacher = False
				self.is_supervisor = False
				self.is_viceprincipal = False
				self.is_principal = False
				self.is_secretary = False
			elif self.type == User.Types.NONTEACHINGSTAFF:
				self.is_teacher = False
				self.is_nonteacher = True
				self.is_supervisor = False
				self.is_viceprincipal = False
				self.is_principal = False
				self.is_secretary = False
			elif self.type == User.Types.SUPERVISOR:
				# self.is_teacher = True
				# self.is_nonteacher = False
				self.is_supervisor = True
				self.is_viceprincipal = False
				self.is_principal = False
				self.is_secretary = False
			elif self.type == User.Types.VICEPRINCIPAL:
				self.is_teacher = True
				self.is_nonteacher = False
				self.is_supervisor = False
				self.is_viceprincipal = True
				self.is_principal = False
				self.is_secretary = False
			elif self.type == User.Types.PRINCIPAL:
				self.is_teacher = True
				self.is_nonteacher = False
				self.is_supervisor = False
				self.is_viceprincipal = False
				self.is_principal = True
				self.is_secretary = False
			elif self.type == User.Types.SECRETARY:
				self.is_teacher = False
				self.is_nonteacher = True
				self.is_supervisor = False
				self.is_viceprincipal = False
				self.is_principal = False
				self.is_secretary = True
			return super(User, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse("users:detail", kwargs={"username": self.username})
		
	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin


class TeachingStaffManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super().get_queryset(*args, **kwargs).filter(type = User.Types.TEACHINGSTAFF)

class NonTeachingStaffManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super().get_queryset(*args, **kwargs).filter(type = User.Types.NONTEACHINGSTAFF)
class SupervisorManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super().get_queryset(*args, **kwargs).filter(type = User.Types.SUPERVISOR)

class VicePrincipalManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super().get_queryset(*args, **kwargs).filter(type = User.Types.VICEPRINCIPAL)

class PrincipalManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super().get_queryset(*args, **kwargs).filter(type = User.Types.PRINCIPAL)

class SecretaryManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super().get_queryset(*args, **kwargs).filter(type = User.Types.SECRETARY)

class Secretary(User):
	base_type = User.Types.SECRETARY
	objects = SecretaryManager()
	
	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		if not self.pk:
			self.type = self.base_type
		return super().save(*args, **kwargs)

class TeachingStaff(User):
	base_type = User.Types.TEACHINGSTAFF
	objects = TeachingStaffManager()

	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		if not self.pk:
			self.type = self.base_type
		return super().save(*args, **kwargs)

class NonTeachingStaff(User):
	base_type = User.Types.NONTEACHINGSTAFF
	objects = NonTeachingStaffManager()
	
	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		if not self.pk:
			self.type = self.base_type
		return super().save(*args, **kwargs)



class Supervisor(User):
	base_type = User.Types.SUPERVISOR
	objects = SupervisorManager()

	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		if not self.pk:
			self.type = self.base_type
		return super().save(*args, **kwargs)

class VicePrincipal(User):
	base_type = User.Types.VICEPRINCIPAL
	objects = VicePrincipalManager()

	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		if not self.pk:
			self.type = self.base_type
		return super().save(*args, **kwargs)

class Principal(User):
	base_type = User.Types.PRINCIPAL
	objects = PrincipalManager()

	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		if not self.pk:
			self.type = self.base_type
		return super().save(*args, **kwargs)

class TeachingStaffDetail(models.Model):
	user = models.OneToOneField(TeachingStaff, on_delete=models.CASCADE)
	sickleave = models.DecimalField(_("Sick Leave Balance"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(168)])
	maxsickleave = models.DecimalField(_("Max. Sick Leave"),max_digits = 4, decimal_places = 1, default = 168, validators=[ MinValueValidator(0), MaxValueValidator(168)])
	sickleavecounter = models.DecimalField(_("Sick Leave Taken (Start from 0 each year)"),max_digits = 60, decimal_places = 1, default = 0)
	casualleave = models.DecimalField(_("Casual Leave Balance"),max_digits = 3, decimal_places = 2, default = 2, validators=[ MinValueValidator(0), MaxValueValidator(20)])
	firstday = models.DateField(default=timezone.now())
	increment = models.DecimalField(_("Sick Leave Increment"),default = 0, max_digits = 2, decimal_places = 0)
	is_teacher = models.BooleanField('teacher status', default=True)
	is_viceprincipal = models.BooleanField('Viceprincipal status', default=False)
	is_principal = models.BooleanField('Principal status', default=False)

	def __str__(self):
		return self.user.username

class NonTeachingStaffDetail(models.Model):
	user = models.OneToOneField(NonTeachingStaff, on_delete=models.CASCADE, null=True, blank=True, related_name='NonTeachingStaffDetail')
	supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True, blank=True, related_name='supervisor')
	viceprincipal = models.ForeignKey(VicePrincipal, on_delete=models.CASCADE, null=True, blank=True, related_name='viceprincipal')
	sickleave = models.DecimalField(_("Sick Leave Balance"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(168)])
	maxsickleave = models.DecimalField(_("Max. Sick Leave"),max_digits = 4, decimal_places = 1, default = 128, validators=[ MinValueValidator(0), MaxValueValidator(168)])
	sickleavecounter = models.DecimalField(_("Sick Leave Taken (Start from 0 each year)"),max_digits = 60, decimal_places = 1, default = 0)
	annualleave = models.DecimalField(_("Annual Leave Balance"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(100)])
	maxannualleave = models.DecimalField(_("Annual Leave (AL Balance last yr + AL Granted this yr)"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(100)])

	compensatedleave = models.DecimalField(_("Overtime Balance (Hours)"),max_digits = 4, decimal_places = 2, default = 0)
	ratio = models.DecimalField(_("Non-Teaching Ratio (100% nonteaching = 1)"),max_digits = 4, decimal_places = 3, default = 0)
	increment = models.DecimalField(_("Sick Leave Increment"),default = 0, max_digits = 2, decimal_places = 0)
	firstday = models.DateField(default=timezone.now())
	is_nonteacher = models.BooleanField('Non teaching staff status', default=True)
	is_secretary = models.BooleanField('Secretary status', default=False)

	def __str__(self):
		return self.user.username

class SecretaryDetail(models.Model):
	user = models.OneToOneField(Secretary, on_delete=models.CASCADE)
	sickleave = models.DecimalField(_("Sick Leave Balance"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(168)])
	maxsickleave = models.DecimalField(_("Max. Sick Leave"),max_digits = 4, decimal_places = 1, default = 128, validators=[ MinValueValidator(0), MaxValueValidator(128)])
	sickleavecounter = models.DecimalField(_("Sick Leave Taken (Reset to 'zero' each year)"),max_digits = 60, decimal_places = 1, default = 0)
	annualleave = models.DecimalField(_("Annual Leave Balance"),max_digits = 3, decimal_places = 2, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(20)])
	maxannualleave = models.DecimalField(_("Max. Annual Leave"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(100)])

	compensatedleave = models.DecimalField(_("Compensated Leave Available (Hours)"),max_digits = 4, decimal_places = 1, default = 0)
	ratio = models.DecimalField(_("Non-Teaching Ratio (100% nonteaching = 1)"),max_digits = 4, decimal_places = 3, default = 0)
	increment = models.DecimalField(_("Sick Leave Increment"),default = 0, max_digits = 2, decimal_places = 0)
	firstday = models.DateField(default=timezone.now())
	is_nonteacher = models.BooleanField('Non teaching staff status', default=True)
	is_secretary = models.BooleanField('Secretary status', default=True)

	def __str__(self):
		return self.user.username

class SupervisorDetail(models.Model):
	user = models.OneToOneField(Supervisor, on_delete=models.CASCADE, null=True, blank=True, related_name='SupervisorDetail')
	overseeing = models.ManyToManyField(NonTeachingStaff, related_name='overseeing', null=True, blank=True)
	sickleave = models.DecimalField(_("Sick Leave Balance"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(168)])
	maxsickleave = models.DecimalField(_("Max. Sick Leave"),max_digits = 4, decimal_places = 1, default = 168, validators=[ MinValueValidator(0), MaxValueValidator(168)])
	sickleavecounter = models.DecimalField(_("Sick Leave Taken (Reset to 'zero' each year)"),max_digits = 60, decimal_places = 1, default = 0)
	casualleave = models.DecimalField(_("Casual Leave Balance (For Teacher only)"),max_digits = 3, decimal_places = 2, default = 2, validators=[ MinValueValidator(0), MaxValueValidator(20)])
	annualleave = models.DecimalField(_("Annual Leave Balance (For Non-Teacher only)"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(100)])
	maxannualleave = models.DecimalField(_("Annual Leave (AL Balance last yr + AL Granted this yr) (For Non-Teacher only)"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(100)])

	compensatedleave = models.DecimalField(_("Overtime Balance (Hours) (For Non-Teacher only)"),max_digits = 4, decimal_places = 1, default = 0)
	ratio = models.DecimalField(_("Non-Teaching Ratio (100% nonteaching = 1) (For Non-Teacher only)"),max_digits = 4, decimal_places = 3, default = 0)

	firstday = models.DateField(default=timezone.now())
	increment = models.DecimalField(_("Sick Leave Increment"),default = 0, max_digits = 2, decimal_places = 0)
	is_supervisor = models.BooleanField('Supervisor status', default=True)
	is_teacher = models.BooleanField('Teacher status', default=False)
	is_nonteacher = models.BooleanField('Non teaching staff status', default=False)
	def __str__(self):
		return self.user.username
class VicePrincipalDetail(models.Model):
	user = models.OneToOneField(VicePrincipal, on_delete=models.CASCADE,null=True, blank=True, related_name='VicePrincipalDetail')
	sickleave = models.DecimalField(_("Sick Leave Balance"),max_digits = 4, decimal_places = 1, default = 0, validators=[ MinValueValidator(0), MaxValueValidator(168)])
	maxsickleave = models.DecimalField(_("Max. Sick Leave"),max_digits = 4, decimal_places = 1, default = 168, validators=[ MinValueValidator(0), MaxValueValidator(168)])
	sickleavecounter = models.DecimalField(_("Sick Leave Taken (Reset to 'zero' each year)"),max_digits = 60, decimal_places = 1, default = 0)
	casualleave = models.DecimalField(_("Casual Leave Balance"),max_digits = 3, decimal_places = 2, default = 2, validators=[ MinValueValidator(0), MaxValueValidator(20)])
	firstday = models.DateField(default=timezone.now())
	increment = models.DecimalField(_("Sick Leave Increment"),default = 0, max_digits = 2, decimal_places = 0)
	is_teacher = models.BooleanField('teacher status', default=True)
	is_viceprincipal = models.BooleanField('VicePrincipal status', default=True)
	allvp = models.ManyToManyField(VicePrincipal, related_name='allvp')
	def __str__(self):
		return self.user.username
class PrincipalDetail(models.Model):
	user = models.OneToOneField(Principal, on_delete=models.CASCADE,null=True, blank=True, related_name='PrincipalDetail')
	is_teacher = models.BooleanField('teacher status', default=True)
	is_principal = models.BooleanField('Principal status', default=True)

class LeaveApplication(models.Model):
	sickleave = 'Sick Leave'
	officialleave_inschool= 'Official Leave (In School)'
	officialleave_outside= 'Official Leave (Outside)'
	casualleave = 'Casual Leave'
	annualleave = 'Annual Leave'
	specialtuberculosisleave = 'Special Tuberculosis Leave'
	maternalleave = 'Maternal Leave'
	nopayleave = 'No-Pay Leave'
	paternityleave = 'Paternity Leave'
	studyleave = 'Study Leave'
	jurorsorwitnesses = 'Jurors or Witnesses'
	leaveforspecialevents = 'Leave for Special Events'
	overtime = 'Overtime'
	overtimecompensatory = 'Overtime Compensatory Leave'
	others = 'Others'
	first = '1st'
	second = '2nd'
	third = '3rd'
	forth = '4th'
	fifth = '5th'
	sixth = '6th'
	seventh = '7th'
	eighth = '8th'
	ninth = '9th'
	allday = 'Whole Day'
	TEACHER_TIMEOFF_CHOICES = [
		(sickleave, 'Sick Leave'),
		(officialleave_inschool, 'Official Leave (In School)'),
		(officialleave_outside, 'Official Leave (Outside)'),
		(casualleave, 'Casual Leave'),
		(specialtuberculosisleave, 'Special Tuberculosis Leave'),
		(maternalleave, 'Maternal Leave'),
		(nopayleave , 'No-Pay Leave'),
		(paternityleave, 'Paternity Leave'),
		(studyleave, 'Study Leave'),
		(jurorsorwitnesses, 'Jurors or Witnesses'),
		(leaveforspecialevents, 'Leave for Special Events'),
		(others, 'Others'),
	]

	NONTEACHER_TIMEOFF_CHOICES = [
		(sickleave, 'Sick Leave'),
		(officialleave_inschool, 'Official Leave (In School)'),
		(officialleave_outside, 'Official Leave (Outside)'),
		(annualleave, 'Annual Leave'),
		(overtime, 'Overtime'),
		(overtimecompensatory, 'Overtime Compensatory Leave'),		
		(specialtuberculosisleave, 'Special Tuberculosis Leave'),
		(maternalleave, 'Maternal Leave'),
		(nopayleave , 'No-Pay Leave'),
		(paternityleave, 'Paternity Leave'),
		(jurorsorwitnesses, 'Jurors or Witnesses'),
		(others, 'Others'),
	]

	ALL_TIMEOFF_CHOICES = [
		(sickleave, 'Sick Leave'),
		(officialleave_inschool, 'Official Leave (In School)'),
		(officialleave_outside, 'Official Leave (Outside)'),
		(annualleave, 'Annual Leave'),
		(casualleave, 'Casual Leave'),
		(overtime, 'Overtime'),
		(overtimecompensatory, 'Overtime Compensatory Leave'),
		(specialtuberculosisleave, 'Special Tuberculosis Leave'),
		(maternalleave, 'Maternal Leave'),
		(nopayleave , 'No-Pay Leave'),
		(paternityleave, 'Paternity Leave'),
		(studyleave, 'Study Leave'),
		(jurorsorwitnesses, 'Jurors or Witnesses'),
		(leaveforspecialevents, 'Leave for Special Events'),
		(others, 'Others'),
	]

	NONTEACHER_CHANGE_TIMEOFF_CHOICES = [
		(annualleave, 'Annual Leave'),
		(overtimecompensatory, 'Overtime Compensatory Leave'),		
		(nopayleave , 'No-Pay Leave'),
	]

	TEACHER_CHANGE_TIMEOFF_CHOICES = [
		(casualleave, 'Casual Leave'),		
		(nopayleave , 'No-Pay Leave'),
	]

	OFFICIAL_TIMEOFF_CHOICES = [
		(officialleave_inschool, 'Official Leave (In School)'),
		(officialleave_outside, 'Official Leave (Outside)'),
	]

	EMERGENCY_TIMEOFF_CHOICES = [
		(sickleave, 'Sick Leave'),		
		(annualleave, 'Annual Leave'),
		(casualleave, 'Casual Leave'),
	]

	pending = 'Pending'
	approved = 'Approved'
	denied = 'Denied'
	canceled = 'Canceled'
	STATUS_CHOICES = [
		(pending, 'Pending'),
		(approved, 'Approved'),
		(denied, 'Denied'),
		(canceled, 'Canceled')
		# (action_required, 'Action Required')
	]

	teacher = 'Teacher'
	nonteacher = 'Nonteacher'

	STAFF_TYPE_CHOICES = [
		(teacher, 'Teacher'),
		(nonteacher, 'Nonteacher'),
	]

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
		(allday, 'Whole Day')
	]


	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	created_at_date = models.DateField(auto_now_add=True, blank=True)
	updated_at = models.DateField( null=True, blank=True)
	stafftype = models.CharField(_("Staff Type"),max_length= 100,choices = STAFF_TYPE_CHOICES, default=nonteacher)
	emergencytype = models.CharField(_("Type of Leave"),max_length= 100,choices = EMERGENCY_TIMEOFF_CHOICES, default=sickleave)
	emergencystatus = models.BooleanField('Emergency apply status', default=False)
	officialtype = models.CharField(_("Type of Leave"),max_length= 100,choices = OFFICIAL_TIMEOFF_CHOICES, default=officialleave_inschool)
	appliedby = models.ForeignKey( User, on_delete=models.CASCADE, null=True, blank=True, related_name='appliedby')
	groupapplystatus = models.BooleanField('Group apply status', default=False)
	alltimeofftype = models.CharField(_("All Type of Leave"),max_length= 100,choices = ALL_TIMEOFF_CHOICES, default=sickleave)
	teachertimeofftype = models.CharField(_("Type of Leave"),max_length= 100,choices = TEACHER_TIMEOFF_CHOICES, default=sickleave)
	nonteachertimeofftype = models.CharField(_("Type of Leave"),max_length= 100,choices = NONTEACHER_TIMEOFF_CHOICES, default=sickleave)
	nonteacherchangetimeofftype = models.CharField(_("Change Leave Type"),max_length= 100,choices = NONTEACHER_CHANGE_TIMEOFF_CHOICES, null=True, blank=True)
	teacherchangetimeofftype = models.CharField(_("Change Leave Type"),max_length= 100,choices = TEACHER_CHANGE_TIMEOFF_CHOICES, null=True, blank=True)
	startdate = models.DateField(default=timezone.now())
	starttime = models.TimeField(default=timezone.now(), null=True)
	enddate = models.DateField(default=timezone.now())
	endtime = models.TimeField(default=timezone.now(), null=True)
	duration = models.DecimalField(_("Total Days"),default = 0, max_digits = 10, decimal_places = 2)
	totalhr = models.DecimalField(_("Total Hours"),default = 0, max_digits = 65, decimal_places = 0)
	period = models.CharField(_("Period"),max_length= 100,null=True, blank=True)

	reason = models.CharField(max_length= 200, default = '')
	file = models.FileField(null = True, blank = True)
	attachmentrequired = models.BooleanField('Attachment Required', default=False)
	attachmentreceived = models.BooleanField('Attachment Received', default=False)
	calendarcheck = models.BooleanField('calendar check', default=False)
	firststatus = models.CharField(_("Decision"),max_length= 20,choices = STATUS_CHOICES, default=pending)
	firstapprovedby = models.ForeignKey( User, on_delete=models.CASCADE, null=True, blank=True, related_name='firstapprovedby')
	firstcomment = models.CharField(_("Comment"),max_length= 200, blank=True)
	secondstatus = models.CharField(_("Decision"),max_length= 20,choices = STATUS_CHOICES, default=pending)
	secondapprovedby = models.ForeignKey( User, on_delete=models.CASCADE, null=True, blank=True, related_name='secondapprovedby')
	secondcomment = models.CharField(_("Comment"),max_length= 200, blank=True)
	secretarystatus = models.CharField(_("Decision"),max_length= 20,choices = STATUS_CHOICES, default=pending)
	secretaryduration = models.DecimalField(_("Modified duration (hr for OT, else use days)"),max_digits = 4, decimal_places = 2, null=True, blank=True)
	secretarycomment = models.CharField(_("Comment"),max_length= 200, blank=True)
	finalstatus = models.CharField(_("Decision"),max_length= 20,choices = STATUS_CHOICES, default=pending)
	finalduration = models.DecimalField(_("Modified duration (hr for OT, else use days)"),max_digits = 4, decimal_places = 2, null=True, blank=True)
	finalcomment = models.CharField(_("Comment"),max_length= 200, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	users = models.ManyToManyField(User, related_name='users')


	pickvp = models.ForeignKey( User, on_delete=models.CASCADE, null=True, blank=True, related_name='pickvp')
	pickmanager = models.ForeignKey( User, on_delete=models.CASCADE, null=True, blank=True, related_name='pickmanager')
	
	class Meta:
	   ordering = ['-created_at']

	# def __str__(self):
	# 	return self.user.username



	def get_absolute_url(self):
		return  reverse("managerapprove", kwargs={"myid" : self.id})  #f"/timeoff/{self.id}"

class Picker(models.Model):
	pickuser = models.ManyToManyField( User, related_name='pickuser')

class IncrementAll(models.Model):
	created_at = models.DateField(default=timezone.now())
	added = models.DecimalField(default = 0, max_digits = 2, decimal_places = 0)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
		