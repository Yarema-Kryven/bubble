from django import forms
from .models import Category,Transaction
import datetime

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','about']
        labels={'name':'Назва','about':'Опис'}


class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['trans','operation_type','money','date','about']
        labels={'trans':'Категорія','operation_type':'Тип операції',
                'money':'Сума','date':'Дата','about':'Опис'}

class ReportForm(forms.Form):
    t=Transaction
    date1=forms.DateField(label='Початкова дата',initial=datetime.date.today)
    date2 = forms.DateField(label='Кінцева дата',initial=datetime.date.today)
    operation_type=forms.TypedChoiceField(label='Тип операції',choices=t.OPERATION_TYPE_CHOICES,coerce=int)
    categories=Category.objects.values('id','name')
    choices=[[0,'']]
    for category in categories:
        choice=[]
        for key in category:
            choice.append(category[key])
        choices.append(choice)
    category=forms.TypedChoiceField(label='Категорія',choices=choices,coerce=int)