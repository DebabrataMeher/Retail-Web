from django.shortcuts import render
from django.db import connection


def index(request):
    return render(request, 'index.html')


def sales(request):
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
        document_no = request.POST.get('document_no')
        product_name = request.POST.get('product_name')
        customer_name = request.POST.get('customer_name')
        barcode = request.POST.get('barcode')
        from_date = request.POST.get('date')
        to_date = request.POST.get('date1')
        with connection.cursor() as cursor:
            cursor.execute("EXEC rpt_SalesProducts @company_id = %s , @customer_name = %s , @from_date = %s , @to_date = %s , @document_no = %s , @product_name = %s , @barcode = %s , @sales_or_return = %s", [company_id,customer_name,from_date,to_date,document_no,product_name,barcode,'sales'])
            results = cursor.fetchall()
            SalesProducts = [(row[1], row[2]) for row in results]    
            cursor.execute("EXEC rpt_SalesProducts @company_id = %s , @customer_name = %s , @from_date = %s , @to_date = %s , @document_no = %s , @product_name = %s , @barcode = %s , @sales_or_return = %s", [company_id,customer_name,from_date,to_date,document_no,product_name,barcode,'return'])
            results = cursor.fetchall()
            ReturnProducts = [(row[1], row[3]) for row in results] 
            cursor.execute("EXEC rpt_SalesDocuments @company_id = %s , @customer_name = %s , @fromDate = %s , @toDate = %s , @document_no = %s ,  @sales_or_return = %s", [company_id,customer_name,from_date,to_date,document_no,'sales'])
            results = cursor.fetchall()
            SalesDocuments = [(row[1], row[18]) for row in results]  
            cursor.execute("EXEC rpt_SalesDocuments @company_id = %s , @customer_name = %s , @fromDate = %s , @toDate = %s , @document_no = %s ,  @sales_or_return = %s", [company_id,customer_name,from_date,to_date,document_no,'return'])
            results = cursor.fetchall()
            ReturnDocuments = [(row[1], row[18]) for row in results]    
            context = {
                    "SalesProducts": SalesProducts,
                    "ReturnProducts": ReturnProducts,
                    "SalesDocuments":SalesDocuments,
                    "ReturnDocuments":ReturnDocuments,
                   }              
        return render(request, 'sales.html', context=context)
    else:
        return render(request, 'sales.html', context=context)
