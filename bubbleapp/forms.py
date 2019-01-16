from django import forms
from .models import Category,Transaction
from django.contrib.auth.models import User
import datetime
from bootstrap_datepicker_plus import DatePickerInput

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','about']
        labels={'name':'Назва','about':'Опис'}


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user=kwargs.pop('user')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['trans'].queryset=Category.objects.filter(user=user)
        self.fields['date'].widget=DatePickerInput(attrs={'size':'40'})

    class Meta():
        model=Transaction
        fields=['trans','operation_type','money','date','about']
        labels={'trans':'Категорія','operation_type':'Тип операції',
                'money':'Сума','date':'Дата','about':'Опис'}
        # widgets={'date': DatePickerInput(attrs={'size':'40'}),}


class ReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user=kwargs.pop('user')
        super(ReportForm, self).__init__(*args, **kwargs)
        categories=Category.objects.filter(user=user).values('id','name')
        choices = [[0, '']]
        for category in categories:
            choice=[]
            for key in category:
                choice.append(category[key])
            choices.append(choice)
        self.fields['category']=forms.TypedChoiceField(label='Категорія',choices=choices,coerce=int)

    t=Transaction
    date1=forms.DateField(widget=DatePickerInput(), label='Початкова дата',initial=datetime.date.today)
    date2 = forms.DateField(widget=DatePickerInput(),label='Кінцева дата',initial=datetime.date.today)
    operation_type=forms.TypedChoiceField(label='Тип операції',choices=t.OPERATION_TYPE_CHOICES,coerce=int)
