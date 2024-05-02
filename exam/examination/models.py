from django.db import models
import TeacherAccount.models
from django import forms
# Create your models here.

# 考试
class Examination(models.Model):
    examination_id = models.AutoField(primary_key=True)
    examination_name = models.TextField(null=False,blank=False)
    status = models.PositiveIntegerField(default=0)  # 0 未开始 1 进行中 2 批卷中 3 已结束
    examination_desc = models.TextField(null=True, blank=True)
    exam_begin_time = models.PositiveIntegerField()  # unix 时间cuo
    exam_last_time = models.PositiveIntegerField()  # 单位秒
    correction_end_time = models.PositiveIntegerField()
    examination_type = models.PositiveIntegerField(default=2)  # 0 期中 1 期末 2 模拟
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    def __str__(self):
        return self.examination_name

    class Meta:
        verbose_name = '考试信息'
        verbose_name_plural = '考试信息'

#试卷
class ExamPaper(models.Model):  # 试卷只属于一次考试 不复用
    paper_id = models.AutoField(primary_key=True)
    examination_detial = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name="papers", null=True)
    paper_name = models.TextField(null=False,blank=False)
    paper_type = models.PositiveIntegerField(null=True, blank=True)
    total_score = models.PositiveIntegerField(default=100)

    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    def __str__(self):
        return self.paper_name

    class Meta:
        verbose_name = '试卷信息'
        verbose_name_plural = '试卷信息'

def in_file_upload_to(instance, filename):
    file_root = 'test_set'
    file_id = instance.test_set_id
    file_type = '1'
    file_path = f'{file_root}/{file_id}/{file_type}/{filename}'
    return file_path

def out_file_upload_to(instance, filename):
    file_root = 'test_set'
    file_id = instance.test_set_id
    file_type = '2'
    file_path = f'{file_root}/{file_id}/{file_type}/{filename}'
    return file_path

class TestSet(models.Model):
    test_set_id = models.AutoField(primary_key=True)
    test_set_name = models.TextField(null=False,blank=False,unique=True)
    test_set_desc = models.TextField(null=True,blank=True)

    test_set_input1 = models.FileField(upload_to=in_file_upload_to, null=True, blank=True)
    test_set_output1 = models.FileField(upload_to=out_file_upload_to, null=True, blank=True)

    test_set_input2 = models.FileField(upload_to=in_file_upload_to, null=True, blank=True)
    test_set_output2 = models.FileField(upload_to=out_file_upload_to, null=True, blank=True)

    test_set_input3 = models.FileField(upload_to=in_file_upload_to, null=True, blank=True)
    test_set_output3 = models.FileField(upload_to=out_file_upload_to, null=True, blank=True)

    test_set_input4 = models.FileField(upload_to=in_file_upload_to, null=True, blank=True)
    test_set_output4 = models.FileField(upload_to=out_file_upload_to, null=True, blank=True)

    test_set_input5 = models.FileField(upload_to=in_file_upload_to, null=True, blank=True)
    test_set_output5 = models.FileField(upload_to=out_file_upload_to, null=True, blank=True)

    def __str__(self):
        return self.test_set_name

    class Meta:
        verbose_name = '测试集表'
        verbose_name_plural = '测试集表'

#题目
class Question(models.Model):
    ques_id = models.AutoField(primary_key=True)
    ques_type = models.PositiveSmallIntegerField()  # 1 选择题 2 阅读题 3 填空题 4 编程题
    ques_name = models.TextField(null=False,blank=False)
    ques_desc = models.TextField()
    ques_ans = models.TextField()
    ques_score = models.PositiveIntegerField(null=False)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    test_set = models.ForeignKey(TestSet, null=True, blank=True, on_delete=models.SET_NULL)
    create_account = models.ForeignKey(TeacherAccount.models.AccountSystem, null=True,blank=True,on_delete=models.SET_NULL)
    def __str__(self):
        return self.ques_desc

    class Meta:
        verbose_name = '题目信息'
        verbose_name_plural = '题目信息'

#试卷题目表
class PaperIncludingQuestions(models.Model):
    id = models.AutoField(primary_key=True)
    paper_detial = models.ForeignKey(ExamPaper, on_delete=models.CASCADE)
    question_detial = models.ForeignKey(Question, on_delete=models.CASCADE)
    ques_score_in_paper = models.PositiveIntegerField(null=False,blank=False)
    ques_id_in_paper = models.PositiveIntegerField(null=False,blank=False)
    ques_name_in_paper = models.TextField(null=False,blank=False)

    def __str__(self):
        return str(self.paper_detial.paper_name) + ' ' + str(self.question_detial.ques_name)

    class Meta:
        verbose_name = '试卷题目表'
        verbose_name_plural = '试卷题目表'