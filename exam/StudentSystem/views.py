from django.http import HttpResponse
import json
import os
import TeacherAccount.logic
from examination.logic import ComplexEncoder
from examination.models import PaperIncludingQuestions
from TeacherAccount.models import AccountSystem
from StudentSystem.models import StudentExamInfo
from StudentSystem.models import TeacherCorrectionList
from StudentSystem.models import StudentExamFile
import StudentSystem.models


# Create your views here.

def UploadStudentExam(request):
    upload_student_exam_resp = {}
    ticket = request.GET.get('ticket')
    account_name = ''
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        upload_student_exam_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(upload_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))

    if (account_name == ''):
        upload_student_exam_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(upload_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))

    student_id = request.GET.get('student_id')
    student_name = request.GET.get('student_name')
    student_dept = request.GET.get('student_dept')
    examination_id = request.GET.get('examination_id')
    paper_id = request.GET.get('paper_id')
    if student_id == '' or examination_id == '' or paper_id == '':
        upload_student_exam_resp['err_msg'] = '关键参数为空'
        return HttpResponse(json.dumps(upload_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))

    paper_file = request.FILES.get("paper_file", None)
    if not paper_file:
        upload_student_exam_resp['err_msg'] = '试卷文件为空'
        return HttpResponse(json.dumps(upload_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))
    StudentSystem.models.StudentExamInfo.objects.create(
        student_id = student_id,
        student_name = student_name,
        student_dept=student_dept,
        examination_id=examination_id,
        paper_id=paper_id,
        paper_file=paper_file.name,
    )
    file_path = '/home/ubuntu/final_project/exam/media/paper_file/' + examination_id + '/' + paper_id + '/' + student_id + '/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = file_path + paper_file.name
    file_dest = open(file_path, 'wb')
    for chunk in paper_file.chunks():
        file_dest.write(chunk)
    file_dest.close()
    upload_student_exam_resp['err_msg'] = '上传试卷成功'
    return HttpResponse(json.dumps(upload_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))

def DownloadStudentExam(request):
    download_student_exam_resp = {}
    download_student_exam_req = json.loads(request.body.decode('utf_8'))
    ticket = download_student_exam_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        download_student_exam_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(download_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        download_student_exam_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(download_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))

    student_account_id = download_student_exam_req.get('student_account_id')
    paper_id = download_student_exam_req.get('paper_id')
    ques_id = download_student_exam_req.get('ques_id')
    if student_account_id == '' or paper_id == '' or ques_id == '':
        download_student_exam_resp['err_msg'] = '关键参数为空'
        return HttpResponse(json.dumps(download_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))
    paper_ques_id = PaperIncludingQuestions.objects.filter(paper_detial_id = paper_id,question_detial_id=ques_id).values()[0]['id']
    file_name = StudentExamFile.objects.filter(student_detail_id=student_account_id, paper_ques_detail_id=paper_ques_id).values()[0]['student_file']
    file_path = '/home/ubuntu/final_project/exam/media/' + file_name
    with open(file_path, 'rb') as f:
        try:
            response = HttpResponse(f)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except Exception:
            download_student_exam_resp['err_msg'] = '文件下载失败'
            return HttpResponse(json.dumps(download_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))

def GetCorrectionList(request):
    get_correction_list_req = json.loads(request.body.decode('utf_8'))
    get_correction_list_resp = {}
    ticket = get_correction_list_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_correction_list_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_correction_list_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        submit_judge_mission_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_correction_list_resp, cls=ComplexEncoder, ensure_ascii=False))

    paper_id = get_correction_list_req.get('paper_id', None)
    if (paper_id == None):
        get_correction_list_resp['err_msg'] = '参数不能为空'
        return HttpResponse(json.dumps(get_correction_list_resp, cls=ComplexEncoder, ensure_ascii=False))
    else:
        student_list = StudentExamInfo.objects.filter(paper_detail_id=paper_id).values()
        student_id_list = []
        map_student_info = {}
        for student in student_list:
            student_id_list.append(student['id'])
            map_student_info[student['id']] = student
        account_id = AccountSystem.objects.filter(username=account_name).values()[0]['id']
        correct_list = TeacherCorrectionList.objects.filter(teacher_account_id=account_id, student_account_id__in=student_id_list).values()
        for correct_info in correct_list:
            map_student_info[correct_info['student_account_id']]['total_score'] = correct_info['total_mark']

        list_student_info = []
        for student in map_student_info.values():
            list_student_info.append(student)
        try:
            get_correction_list_resp['student_list'] = list_student_info
            get_correction_list_resp['err_msg'] = '获取老师批改名单成功'
            return HttpResponse(json.dumps(get_correction_list_resp, cls=ComplexEncoder, ensure_ascii=False))
        except Exception:
            get_correction_list_resp['err_msg'] = '获取老师批改名单失败'
            return HttpResponse(json.dumps(get_correction_list_resp, cls=ComplexEncoder, ensure_ascii=False))
