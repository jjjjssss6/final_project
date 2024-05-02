from django.db import models
from examination.models import ExamPaper
from examination.models import PaperIncludingQuestions
from TeacherAccount.models import AccountSystem
from exam.settings import MEDIA_ROOT
import os
# Create your models here.


class StudentExamInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.TextField(null=False, blank=False)
    student_name = models.TextField()
    student_dept = models.TextField()
    paper_detail = models.ForeignKey(ExamPaper, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    paper_file = models.TextField()

    def __str__(self):
        return self.student_name

    class Meta:
        verbose_name = '考生名单'
        verbose_name_plural = '考生名单'

class TeacherCorrectionList(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_account = models.ForeignKey(AccountSystem, on_delete=models.CASCADE)
    student_account = models.ForeignKey(StudentExamInfo, on_delete=models.CASCADE)
    total_mark = models.IntegerField(default=0)

    def __str__(self):
        return str(self.teacher_account.username) + ' ' + str(self.student_account.student_name)

    class Meta:
        unique_together = ('teacher_account', 'student_account')
        verbose_name = '老师批改名单表'
        verbose_name_plural = '老师批改名单表'

def upload_to(instance, filename):
    file_root = 'paper_file'
    student_id = str(instance.student_detail.id)
    paper_id = str(instance.paper_ques_detail.paper_detial_id)
    ques_id = str(instance.paper_ques_detail.question_detial_id)
    file_path = f'{file_root}/{student_id}/{paper_id}/{ques_id}/{filename}'
    return file_path

class StudentExamFile(models.Model):
    id = models.AutoField(primary_key=True)
    student_detail = models.ForeignKey(StudentExamInfo, on_delete=models.CASCADE)
    paper_ques_detail = models.ForeignKey(PaperIncludingQuestions, on_delete=models.CASCADE)
    student_file = models.FileField(upload_to=upload_to)
    def __str__(self):
        return str(self.student_detail.student_name) + ' ' + str(self.paper_ques_detail.ques_name_in_paper)

    class Meta:
        verbose_name = '上传学生试卷'
        verbose_name_plural = '上传学生试卷'