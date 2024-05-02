from django.urls import  path, include

import TeacherAccount.views

urlpatterns = [
    path('login', TeacherAccount.views.Login),
]