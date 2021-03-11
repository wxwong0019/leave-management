from django.db import models
from django.urls import reverse
from django.utils import timezone
# from datetime import datetime

# Create your models here.
class Timeoff(models.Model):
	title		= models.CharField(max_length =50)
	name		= models.CharField(max_length =50, default="input")
	description	= models.TextField(blank=True, null=False, default='testing')
	date 		= models.DateField(default=timezone.now())
	email 		= models.EmailField(default='default@test.edu')



	def get_absolute_url(self):
		return  reverse("timeoff:timeoff-detail", kwargs={"myid" : self.id})  #f"/timeoff/{self.id}"
