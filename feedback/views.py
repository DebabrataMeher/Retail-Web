from django.shortcuts import render
from .models import tbl_ReturnReason,tbl_ReturnFeedbackSubmission
from django.shortcuts import render
from .models import tbl_ReturnReason,tbl_ReturnFeedbackSubmission
from SalesKanban.models import tbl_SalesProjections

def your_view(request):
    data = tbl_SalesProjections.objects.all() .delete() 
    return render(request, 'success.html', {'data': data})


from django.db import connection
from django.shortcuts import render
import json
def feedback_view(request):
    cursor = connection.cursor()
    cursor1 = connection.cursor()
    cursor2=connection.cursor()
    cursor4=connection.cursor()
    cursor.execute("EXEC rpt_GetReturnReasonCountsByMarketPlace @marketPlace = %s, @fromDate = %s, @toDate = %s ", ['All','',''])
    feedbackView1 = cursor.fetchall()
    cursor1.execute("EXEC [rpt_GetReturnFeedbackViewReport] @marketPlace = %s, @fromDate = %s, @toDate = %s ", ['All','',''])
    feedbackTbl=cursor1.fetchall()
    cursor2.execute("EXEC [rpt_GetReturnCountsForEachMarketPlace]  @fromDate = %s, @toDate = %s ", ['',''])
    Countmktplc1=cursor2.fetchall()
    cursor4.execute("EXEC rpt_GetReturnCountsOfProductByMarketPlace @marketPlace = %s, @fromDate = %s, @toDate = %s ", ['All','',''])
    ReturnByProducts=cursor4.fetchall()
    context = {
            'feedbackView': json.dumps(feedbackView1),
            'feedbackView2':feedbackView1,
            'feedbackTbl':feedbackTbl,
            'Countmktplc':Countmktplc1,
            'ReturnByProducts1':ReturnByProducts,
            'ReturnByProducts':json.dumps(ReturnByProducts),
            'Countmktplc1':json.dumps(Countmktplc1),
        }
    if request.method == 'POST':
        from_date = request.POST.get('date')
        to_date = request.POST.get('date1')
        market_place = request.POST.get('market_place')
        cursor.execute("EXEC [rpt_GetReturnFeedbackViewReport] @marketPlace = %s, @fromDate = %s, @toDate = %s ", [market_place,from_date,to_date])
        feedbackTbl = cursor.fetchall()
        cursor.execute("EXEC rpt_GetReturnReasonCountsByMarketPlace @marketPlace = %s, @fromDate = %s, @toDate = %s ", [market_place,from_date,to_date])
        feedbackView1=cursor.fetchall()
        cursor3=connection.cursor()
        cursor3.execute("EXEC rpt_GetReturnCountsOfProductByMarketPlace @marketPlace = %s, @fromDate = %s, @toDate = %s ", [market_place,from_date,to_date])
        ReturnByProducts = cursor3.fetchall()
        context = {
                   'ReturnByProducts':ReturnByProducts,
                   'ReturnByProducts':json.dumps(ReturnByProducts),
                   'ReturnByProducts1':ReturnByProducts,
                   'feedbackView': json.dumps(feedbackView1),
                    'feedbackView2':feedbackView1,
                    'feedbackTbl':feedbackTbl,
                    'Countmktplc':Countmktplc1,
                    'Countmktplc1':json.dumps(Countmktplc1),
                    'from_date':from_date,
                    'to_date':to_date,
                    'market_place':market_place,
                    
                   }    
        return render(request, 'feedback_report view.html', context=context)
    return render(request, 'feedback_report view.html', context=context)




from django.shortcuts import render
def user_input(request):
    return_re = tbl_ReturnReason.objects.all()
    return_reas=[(row.return_id,row.return_reason) for row in return_re]
    context = {
                   'return_reas':return_reas,
                   }
    if request.method == 'POST':
        if 'button1' in request.POST:
            date_of_return = request.POST.get('date_of_return')
            market_place = request.POST.get('market_place')
            return_item_id = request.POST.get('return_item_id')
            order_reference = request.POST.get('order_reference')
            product_name = request.POST.get('product_name')
            quantity = request.POST.get('quantity')
            return_id = request.POST.get('return_id')
            customer_details = request.POST.get('customer_details')
            reason_description = request.POST.get('reason_description')
            is_deleted = request.POST.get('is_deleted')
            is_deleted = True if is_deleted == 'on' else False
            your_instance = tbl_ReturnFeedbackSubmission(date_of_return=date_of_return, market_place=market_place, return_item_id=return_item_id ,order_reference=order_reference ,product_name=product_name, quantity=quantity, return_id=return_id, customer_details=customer_details, reason_description=reason_description, is_deleted=is_deleted)
            your_instance.save()
            context['success_message'] = "Feedback Submitted of "+return_item_id
        if 'button2' in request.POST:
            return_reason = request.POST.get('return_reason')
            your_instance1 = tbl_ReturnReason(return_reason=return_reason)
            your_instance1.save()
            context['success_message'] = "Return reason added successfully."
    return render(request, 'feedbackSubmission.html', context=context)


