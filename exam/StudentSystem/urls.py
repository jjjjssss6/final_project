from django.urls import  path, include

import StudentSystem.views

urlpatterns = [
    path('upload_student_exam', StudentSystem.views.UploadStudentExam),
    path('download_student_exam', StudentSystem.views.DownloadStudentExam),
    path('get_student_list', StudentSystem.views.GetCorrectionList),
]