from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('S', 'Student'),
        ('A', 'Alumni'),
        ('C', 'Company'),
        ('F', 'Admin')
    )
    user_role = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, blank=False, null=False, verbose_name='Role', default='F')
    user_contact = models.IntegerField(verbose_name='Contact', default='0')
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.username

class Student(User):
    roll_no = models.CharField(max_length=9, verbose_name='Roll Number')
    dept = models.CharField(max_length=30, verbose_name='Department')
    CV = models.FileField(upload_to='resume/', verbose_name='Resume')

    class Meta:
        db_table = 'student'

class Alumni(User):
    graduating_year = models.IntegerField(verbose_name='Graduating Year')
    dept = models.CharField(max_length=30, verbose_name='Department')

    class Meta:
        db_table = 'alumnus'
        verbose_name_plural = 'alumni'

class Company(User):
    company_name = models.CharField(max_length=30, verbose_name='Company Name')
    desc = models.CharField(max_length=255, verbose_name='Company Description')
    
    class Meta:
        db_table = 'company'
        verbose_name_plural = 'companies'

class Notification(models.Model):
    message = models.CharField(max_length=255)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-posted_on',)

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)