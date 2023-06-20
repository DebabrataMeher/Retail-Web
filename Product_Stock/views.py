from django.shortcuts import render
from django.db import connection

def index(request):
    return render(request, 'index.html')


def stocks(request):
    cursor = connection.cursor()
    cursor3 = connection.cursor()
    cursor.execute("SELECT * FROM tbl_Company_Management ")
    cursor3.execute("EXEC [dbo].[usp_getOutlet_company] ")
    companies = cursor.fetchall()
    outlets=cursor3.fetchall()
    context = {
                   'companies':companies,
                    "outlets":outlets,
                   }
    if request.method == 'POST':
        company_id = request.POST.get('my_input')
        outlet_id = request.POST.get('my_input1')
        document = request.POST.get('document')
        product_name = request.POST.get('product_name')
        barcode = request.POST.get('barcode')
        date = request.POST.get('date')
        date1 = request.POST.get('date1')
        with connection.cursor() as cursor:
            cursor.execute("EXEC rpt_AvailableStock @company_id = %s , @outlet_id = %s ", [company_id,outlet_id])
            results1 = cursor.fetchall()
            avalable = [(row[1], row[4]) for row in results1]       
            cursor.execute("EXEC rpt_LowStock @company_id = %s , @outlet_id = %s ", [company_id,outlet_id])
            results = cursor.fetchall()
            Low_Stock = [(row[1], row[4]) for row in results]    
            cursor.execute("EXEC rpt_StockTransferDocuments @from_date = %s , @to_date = %s , @company_id = %s , @outlet_id = %s , @document_no = %s", [date,date1,company_id,outlet_id,document])
            results = cursor.fetchall()
            Stock_transfer_document = [(row[1], row[7]) for row in results] 
            cursor.execute("EXEC rpt_StockTransferProducts @from_date = %s , @to_date = %s , @company_id = %s , @outlet_id = %s , @document_no = %s", [date,date1,company_id,outlet_id,document])
            results = cursor.fetchall()
            Stock_transfer = [(row[8], row[9]) for row in results] 
            cursor.execute("EXEC rpt_StockAdjustmentManual @company_id = %s , @outlet_id = %s , @product_name = %s , @barcode = %s ", [company_id,outlet_id,product_name,barcode])
            results = cursor.fetchall()
            StockAdjustmentManual = [(row[1], row[5]) for row in results]    
            context = {
                    "avalable": avalable ,
                    "Low_Stock": Low_Stock,
                    "Stock_transfer": Stock_transfer,
                    "Stock_transfer_document":Stock_transfer_document,
                    "StockAdjustmentManual":StockAdjustmentManual,
                   }
        return render(request, 'stocks.html', context=context)
    else:
        return render(request, 'stocks.html', context=context)










