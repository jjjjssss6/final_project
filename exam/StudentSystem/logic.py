from django import forms
import StudentSystem.models
from TeacherAccount.logic import GetUserNameById

def GetStudentInfoById(id):
    info = {}
    try:
        student_info = StudentSystem.models.StudentExamInfo.objects.filter(id=id).values()[0]
        return student_info
    except Exception:
        return '根据id获取学生信息失败'

def GetStudentInfoAndTeacherNameByCorrectionId(id):
    info = {}
    try:
        correction_info = StudentSystem.models.TeacherCorrectionList.objects.filter(id=id).values()[0]
        info['teacher_name'] = GetUserNameById(correction_info['teacher_account_id'])
        info['student_info'] = GetStudentInfoById(correction_info['student_account_id'])
        return info
    except Exception:
        return '根据id获取改卷名单信息失败'
