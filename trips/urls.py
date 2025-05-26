from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:trip_id>/reserve/', views.make_reservation, name='make_reservation'),
    path('payment/<int:reservation_id>/process/', views.payment_process, name='payment_process'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/trip/create/', views.admin_trip_create, name='admin_trip_create'),
    path('admin/trip/<int:trip_id>/delete/', views.admin_trip_delete, name='admin_trip_delete'),
    path('admin/trip/<int:trip_id>/discount/', views.admin_trip_discount, name='admin_trip_discount'),
    path('my-reservations/', views.user_reservations, name='user_reservations'),
]