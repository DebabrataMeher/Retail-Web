from django.shortcuts import render
from django.db import connection


def index(request):
    return render(request, 'index.html')


def accounts(request):
    cursor = connection.cursor()
    cursor3 = connection.cursor()
    cursor2 = connection.cursor()
    cursor.execute("SELECT * FROM tbl_Company_Management ")
    cursor2.execute("SELECT * from tbl_Accounts ")
    cursor3.execute("EXEC [dbo].[usp_getOutlet_company] ")
    companies = cursor.fetchall()
    Account=cursor2.fetchall()
    outlets=cursor3.fetchall()
    context = {
                   'companies':companies,
                    "outlets":outlets,
                    "Account":Account,
                   }
    if request.method == 'POST':
        company_id = request.POST.get('my_input')
        outlet_id = request.POST.get('my_input1')
        AccountId = request.POST.get('my_input2')
        transaction_type = request.POST.get('my_input3')
        document_no = request.POST.get('document_no')
        date = request.POST.get('date')
        date1 = request.POST.get('date1')
        with connection.cursor() as cursor:
            cursor.execute("EXEC rpt_AccountBalance @company_id = %s ", [company_id,])
            results = cursor.fetchall()
            AccountBalance = [(row[1], row[3]) for row in results]    
            cursor.execute("EXEC rpt_AccountTransactions @account_id=%s,@from_date=%s,@to_date=%s,@document_no=%s,@transaction_type=%s,@party=%s,@outlet_id=%s,@expenditure_head=%s",[AccountId,date,date1,document_no,transaction_type,'',outlet_id,''])
            results = cursor.fetchall()
            AccountTransactions = [(row[2], row[6]) for row in results]    
            cursor.execute("EXEC rpt_SplitPayments @outlet_id = %s , @from_date = %s, @to_date = %s", [outlet_id,date,date1])
            results1 = cursor.fetchall()
            SplitPayments = [(row[0], row[1]) for row in results1]    
            context = {
                   
                    "AccountBalance": AccountBalance,
                    "SplitPayments": SplitPayments,
                    "AccountTransactions":AccountTransactions,
                   }
        return render(request, 'Account.html', context=context)
    else:
        return render(request, 'Account.html', context=context)
