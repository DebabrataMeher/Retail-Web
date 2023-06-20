from django.shortcuts import render
from django.db import connection
from datetime import datetime
def setting(request):
    context = {

                   }
    if request.method == 'POST':
        account_sid = request.POST['whatsappApi']
        auth_token = request.POST['Apikey']
        Enable_WhatsApp = request.POST['yes_no']
        twilio_phone_number = '+14155238886'
        to_phone_number = '+918310095539'
        scheduler = request.POST['scheduler']
        reports = request.POST['my_input3']
        time = request.POST['rtime']
        current_time = datetime.now().strftime('%H:%M')
        # if(current_time==time):
        #     print("Demo Contents")
        if(Enable_WhatsApp=='ON'):
            with connection.cursor() as cursor:
                results=''
                if(reports=='Available_Stock' ):
                    cursor.execute('EXEC rpt_AvailableStock 72,164')
                    results1 = cursor.fetchall()
                    results= [(row[1], row[4],row[3]) for row in results1]
                    displayed_columns = ['Product Name    ', '    Quantity' ]
                elif(reports=='Low_Stock'):
                    cursor.execute('EXEC rpt_LowStock 72,164')
                    results1 = cursor.fetchall()
                    results= [(row[1], row[4] ,row[3]) for row in results1]
                    displayed_columns = ['Product Name    ', '    Quantity' ]
                elif(reports=='PurchaseProducts'):
                    cursor.execute("EXEC [rpt_PurchaseProducts] 72,'','01-Mar-23','01-Jun-23','','','','purchase'")
                    results1 = cursor.fetchall()
                    results= [(row[1], row[3] ) for row in results1]
                    displayed_columns = ['Product Name    ', '    Quantity' ]
                elif(reports=="Return's_PurchaseProducts"):
                    cursor.execute("EXEC [rpt_PurchaseProducts] 72,'','01-Mar-23','01-Jun-23','','','','return'")
                    results1 = cursor.fetchall()
                    results= [(row[1], row[3] ) for row in results1]
                    displayed_columns = ['Product Name    ', '    Quantity' ]
                elif(reports=='SalesProducts'):
                    cursor.execute("EXEC [rpt_SalesProducts] 72,'','01-Mar-23','01-Jun-23','','','','sales'")
                    results1 = cursor.fetchall()
                    results= [(row[1], row[3] ) for row in results1]
                    displayed_columns = ['Product Name    ', '    Quantity' ]
                elif(reports=="Return's_SalesProducts"):
                    cursor.execute("EXEC [rpt_SalesProducts] 72,'','01-Mar-23','01-Jun-23','','','','return'")
                    results1 = cursor.fetchall()
                    results= [(row[1], row[3] ) for row in results1]
                    displayed_columns = ['Product Name    ', '    Quantity' ]
                elif(reports=="Return_Reason_Report"):
                    cursor.execute('SELECT count(*) "Number of reasons", return_reason FROM tbl_ReturnReason, tbl_ReturnFeedbackSubmission WHERE tbl_ReturnReason.return_id=tbl_ReturnFeedbackSubmission.return_id GROUP BY return_reason;')
                    results1 = cursor.fetchall()
                    results= [(row[1], row[0] ) for row in results1]
                    displayed_columns = ['Return Reason    ', '    Number of Reasons']
                message = 'Hello '+scheduler+"\n\n"+"Your "+reports+" is -->"+"\n\n"
                message += "\t".join(displayed_columns) + "\n"
                for record in results:
                    displayed_values = [record[0], record[1] ]
                    message += "\t".join(str(field) for field in displayed_values) + "\n"

                from twilio.rest import Client
                client = Client(account_sid, auth_token)
                max_length = 1600
                message_parts = [message[i:i + max_length] for i in range(0, len(message), max_length)]
                for part in message_parts:
                    message = client.messages.create(
                        body=part,
                        from_=f'whatsapp:{twilio_phone_number}',
                        to=f'whatsapp:{to_phone_number}'
                    )
                context['success_message'] = "Successfully message sended on WhatsApp."
    return render(request, 'setting.html', context=context)

def index(request):
    return render(request, 'index.html')






















































from twilio.rest import Client

def send_sms_view(request):
    if request.method == 'POST':
        account_sid = request.POST['account_sid']
        auth_token = request.POST['auth_token']
        twilio_phone_number = request.POST['twilio_phone_number']
        to_phone_number = request.POST['to_phone_number']
        message = request.POST['message']

        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=to_phone_number
        )

        return render(request, 'success.html')

    return render(request, 'send_sms.html')