from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login_page'),  # Rename your custom login view
    path('main/', views.main, name='main'),
    path('add_student/', views.add_student, name='add_student'),
    path('delete_student/<int:reg_no>/', views.delete_student, name='delete_student'),
    path('delete_mark/<str:subject_id>/<int:reg_no>/', views.delete_mark, name='delete_mark'),
    path('report/<int:reg_no>/', views.report, name='report'),
    path('add_marks/<int:reg_no>/', views.add_marks, name='add_marks'),
    path('upload_student/', views.upload_student, name='upload_student'),
]
