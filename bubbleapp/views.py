from django.shortcuts import render
from .models import Category,Subcategory,Transaction
from .forms import CategoryForm,TransactionForm,ReportForm
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.db.models import Sum
# Create your views here.


def index(request):
    #Home page
    context={}
    return render(request,'index.html',context)


def categories(request):
    #Page with categories
    categories=Category.objects.order_by('name')
    context={'categories':categories}
    return render(request, 'categories.html',context)


def new_category(request):
    #Adding of new category
    if request.method != 'POST':
        # Дані не відправлялися, створюється нова формв
        form = CategoryForm()
    else:
        # Відправлені дані POST: обробити дані
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('categories'))
    context = {'form': form}
    return render(request, 'new_category.html', context)


def edit_category(request,category_id):
    #Editing existing category
    category = Category.objects.get(id=category_id)
    if request.method != 'POST':
        # Початковий запит. Форма заповнюється наявними даними.
        form = CategoryForm(instance=category)
    else:
        # Відправка даних POST. Обробити дані.
        form = CategoryForm(instance=category,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('categories'))
    context = {'category': category,'form': form}
    return render(request, 'edit_category.html', context)


def delete_category(request,category_id):
    # Deleting existing category
    Category.objects.filter(id=category_id).delete()
    return HttpResponseRedirect(reverse('categories'))


def transactions(request):
    #Shows transactions
    transactions=Transaction.objects.order_by('-date')
    context={'transactions':transactions}
    return render(request, 'transactions.html',context)


def new_transaction(request,transaction_id=0):
    #Adds/changes new transaction
    if transaction_id:
        transaction = Transaction.objects.get(id=transaction_id)
        if request.method != 'POST':
            # Початковий запит. Форма заповнюється наявними даними.
            form = TransactionForm(instance=transaction)
        else:
            # Відправка даних POST. Обробити дані.
            form = TransactionForm(instance=transaction, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('transactions'))
        context = {'transaction': transaction, 'form': form}
        return render(request, 'new_transaction.html', context)
    else:
        if request.method != 'POST':
            # Дані не відправлялися, створюється нова формв
            form = TransactionForm()
        else:
            # Відправлені дані POST: обробити дані
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('transactions'))
        context = {'form': form}
        return render(request, 'new_transaction.html', context)


def delete_transaction(request,transaction_id):
    # Deleting existing transaction
    Transaction.objects.filter(id=transaction_id).delete()
    return HttpResponseRedirect(reverse('transactions'))


def about(request):
    #Shows page with information about site
    form=ReportForm()
    context={'form':form}
    return render(request,'contact_form.html',context)


def report(request):
    #Form with report
    if request.method != 'POST' or ('reset' in request.POST):
        # Дані не відправлялися, створюється нова формв
        form = ReportForm()
    else:
        # Відправлені дані POST: обробити дані
        form = ReportForm(request.POST)
        if form.is_valid():
            context = graph_parameters(form.cleaned_data)
            if 'by date' in request.POST:
                return render(request, 'report_line_chart.html', context)
            else: #if 'graph' in request.POST
                return render(request, 'report_pie_chart.html', context)

    context={'form':form}
    return render(request,'report_form.html',context)


def display_meta(request):
    values = request.META.items()

    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def graph_parameters(params):
    #Takes parameters in request.POST and returns data for Line and Pie Charts
    dates = []
    values_by_day = []
    chart_categories_names=[]
    chart_categories_values=[]
    results=Transaction.objects.filter(date__gte=params['date1'])\
        .filter(date__lte=params['date2'])
    if params['operation_type']:
        results=results.filter(operation_type__exact=params['operation_type'])
    results_by_category = results
    if params['category']:
        results=results.filter(trans__id__exact=params['category'])
    #Makes label for operation type for search
    operation_type=params['operation_type']
    if operation_type==1:
        operation_type='Витрати'
    else:
        operation_type = 'Доходи'
    #Make categories name
    category=params['category']
    if category:
        category=Category.objects.get(id=category).name
    else:
        category='Усі категорії'
    # Make sorted list for all dates:
    for result in results:
        dates.append(str(result.date))
    for res in results_by_category:
        chart_categories_names.append(res.name_of_Category())
    dates=list(set(dates))
    dates.sort()
    chart_categories_names=list(set(chart_categories_names))
    chart_categories_names.sort()
    # Make period
    period = str(params['date1']) + '  --  ' + str(params['date2'])
    #Make Sum for all dates:
    for date in dates:
        sum=results.filter(date__exact=date).aggregate(Sum('money'))['money__sum']
        values_by_day.append(str(int(sum*100)/100))
    for cat in chart_categories_names:
        sum = results_by_category.filter(trans__name__exact=cat).aggregate(Sum('money'))['money__sum']
        chart_categories_values.append(str(int(sum*100)/100))
    #SELECT category.name, sum(money) FROM results group by category.name
    sum_by_categories=results_by_category.values('trans__name').annotate(Sum('money'))
    sum=results_by_category.values('trans__name').aggregate(money=Sum('money'))
    # Making string with values for convertion in chart script:
    dates = ' '.join(dates)
    values_by_day = ' '.join(values_by_day)
    chart_categories_names=' '.join(chart_categories_names)
    chart_categories_values=' '.join(chart_categories_values)
    #At least:... =)
    context={'dates':dates,'values_by_day':values_by_day,'operation_type1':operation_type,'period':period,
             'category':category,'chart_categories_names':chart_categories_names,'sum':sum,
             'chart_categories_values':chart_categories_values,'sum_by_categories':sum_by_categories}
    return context


