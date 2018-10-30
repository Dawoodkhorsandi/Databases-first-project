from django.urls import path
from . import views


app_name = 'app'


urlpatterns = [
     path('',
          views.index,
          name='index'),  
     # path('login/',
     #      views.login,
     #      name='my_login')  ,

     # Step1 demonstrates user request form and modreation of 
     # their request  
     path('step1/',
          views.sending_request,
          name='step1'),
     path('requests/',
          views.request_table,
          name='request_table'),
     path("requests/edit/<str:national_code>/",
          views.edit_request,
          name="edit_request"),
     path("requests/confirm/step1/<str:national_code>/",
          views.confirm_request_step1,
          name="confirm_request_step1"),
     path("requests/delete/<str:national_code>/",
          views.delete_request,
          name="delete_request"),
     path('confirmed_table/',
          views.confirmed_table,
          name='confirmed_table'),
     path('bill/<int:subscription_number>/',
          views.bill,
          name='bill'),
     path('bills/',
          views.all_bills,
          name='all_bills'),
     path('pay/<str:subscription_number>/<str:ID>/',
          views.pay,
          name='pay'),

]
