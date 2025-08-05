"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from core.views import register_customer
from core import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("register", register_customer, name="register_customer"),
    
    path("check-eligibility", views.check_eligibility),

    path("create-loan/", views.create_loan, name="create_loan"),

    path("view-loan", views.view_loan),
    path("view-loans/<int:customer_id>", views.view_loans_by_customer),
    path("view-all-loans", views.view_all_loans),
]   
