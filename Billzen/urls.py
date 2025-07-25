"""
URL configuration for Billzen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from Login import views
urlpatterns = [
    path('',views.login,name='login'),
    path('',include('Product_Stock.urls')),
    path('',include('Purchase.urls')),
    path('',include('sales.urls')),
    path('',include('Account.urls')),
    path('',include('setting.urls')),
    path('',include('Login.urls')),
    path('',include('feedback.urls')),
    path('',include('SalesKanban.urls')),
    path('',include('SalesInIndiaMap.urls')),
]
