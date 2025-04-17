from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
  
    path('', views.landing_page, name='landing_page'),
    path('logout', views.landing_page, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('reset-password/', views.reset_password, name='reset_password'),
   
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
   
    path('role-selection/', views.role_selection_view, name='role_selection'),
    path('students/<str:role>/', views.student_list_view, name='student_list'),
    path('students/midsem/<int:student_id>/', views.update_midsem_marks, name='update_midsem_marks'),
    path('students/endsem/<int:student_id>/', views.update_endsem_marks, name='update_endsem_marks'),
    path('students/', views.student_list_view, name='student_list'),
   
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-list/<str:role>/', views.student_list_view, name='student_list'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Add dashboard later
    path('send-marks-email/<str:role>/', views.send_marks_email, name='send_marks_email'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/login/', views.custom_login, name='student_login'),
    path('pdf_success/', views.pdf_success, name='pdf_success'),  # New success page
    path('professor-login/', views.professor_login, name='professor_login'),


]
