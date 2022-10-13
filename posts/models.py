
from django.db import models
from django.contrib.auth.models import User




class posts(models.Model):
	user = models.ForeignKey(User, related_name = "OP" ,on_delete=models.CASCADE,blank = True)
	title = models.CharField(max_length = 100)
	post_text = models.TextField(max_length=1000)
	publish_date = models.DateField(auto_now_add=True,editable = True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'posts'



