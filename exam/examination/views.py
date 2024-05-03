from django.http import HttpResponse
import json
import TeacherAccount.logic
import examination.models
from examination.logic import ComplexEncoder
import os
import time
# Create your views here

def GetAllExamination(request):
    get_all_examination_req = json.loads(request.body.decode('utf_8'))
    get_all_examination_resp = {}
    ticket = get_all_examination_req.get('ticket')
    account_name = ''
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_all_examination_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_all_examination_resp, cls=ComplexEncoder, ensure_ascii=False))

    if (account_name == ''):
        get_all_examination_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_all_examination_resp, cls=ComplexEncoder, ensure_ascii=False))

    try:
        all_examination = list(examination.models.Examination.objects.all().values())
        real_all_examination = []
        for tmp_examination in all_examination:
            real_examination = tmp_examination
            now_time = time.time()
            if (now_time < real_examination['exam_begin_time']):
                real_examination['status'] = 0
            elif (now_time >= real_examination['exam_begin_time'] and now_time <= real_examination['exam_begin_time'] + real_examination['exam_last_time']):
                real_examination['status'] = 1
            elif (now_time <= real_examination['correction_end_time']):
                real_examination['status'] = 2
            else:
                real_examination['status'] = 3
            real_all_examination.append(real_examination)
            try:
                examination.models.Examination.objects.filter(examination_id=real_examination['examination_id']).update(status=real_examination['status'])
            except Exception:
                get_all_examination_resp['err_msg'] = '更新考试状态失败'
                return HttpResponse(json.dumps(get_all_examination_resp, cls=ComplexEncoder, ensure_ascii=False))
        get_all_examination_resp['examination_detail_list'] = real_all_examination
        get_all_examination_resp['err_msg'] = '获取所有考试信息成功'
        return HttpResponse(json.dumps(get_all_examination_resp, cls=ComplexEncoder, ensure_ascii=False))
    except Exception:
        get_all_examination_resp['err_msg'] = '获取所有考试信息失败'
        return HttpResponse(json.dumps(get_all_examination_resp, cls=ComplexEncoder, ensure_ascii=False))

def GetExamination(request):
    get_examination_req = json.loads(request.body.decode('utf_8'))
    get_examination_resp = {}
    ticket = get_examination_req.get('ticket')
    account_name = ''
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
         get_examination_resp['err_msg'] = '票据验证失败'
         return HttpResponse(json.dumps(get_examination_resp, cls=ComplexEncoder, ensure_ascii=False))

    if (account_name == ''):
        get_examination_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_examination_resp, cls=ComplexEncoder, ensure_ascii=False))

    examination_id = get_examination_req.get('examination_id')
    examination_detail = examination.models.Examination.objects.filter(examination_id = examination_id).values()
    if (examination_detail.count() == 0):
        get_examination_resp['err_msg'] = '找不到考试信息'
    elif(examination_detail.count() > 1):
        get_examination_resp['err_msg'] = '考试信息异常'
    else:
        get_examination_resp['err_msg'] = '考试信息查询成功'
        get_examination_resp['examination_detail'] = examination_detail[0]

    return HttpResponse(json.dumps(get_examination_resp, cls=ComplexEncoder, ensure_ascii=False))

def GetPaperInExam(request):
    get_paper_in_exam_req = json.loads(request.body.decode('utf_8'))
    get_paper_in_exam_resp = {}
    ticket = get_paper_in_exam_req.get('ticket')
    account_name = ''
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_paper_in_exam_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_paper_in_exam_resp, cls=ComplexEncoder, ensure_ascii=False))

    if (account_name == ''):
        get_paper_in_exam_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_paper_in_exam_resp, cls=ComplexEncoder, ensure_ascii=False))

    examination_id = get_paper_in_exam_req.get('examination_id')
    try:
        get_paper_in_exam_resp['examination_detail_list'] = list(examination.models.ExamPaper.objects.filter(examination_detial_id=examination_id).values())
        get_paper_in_exam_resp['err_msg'] = '获取所有考试下试卷信息成功'
        return HttpResponse(json.dumps(get_paper_in_exam_resp, cls=ComplexEncoder, ensure_ascii=False))
    except Exception:
        get_paper_in_exam_resp['err_msg'] = '获取所有考试下试卷信息失败'
        return HttpResponse(json.dumps(get_paper_in_exam_resp, cls=ComplexEncoder, ensure_ascii=False))


def GetExamPaper(request):
    get_exam_paper_req = json.loads(request.body.decode('utf_8'))
    get_exam_paper_resp = {}
    ticket = get_exam_paper_req.get('ticket')
    account_name = ''
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_exam_paper_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_exam_paper_resp, cls=ComplexEncoder, ensure_ascii=False))

    if (account_name == ''):
        get_exam_paper_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_exam_paper_resp, cls=ComplexEncoder, ensure_ascii=False))

    paper_id = get_exam_paper_req.get('paper_id')
    paper_detail = examination.models.ExamPaper.objects.filter(paper_id=paper_id).values()
    if (paper_detail.count() == 0):
        get_exam_paper_resp['err_msg'] = '找不到试卷信息'
    elif (paper_detail.count() > 1):
        get_exam_paper_resp['err_msg'] = '试卷信息异常'
    else:
        get_exam_paper_resp['err_msg'] = '试卷信息查询成功'
        get_exam_paper_resp['paper_detail'] = paper_detail[0]

    return HttpResponse(json.dumps(get_exam_paper_resp, cls=ComplexEncoder, ensure_ascii=False))

def GetQuesInPaper(request):
    get_ques_in_paper_req = json.loads(request.body.decode('utf_8'))
    get_ques_in_paper_resp = {}
    ticket = get_ques_in_paper_req.get('ticket')
    account_name = ''
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_ques_in_paper_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_ques_in_paper_resp, cls=ComplexEncoder, ensure_ascii=False))

    if (account_name == ''):
        get_ques_in_paper_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_ques_in_paper_resp, cls=ComplexEncoder, ensure_ascii=False))

    paper_id = get_ques_in_paper_req.get('paper_id')
    ques_including_ques_detail = examination.models.PaperIncludingQuestions.objects.filter(paper_detial_id=paper_id).values()

    ques_id_list = []
    for ques_detail in ques_including_ques_detail:
        ques_id_list.append(ques_detail['question_detial_id'])
    ques_id_list = list(set(ques_id_list))
    ques_list = examination.models.Question.objects.filter(ques_id__in=ques_id_list).values()
    real_ques_list = []
    index = 0
    for ques in ques_list:
        real_ques = ques
        real_ques['ques_score_in_paper'] = ques_including_ques_detail[index]['ques_score_in_paper']
        real_ques['ques_id_in_paper'] = ques_including_ques_detail[index]['ques_id_in_paper']
        real_ques['ques_name_in_paper'] = ques_including_ques_detail[index]['ques_name_in_paper']
        real_ques_list.append(real_ques)
        index = index + 1

    get_ques_in_paper_resp['examination_detail_list'] = list(ques_list)
    get_ques_in_paper_resp['err_msg'] = '获取试卷下所有题目成功'
    return HttpResponse(json.dumps(get_ques_in_paper_resp, cls=ComplexEncoder, ensure_ascii=False))



    return 0

def GetQuestion(request):
    get_question_req = json.loads(request.body.decode('utf_8'))
    get_question_resp = {}
    ticket = get_question_req.get('ticket')
    account_name = ''
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_question_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_question_resp, cls=ComplexEncoder, ensure_ascii=False))

    if (account_name == ''):
        get_question_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_question_resp, cls=ComplexEncoder, ensure_ascii=False))

    ques_id = get_question_req.get('ques_id')
    ques_detail = examination.models.Question.objects.filter(ques_id=ques_id).values()
    if (ques_detail.count() == 0):
        get_question_resp['err_msg'] = '找不到题目信息'
    elif (ques_detail.count() > 1):
        get_question_resp['err_msg'] = '题目信息异常'
    else:
        get_question_resp['err_msg'] = '题目信息查询成功'
        get_question_resp['paper_detail'] = ques_detail[0]

    return HttpResponse(json.dumps(get_question_resp, cls=ComplexEncoder, ensure_ascii=False))

def UploadTestset(request):
    upload_testset_resp = {}
    ticket = request.GET.get('ticket')
    account_name = ''
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        upload_testset_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))

    if (account_name == ''):
        upload_testset_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))

    ques_id = request.GET.get('ques_id', None)
    if (ques_id == None):
        upload_testset_resp['err_msg'] = '题目id为空'
        return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))

    try:
        if examination.models.Question.objects.filter(ques_id=int(ques_id)).values()[0]['ques_type'] != 4:
            upload_testset_resp['err_msg'] = '非编程题不可创建测试集'
            return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))
    except Exception:
        upload_testset_resp['err_msg'] = '题目信息不存在'
        return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))

    file_name = ''
    testset_type = request.GET.get('testset_type', None)
    if (testset_type == None):
        upload_testset_resp['err_msg'] = '测试集类型为空'
        return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (testset_type != '1' and testset_type != '2'):
        upload_testset_resp['err_msg'] = '测试集类型未知'
        return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))
    elif (testset_type == '1'):
        file_name = '输入.txt'
    elif (testset_type == '2'):
        file_name = '输出.txt'
    file_path = '/home/ubuntu/final_project/exam/media/testset/' + ques_id + '/' + testset_type + '/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    testset_file = request.FILES.get("testset_file", None)
    if (testset_file == None):
        upload_testset_resp['err_msg'] = '测试集为空'
        return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))
    file_path = file_path + file_name
    file_dest = open(file_path, 'wb')
    for chunk in testset_file.chunks():
        file_dest.write(chunk)
    file_dest.close()
    upload_testset_resp['err_msg'] = '上传测试集成功'
    return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))



def DownloadTestset(request):
    download_testset_resp = {}
    download_testset_req = json.loads(request.body.decode('utf_8'))
    ticket = download_testset_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        download_testset_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(download_testset_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        download_testset_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(download_testset_resp, cls=ComplexEncoder, ensure_ascii=False))

    test_set_id = download_testset_req.get('test_set_id', None)
    if (test_set_id == None):
        upload_testset_resp['err_msg'] = '测试集id为空'
        return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))

    test_set_detail = examination.models.TestSet.objects.filter(test_set_id=test_set_id).values()
    if test_set_detail.count() == 0:
        download_testset_resp['err_msg'] = '测试集不存在'
        return HttpResponse(json.dumps(download_testset_resp, cls=ComplexEncoder, ensure_ascii=False))


    argv = 'test_set_'
    test_set_type = download_testset_req.get('test_set_type', None)
    if (test_set_type == None):
        download_testset_resp['err_msg'] = '测试集类型为空'
        return HttpResponse(json.dumps(download_testset_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (test_set_type != '1' and test_set_type != '2'):
        upload_testset_resp['err_msg'] = '测试集类型未知'
        return HttpResponse(json.dumps(upload_testset_resp, cls=ComplexEncoder, ensure_ascii=False))
    elif (test_set_type == '1'):
        argv = argv + 'input'
    elif (test_set_type == '2'):
        argv = argv + 'output'
    test_set_no = download_testset_req.get('test_set_no', None)
    if (test_set_no == None):
        download_testset_resp['err_msg'] = '测试集组数为空'
        return HttpResponse(json.dumps(download_testset_resp, cls=ComplexEncoder, ensure_ascii=False))
    argv = argv + str(test_set_no)

    file_path = '/home/ubuntu/final_project/exam/media/' + test_set_detail[0][argv]
    with open(file_path, 'rb') as f:
        try:
            response = HttpResponse(f)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except Exception:
            download_student_exam_resp['err_msg'] = '文件下载失败'
            return HttpResponse(json.dumps(download_student_exam_resp, cls=ComplexEncoder, ensure_ascii=False))

def GetTestSet(request):
    get_test_set_resp = {}
    get_test_set_req = json.loads(request.body.decode('utf_8'))
    ticket = get_test_set_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_test_set_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_test_set_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        get_test_set_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_test_set_resp, cls=ComplexEncoder, ensure_ascii=False))

    test_set_id = get_test_set_req.get('test_set_id', None)
    if (test_set_id == None):
        get_test_set_resp['err_msg'] = '测试集id为空'
        return HttpResponse(json.dumps(get_test_set_resp, cls=ComplexEncoder, ensure_ascii=False))
    test_set_detail = examination.models.TestSet.objects.filter(test_set_id=test_set_id).values()
    if test_set_detail.count() == 0:
        download_testset_resp['err_msg'] = '测试集不存在'
        return HttpResponse(json.dumps(download_testset_resp, cls=ComplexEncoder, ensure_ascii=False))
    real_test_set_detail = test_set_detail[0]
    for i in range(1, 6, 1):
        argv_in = 'test_set_input' + str(i)
        argv_out = 'test_set_output' + str(i)
        if (real_test_set_detail[argv_in] == '' or real_test_set_detail[argv_out] == ''):
            continue
        file_path_in = '/home/ubuntu/final_project/exam/media/' + real_test_set_detail[argv_in]
        file_path_out = '/home/ubuntu/final_project/exam/media/' + real_test_set_detail[argv_out]
        with open(file_path_in, 'r') as f:
            res = str(f.readlines())
            print(res)
            res = res.strip("\n")
            print(res)
            real_test_set_detail[argv_in + '_detail'] = res
        with open(file_path_out, 'r') as f:
            res = str(f.readlines())
            print(res)
            res = res.strip("\n")
            print(res)
            real_test_set_detail[argv_out + '_detail'] = res

    get_test_set_resp['err_msg'] = '获取测试集成功'
    get_test_set_resp['test_set_detail'] = real_test_set_detail
    return HttpResponse(json.dumps(get_test_set_resp, cls=ComplexEncoder, ensure_ascii=False))
