from distutils.archive_util import make_archive
from django.db import models
from authentication.models import User
# Create your models here.


class EventGroup(models.Model):
    # 이게... 모든 event의 subclass에도 똑같이?
    # 휴가에도 종류가 있음
    # 구분이 필요함.
    # privateEvent, Vacation, Task

    TYPE_CHOICES = (
        ('Ev', 'Event'),
        ('Va', 'Vacation'),
        ('Ta', 'Task'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    name = models.CharField(max_length=20)
    color = models.CharField(verbose_name="color", max_length=7)
    # for private event
    user = models.ForeignKey(User, on_delete= models.CASCADE, blank=True, null = True)
    is_private = models.BooleanField()
    # user, name, color ? 
        # private event
    # public event (휴가 / 업무 등)
    # public event를 추가할 때는 public eventgroup만 가져오고
    # private event를 추가할 때는 private group만 가져와야 함. 근데 user 추가


class Event(models.Model):
    """
    1) user와 many-to-many https://stackoverflow.com/questions/33182092/django-rest-framework-serializing-many-to-many-field
    2) 색상
    3) 
        # id: '1', # 있음
        # calendarId: '0', # group임
        # title: 'TOAST UI Calendar Study', # 없음. 필요 
        # category: 'time', # 이건 computed attribute로 넣자
        # dueDateClass: '', # ? 
        # start: today.toISOString(), # 있음
        # end: getDate('hours', today, 3, '+').toISOString() # 있음
    """
    
    start = models.DateTimeField(verbose_name="from")
    end = models.DateTimeField(verbose_name="to")
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    relatedPeople = models.ManyToManyField(User, related_name= 'people')
    group = models.ForeignKey(EventGroup, on_delete= models.CASCADE, null= True)
    title = models.CharField(max_length= 50)
    description = models.TextField(default = "", blank= True, null= True)
    


class Vacation(Event):
    isPermmitted = models.BooleanField(default= False)
    


