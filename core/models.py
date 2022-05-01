from pyexpat import model
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from picklefield.fields import PickledObjectField


from board.models import *
from event.models import *


class Wrapper(models.Model):
    """
    contents wrapper
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name= '작성자',on_delete=models.CASCADE, null=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    create_date = models.DateTimeField(verbose_name= '작성일자', auto_now= True)
    modify_date = models.DateTimeField(verbose_name= '수정일자',null=True, blank=True)
    title = models.CharField(max_length= 50)
    #content = PickledObjectField() # to assign multiple model into one field
    app_name = models.CharField(max_length=20)
    

    # one-to-one field
    post = models.OneToOneField(Post, on_delete= models.CASCADE, null= True, blank= True)
    event = models.OneToOneField(Event, on_delete= models.CASCADE, null= True, blank= True )

class Reply(models.Model):
    """
    Reply for Wrapper class

    Attributes:
        wrapper : upper model for contents wrapping
        author : of the reply
        content : of the reply
        create_date : of the reply
        modify_date : of the reply
    """
    wrapper = models.ForeignKey(Wrapper, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    create_date = models.DateTimeField(verbose_name= '작성일자', auto_now= True)
    modify_date = models.DateTimeField(verbose_name= '수정일자', null=True, blank=True)

class Comment(models.Model):
    """
    Comment for Reply class

    Attributes:
        author : of the reply
        content : of the reply
        create_date : of the reply
        modify_date : of the reply
    """
    reply = models.ForeignKey(Reply, null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(verbose_name= '작성일자')
    modify_date = models.DateTimeField(verbose_name= '수정일자', null=True, blank=True)