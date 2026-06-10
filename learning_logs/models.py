from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.text


class Entry(models.Model):
    """学到的关于某个主题的具体知识"""
    #on_delete=models.CASCADE为删除主题时，删除所有关联的条目
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # ✅ 设置后：会显示 "Entries"（正确的英文复数）
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text[:50] + "..."