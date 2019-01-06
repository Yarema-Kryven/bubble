from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=30)
    about=models.CharField(max_length=100)
    class Meta():
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

#-------------------------
class Subcategory(models.Model):
    subcategory=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=50)
    about = models.CharField(max_length=100)
    class Meta():
        verbose_name_plural = 'subcategories'
    def __str__(self):
            return self.name

#-------------------------
class Transaction(models.Model):
    OPERATION_TYPE_CHOICES=((1,'Витрата'),(2,'Прибуток'))
    trans=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    operation_type=models.DecimalField(
        max_digits=1,
        choices=OPERATION_TYPE_CHOICES,
        default=1,decimal_places=0)
    money=models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    date=models.DateField()
    about = models.CharField(max_length=100)

    class Meta():
        verbose_name_plural = 'transactions'

    def name_of_Category(self):
        try:
            name=Category.objects.get(id=self.trans.pk)
        except:
            return 'Відсутня категорія'
        return name.name

    def __str__(self):
            return self.about

    def __add__(self, other):
        if self.operation_type==1:
            return -self.money
        else:
            return self.money