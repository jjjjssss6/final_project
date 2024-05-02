from django.db import models
from StudentSystem.models import TeacherCorrectionList
from TeacherAccount.models import AccountSystem
from examination.models import PaperIncludingQuestions

# Create your models here.

class CorrectTestDetail(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_correct_details = models.ForeignKey(TeacherCorrectionList,null=True,blank=True, on_delete=models.CASCADE)
    ques_detail = models.ForeignKey(PaperIncludingQuestions, on_delete=models.CASCADE)
    student_score = models.PositiveIntegerField(null=False,blank=False)
    correct_detail = models.TextField(null=True)  # 得分点详情 一些批注
    recheck_teacher_detail = models.ForeignKey(AccountSystem, null=True,blank=True,on_delete=models.SET_NULL)
    recheck_score = models.PositiveIntegerField(null=True,blank=True)

    class Meta:
        verbose_name = '判题记录'
        verbose_name_plural = '判题记录'

    # def __str__(self):
    #     return str(self.student_id) + '_' + str(self.ques_id)
