from django.shortcuts import render
from django.shortcuts import render, redirect
from Login.sms_utils import send_sms
# Create your views here.
def login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        if phone_number == '+917749959081' and password == '1234':
            message = " Hello Surya Welcome to BillZen Application "
            send_sms(phone_number, message)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid phone number or password'})
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')

def logout(request):
    return render(request, 'login.html')