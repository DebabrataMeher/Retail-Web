from django.shortcuts import render
from django.db import connection
from .models import tbl_SalesProjections
from datetime import datetime


def save_sales_projection(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tbl_SalesProjections")
    get_sales_projection = cursor.fetchall()
    context = {
        'get_sales_projection': get_sales_projection,
    }
    selected_row_data = None
    if request.method == 'POST':
        projection_title = request.POST.get('projection_title')
        filter_start_date = request.POST.get('filter_start_date')
        filter_end_date = request.POST.get('filter_end_date')
        target_value = request.POST.get('target_value')
        projection = tbl_SalesProjections(
            projection_title=projection_title,
            filter_start_date=filter_start_date,
            filter_end_date=filter_end_date,
            target_value=target_value
        )
        projection.save()
        success_message = "New Projection added successfully."
        context = {
            'get_sales_projection': get_sales_projection,
            'success_message': success_message,
        }
    elif request.method == 'GET' and 'row_id' in request.GET:
        selected_row_id = request.GET.get('row_id')
        selected_row_data = get_sales_projection[int(selected_row_id)]
        filter_start_date = selected_row_data[2]
        filter_end_date = selected_row_data[3]
        start_date = datetime.strptime(str(filter_start_date), "%Y-%m-%d").date()
        end_date = datetime.strptime(str(filter_end_date), "%Y-%m-%d").date()
        num_days = (end_date - start_date).days
        value = 56
        expectedvalue = selected_row_data[4]/num_days
        context = {
        'selected_row_data': selected_row_data,
        'value': value,
        'expectedvalue': expectedvalue,
        }
    return render(request, 'SalesKanban.html', context=context)


from decimal import Decimal, ROUND_HALF_UP
def show_kanban(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tbl_SalesProjections")
    get_sales_projection = cursor.fetchall()
    value = 56
    net_value=0
    expectedvalue = 75
    context = {
        'get_sales_projection': get_sales_projection,
        'value': value,
        'selected_row_data': None,  
        'expectedvalue': expectedvalue,
    }
    selected_row_data = None 
    if request.method == 'GET' and 'row_id' in request.GET:
        selected_row_id = request.GET.get('row_id')
        selected_row_data = get_sales_projection[int(selected_row_id)]
        filter_start_date = selected_row_data[2]
        filter_end_date = selected_row_data[3]
        start_date = datetime.strptime(str(filter_start_date), "%Y-%m-%d").date()
        end_date = datetime.strptime(str(filter_end_date), "%Y-%m-%d").date()
        num_days = (end_date - start_date).days
        cursor1 = connection.cursor()
        cursor1.execute("EXEC [rpt_GetNetValue] @filter_start_date = %s , @filter_end_date = %s" , [start_date, end_date])
        net_value = cursor1.fetchall()
        value = 86
        result = Decimal(selected_row_data[4]) / Decimal(num_days)
        expectedvalue = result.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        context = {
        'selected_row_data': selected_row_data,
        'value': value,
        "net_value":net_value,
        'expectedvalue': expectedvalue,
        'get_sales_projection': get_sales_projection,
        }
    return render(request, 'show_kanban.html', context=context)