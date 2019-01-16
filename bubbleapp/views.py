from django.shortcuts import render
from .models import Category,Subcategory,Transaction
from .forms import CategoryForm,TransactionForm,ReportForm
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.



def index(request):
    #Home page
    context={}
    return render(request,'index.html',context)


@login_required
def categories(request):
    #Page with categories
    # categories=Category.objects.filter(owner=request.user).order_by('name')
    categories = Category.objects.filter(user=request.user).order_by('name')
    context={'categories':categories}
    return render(request, 'categories.html',context)


@login_required
def new_category(request):
    #Adding of new category
    if request.method != 'POST':
        # Дані не відправлялися, створюється нова формв
        form = CategoryForm()
    else:
        # Відправлені дані POST: обробити дані
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category=form.save(commit=False)
            new_category.user=request.user
            new_category.save()
            return HttpResponseRedirect(reverse('bubbleapp:categories'))
    context = {'form': form}
    return render(request, 'new_category.html', context)


@login_required
def edit_category(request,category_id):
    #Editing existing category
    category = Category.objects.get(id=category_id)
    if category.user != request.user:
        raise Http404

    if request.method != 'POST':
        # Початковий запит. Форма заповнюється наявними даними.
        form = CategoryForm(instance=category)
    elif 'reset' in request.POST:
        form = CategoryForm()
    else:
        # Відправка даних POST. Обробити дані.
        form = CategoryForm(instance=category,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bubbleapp:categories'))
    context = {'category': category,'form': form}
    return render(request, 'edit_category.html', context)


@login_required
def delete_category(request,category_id):
    # Deleting existing category
    category = Category.objects.get(id=category_id)
    if category.owner != request.user:
        raise Http404
    Category.objects.filter(id=category_id,owner=request.user).delete()
    return HttpResponseRedirect(reverse('bubbleapp:categories'))


@login_required
def transactions(request):
    #Shows transactions
    transactions=Transaction.objects.filter(user=request.user).order_by('-date')
    context={'transactions':transactions}
    return render(request, 'transactions.html',context)


@login_required
def new_transaction(request,transaction_id=0):
    #Adds/changes new transaction
    if transaction_id:
        transaction = Transaction.objects.get(id=transaction_id)
        if transaction.user != request.user:
            raise Http404
        if request.method != 'POST':
            # Початковий запит. Форма заповнюється наявними даними.
            form = TransactionForm(instance=transaction,user=request.user)
        else:
            # Відправка даних POST. Обробити дані.
            form = TransactionForm(instance=transaction, data=request.POST,user=request.user)
            if form.is_valid():
                new_transaction=form.save(commit=False)
                new_transaction.user = request.user
                new_transaction.save()
                return HttpResponseRedirect(reverse('bubbleapp:transactions'))
        context = {'transaction': transaction, 'form': form}
        return render(request, 'new_transaction.html', context)
    else:
        if request.method != 'POST':
            # Дані не відправлялися, створюється нова формв
            form = TransactionForm(user=request.user)
        else:
            # Відправлені дані POST: обробити дані
            form = TransactionForm(request.POST,user=request.user)
            if form.is_valid():
                new_transaction = form.save(commit=False)
                new_transaction.user = request.user
                new_transaction.save()
                return HttpResponseRedirect(reverse('bubbleapp:transactions'))
        context = {'form': form}
        return render(request, 'new_transaction.html', context)


@login_required
def delete_transaction(request,transaction_id):
    # Deleting existing transaction
    transaction = Transaction.objects.get(id=transaction_id)
    if transaction.user != request.user:
        raise Http404
    Transaction.objects.filter(id=transaction_id).delete()
    return HttpResponseRedirect(reverse('bubbleapp:transactions'))


def about(request):
    #Shows page with information about site
    form=ReportForm()
    context={'form':form}
    return render(request,'about.html',context)


@login_required
def report(request):
    #Form with report
    if request.method != 'POST' or ('reset' in request.POST):
        # Дані не відправлялися, створюється нова форма
        form = ReportForm(user=request.user)
    else:
        # Відправлені дані POST: обробити дані
        form = ReportForm(request.POST,user=request.user)
        if form.is_valid():
            context = graph_parameters(request,form.cleaned_data)
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


def graph_parameters(request,params):
    #Takes parameters in request.POST and returns data for Line and Pie Charts
    dates = []
    values_by_day = []
    chart_categories_names=[]
    chart_categories_values=[]
    results=Transaction.objects.filter(user=request.user).filter(date__gte=params['date1'])\
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


