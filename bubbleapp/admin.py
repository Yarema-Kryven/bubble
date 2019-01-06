from django.contrib import admin
from bubbleapp.models import Category,Subcategory,Transaction

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Transaction)