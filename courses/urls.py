from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_courses, name='list_courses'),
    path('add/', views.add_course, name='add_course'),
    path('update/<int:course_id>/', views.update_course, name='update_course'),
    path('delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('search/', views.search_courses, name='search_courses'),
    path('associate/', views.associate_student, name='associate_student'),
    path('student-courses/<int:student_id>/', views.get_courses_by_student, name='get_courses_by_student'),
    path('courses/disassociate-all/<str:student_id>/', views.disassociate_all_student_courses, name='disassociate_all_student_courses'),
]
