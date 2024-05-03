from django.urls import  path, include

import CorrectTest.views

urlpatterns = [
    path('correct_ques', CorrectTest.views.CorrectQues),
    path('recheck_ques', CorrectTest.views.RecheckQues),
    path('get_correct_ques', CorrectTest.views.GetCorrectQues),
    path('submit_judge_mission', CorrectTest.views.SubmitJudgeMission),
    path('get_judge_result', CorrectTest.views.GetJudgeResult),
    path('get_grade_table', CorrectTest.views.GetGradeTable),
]
