from django import  forms
from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic       #指定模型配置表单
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}