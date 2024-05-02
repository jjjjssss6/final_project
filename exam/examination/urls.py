from django.urls import  path, include

import examination.views

urlpatterns = [
    path('get_all_examination', examination.views.GetAllExamination),
    path('get_examination', examination.views.GetExamination),
    path('get_paper_in_exam', examination.views.GetPaperInExam),
    path('get_exam_paper', examination.views.GetExamPaper),
    path('get_ques_in_paper', examination.views.GetQuesInPaper),
    path('get_question', examination.views.GetQuestion),
    path('upload_testset', examination.views.UploadTestset),
    path('download_testset', examination.views.DownloadTestset),

]