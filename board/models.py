from django.db import models

# Create your models here.
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    """
    Category for Post instance
    """
    name = models.CharField(verbose_name= '이름', max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '카테고리'
        verbose_name = '카테고리'


class Post(models.Model):
    """
    Post of board
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name= '작성자',on_delete=models.CASCADE, null=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    create_date = models.DateTimeField(verbose_name= '작성일자', auto_now= True)
    modify_date = models.DateTimeField(verbose_name= '수정일자',null=True, blank=True)
    title = models.TextField() # deprecated
    content = models.TextField(verbose_name='내용')
    category = models.ForeignKey(Category, verbose_name= '카테고리', on_delete=models.CASCADE, null = True, blank = True)
    #notice = models.BooleanField(verbose_name= "상단고정게시물", null=True, blank=True)





    def __str__(self):
        return self.content

    class Meta:
        # 복수형 저장. 관리자페이지에서 이 이름으로 보인다
        verbose_name = '게시글'
        verbose_name_plural = '게시글'