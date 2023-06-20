from django.shortcuts import render

# Create your views here.

from django.db import connection

def StateMapView(request):
    cursor = connection.cursor()
    cursor.execute("EXEC [rpt_GetSalesReportByState]")
    data = cursor.fetchall()
    cursor1 = connection.cursor()
    cursor1.execute("EXEC [rpt_GetSalesReportByStateIfNotNull]")
    avalable_sale = cursor1.fetchall()
    chart_data = [['State', 'Sales']]
    for row in data:
        state = row[0]
        sales = row[1]
        chart_data.append([state, sales])
    context = {
        'chart_data': chart_data,
        'avalable_sale':avalable_sale,
    }
    return render(request, 'SalesInIndiaMap.html',context=context)
