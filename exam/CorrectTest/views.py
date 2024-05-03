from django.http import HttpResponse
import TeacherAccount.logic
import json
from TeacherAccount.models import AccountSystem
from examination.logic import ComplexEncoder
from CorrectTest.logic import EasyCurl
from StudentSystem.models import TeacherCorrectionList
from StudentSystem.models import StudentExamInfo
from examination.logic import GetPaperQuesById
from TeacherAccount.logic import GetUserNameById
from StudentSystem.logic import GetStudentInfoAndTeacherNameByCorrectionId

import examination.models
import CorrectTest.models

# Create your views here.

def CorrectQues(request):
    correct_ques_resp = {}
    correct_ques_req = json.loads(request.body.decode('utf_8'))
    ticket = correct_ques_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        correct_ques_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        correct_ques_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    teacher_account_id = AccountSystem.objects.filter(username=account_name).values()[0]['id']

    student_account_id = correct_ques_req.get('student_account_id', None)
    if student_account_id == None:
        correct_ques_resp['err_msg'] = '考生id不能为空'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    teacher_correction_detail = TeacherCorrectionList.objects.filter(teacher_account_id=teacher_account_id,student_account_id=student_account_id).values()
    if (teacher_correction_detail.count() == 0):
        correct_ques_resp['err_msg'] = '找不到老师批改信息'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    elif (teacher_correction_detail.count() > 1):
        correct_ques_resp['err_msg'] = '老师批改信息异常'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))

    ques_id = correct_ques_req.get('ques_id', None)
    if ques_id == None:
        correct_ques_resp['err_msg'] = '题目id不能为空'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    ques_detail = examination.models.Question.objects.filter(ques_id=ques_id).values()
    if (ques_detail.count() == 0):
        correct_ques_resp['err_msg'] = '找不到题目信息'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    elif(ques_detail.count() > 1):
        correct_ques_resp['err_msg'] = '题目信息异常'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    paper_id = correct_ques_req.get('paper_id', None)
    if paper_id == None:
        correct_ques_resp['err_msg'] = '试卷id不能为空'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    paper_detail = examination.models.ExamPaper.objects.filter(paper_id=paper_id).values()
    if (paper_detail.count() == 0):
        correct_ques_resp['err_msg'] = '找不到试卷信息'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    elif (paper_detail.count() > 1):
        correct_ques_resp['err_msg'] = '试卷信息异常'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    paper_ques_detail = examination.models.PaperIncludingQuestions.objects.filter(paper_detial_id=paper_id,question_detial_id=ques_id).values()
    if (paper_ques_detail.count() == 0):
        correct_ques_resp['err_msg'] = '找不到试卷题目信息'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    elif (paper_ques_detail.count() > 1):
        correct_ques_resp['err_msg'] = '试卷题目信息异常'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))


    student_score = correct_ques_req.get('student_score', None)
    if student_score == None:
        correct_ques_resp['err_msg'] = '得分不能为空'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))

    if paper_ques_detail[0]['ques_score_in_paper'] < student_score:
        correct_ques_resp['err_msg'] = '得分不能大于题目总分'
        return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))


    correct_test_count = CorrectTest.models.CorrectTestDetail.objects.filter(teacher_correct_details_id=teacher_correction_detail[0]['id'],ques_detail_id=paper_ques_detail[0]['id']).values().count()
    origin_score = CorrectTest.models.CorrectTestDetail.objects.filter(teacher_correct_details_id=teacher_correction_detail[0]['id'],ques_detail_id=paper_ques_detail[0]['id']).values()[0]['student_score']
    diff_score = 0
    if correct_test_count > 0:  # 判题记录已存在
        try:
            CorrectTest.models.CorrectTestDetail.objects.filter(
                teacher_correct_details_id=teacher_correction_detail[0]['id'], ques_detail_id=paper_ques_detail[0]['id']).update(student_score=student_score,correct_detail=correct_ques_req.get('correct_detail', None))
        except Exception:
            correct_ques_resp['err_msg'] = '判题信息录入失败'
            return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
        diff_score = student_score - origin_score
    else:
        try:
            CorrectTest.models.CorrectTestDetail.objects.create(
                teacher_correct_details_id=teacher_correction_detail[0]['id'],
                ques_detail_id=paper_ques_detail[0]['id'],
                student_score=student_score,
                correct_detail=correct_ques_req.get('correct_detail', None)
            )
            diff_score = student_score
        except Exception:  # 判题信息已存在？修改判题数据
            correct_ques_resp['err_msg'] = '判题信息录入失败'
            return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    TeacherCorrectionList.objects.filter(teacher_account_id=teacher_account_id, student_account_id=student_account_id).update(total_mark=teacher_correction_detail[0]['total_mark'] + diff_score)


    correct_ques_resp['err_msg'] = '判题成功'
    return HttpResponse(json.dumps(correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))

def RecheckQues(request):
    recheck_ques_resp = {}
    recheck_ques_req = json.loads(request.body.decode('utf_8'))
    ticket = recheck_ques_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        recheck_ques_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(recheck_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        recheck_ques_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(recheck_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    teacher_account_id = AccountSystem.objects.filter(username=account_name).values()[0]['id']
    correct_id = recheck_ques_req.get('correct_id')
    correct_detail = CorrectTest.models.CorrectTestDetail.objects.filter(id=correct_id).values()[0]
    paper_ques_detail = examination.models.PaperIncludingQuestions.objects.filter(id=correct_detail['ques_detail_id']).values()
    recheck_score = recheck_ques_req.get('recheck_score', None)
    if recheck_score == None:
        recheck_ques_resp['err_msg'] = '复核得分不能为空'
        return HttpResponse(json.dumps(recheck_ques_resp, cls=ComplexEncoder, ensure_ascii=False))

    if paper_ques_detail[0]['ques_score_in_paper'] < recheck_score:
        recheck_ques_resp['err_msg'] = '复核得分不能大于题目总分'
        return HttpResponse(json.dumps(recheck_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    student_account_id = TeacherCorrectionList.objects.filter(id=correct_detail['teacher_correct_details_id']).values()[0]['student_account_id']
    teacher_correction_count = TeacherCorrectionList.objects.filter(teacher_account_id=teacher_account_id,
                                                                     student_account_id=student_account_id).values().count()
    if teacher_correction_count == 0:
        recheck_ques_resp['err_msg'] = '该老师没有复核权限'
        return HttpResponse(json.dumps(recheck_ques_resp, cls=ComplexEncoder, ensure_ascii=False))



    try:
        CorrectTest.models.CorrectTestDetail.objects.filter(id=correct_id).update(recheck_score=recheck_score,
                                                          recheck_teacher_detail_id=teacher_account_id)
    except Exception:
        recheck_ques_resp['err_msg'] = '复核信息录入失败'
        return HttpResponse(json.dumps(recheck_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    recheck_ques_resp['err_msg'] = '复核信息录入成功'
    return HttpResponse(json.dumps(recheck_ques_resp, cls=ComplexEncoder, ensure_ascii=False))

def GetCorrectQues(request):
    get_correct_ques_resp = {}
    get_correct_ques_req = json.loads(request.body.decode('utf_8'))
    ticket = get_correct_ques_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_correct_ques_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        get_correct_ques_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    teacher_account_id = AccountSystem.objects.filter(username=account_name).values()[0]['id']
    paper_id = get_correct_ques_req.get('paper_id')


    student_id_list = []
    student_info_list = StudentExamInfo.objects.filter(paper_detail_id=paper_id).values()
    for student_info in student_info_list:
        student_id_list.append(student_info['id'])
    teacher_correction_id_list = []
    teacher_correct_info_list = TeacherCorrectionList.objects.filter(student_account_id__in=student_id_list).values()
    is_auth = 0
    for teacher_correct_info in teacher_correct_info_list:
        if teacher_correct_info['teacher_account_id'] == teacher_account_id:
            is_auth = 1
        teacher_correction_id_list.append(teacher_correct_info['id'])
    if (is_auth == 0):
        get_correct_ques_resp['err_msg'] = ' 无本次考试相关权限'
        return HttpResponse(json.dumps(get_correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))
    paper_ques_id_list = []
    paper_ques_detail_list = examination.models.PaperIncludingQuestions.objects.filter(paper_detial_id=paper_id).values()
    for paper_ques_detail in paper_ques_detail_list:
        paper_ques_id_list.append(paper_ques_detail['id'])

    correct_info_list = list(CorrectTest.models.CorrectTestDetail.objects.filter(teacher_correct_details_id__in=teacher_correction_id_list,ques_detail_id__in=paper_ques_id_list)
                                                                     .order_by('ques_detail_id', 'teacher_correct_details_id').values())
    index = 0
    student_account_id = get_correct_ques_req.get('student_account_id', None)
    ques_id = get_correct_ques_req.get('ques_id', None)


    real_correct_info_list = []
    for correct_info in correct_info_list:
        real_correct_info = correct_info
        real_correct_info['ques_detail'] = GetPaperQuesById(correct_info['ques_detail_id'])
        real_correct_info['teacher_correct_details'] = GetStudentInfoAndTeacherNameByCorrectionId(correct_info['teacher_correct_details_id'])
        real_correct_info['recheck_teacher_name'] = GetUserNameById(correct_info['recheck_teacher_detail_id'])
        index = index + 1
        if student_account_id != None and real_correct_info['teacher_correct_details']['student_info']['id'] != student_account_id:
            continue
        if ques_id != None and real_correct_info['ques_detail']['id'] != ques_id:
            continue
        real_correct_info_list.append(real_correct_info)

    get_correct_ques_resp['err_msg'] = '判题记录获取成功'
    get_correct_ques_resp['correct_info_list'] = real_correct_info_list
    return HttpResponse(json.dumps(get_correct_ques_resp, cls=ComplexEncoder, ensure_ascii=False))

def GetGradeTable(request):
    get_grade_table_req = json.loads(request.body.decode('utf_8'))
    get_grade_table_resp = {}
    ticket = get_grade_table_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_grade_table_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_grade_table_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        get_grade_table_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_grade_table_resp, cls=ComplexEncoder, ensure_ascii=False))

    paper_id = get_grade_table_req.get('paper_id', None)
    if paper_id == None:
        get_grade_table_resp['err_msg'] = 'paper id为空'
        return HttpResponse(json.dumps(get_grade_table_resp, cls=ComplexEncoder, ensure_ascii=False))
    paper_ques_id_list = []
    paper_ques_detail_list = examination.models.PaperIncludingQuestions.objects.filter(
        paper_detial_id=paper_id).values()
    for paper_ques_detail in paper_ques_detail_list:
        paper_ques_id_list.append(paper_ques_detail['id'])
    correct_info_list = list(
        CorrectTest.models.CorrectTestDetail.objects.filter(ques_detail_id__in=paper_ques_id_list)
        .order_by('ques_detail_id', 'teacher_correct_details_id').values())
    map_student_info = {}
    map_ques_detail = {}
    map_score_detail = {}
    real_correct_info_list = []
    for correct_info in correct_info_list:
        real_correct_info = correct_info
        real_correct_info['ques_detail'] = GetPaperQuesById(correct_info['ques_detail_id'])
        map_ques_detail[real_correct_info['ques_detail']['id']] = real_correct_info['ques_detail']
        real_correct_info['teacher_correct_details'] = GetStudentInfoAndTeacherNameByCorrectionId(
            correct_info['teacher_correct_details_id'])
        map_student_info[real_correct_info['teacher_correct_details']['student_info']['id']] = real_correct_info['teacher_correct_details']['student_info']
        map_student_info[real_correct_info['teacher_correct_details']['student_info']['id']]['teacher_name'] = real_correct_info['teacher_correct_details']['teacher_name']
        real_correct_info['recheck_teacher_name'] = GetUserNameById(correct_info['recheck_teacher_detail_id'])
        map_score_detail[str(correct_info['ques_detail_id']) + '_' + str(real_correct_info['teacher_correct_details']['student_info']['id'])] = real_correct_info['student_score']
        real_correct_info_list.append(real_correct_info)

    index = 0
    grade_table = []
    for student_info in map_student_info.values():
        index = index + 1
        student_grade = {}
        student_grade['id'] = index
        student_grade['student_id'] = student_info['student_id']
        student_grade['name'] = student_info['student_name']
        student_grade['dept'] = student_info['student_dept']
        total_score = 0
        for ques_info in map_ques_detail.values():
            student_grade[ques_info['ques_name_in_paper']] = map_score_detail[str(ques_info['id']) + '_' + str(student_info['id'])]
            total_score = total_score + map_score_detail[str(ques_info['id']) + '_' + str(student_info['id'])]
        student_grade['total_score'] = total_score
        student_grade['teacher_name'] = student_info['teacher_name']
        grade_table.append(student_grade)

    get_grade_table_resp['err_msg'] = '成绩表获取成功'
    get_grade_table_resp['grade_table'] = grade_table
    return HttpResponse(json.dumps(get_grade_table_resp, cls=ComplexEncoder, ensure_ascii=False))


def SubmitJudgeMission(request):
    submit_judge_mission_req = json.loads(request.body.decode('utf_8'))
    submit_judge_mission_resp = {}
    ticket = submit_judge_mission_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        submit_judge_mission_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        submit_judge_mission_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))

    real_req = {}
    source_code = submit_judge_mission_req.get('source_code', None)
    if source_code == None:
        submit_judge_mission_resp['err_msg'] = 'source_code为空'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))
    real_req['source_code'] = source_code
    language_id = submit_judge_mission_req.get('language_id')
    if language_id == 1:  # C++ (GCC 9.2.0)
        language_id = 54
    elif language_id == 2:  # C (GCC 7.4.0)
        language_id = 48
    elif language_id == 3:  # Java (OpenJDK 13.0.1)
        language_id = 62
    elif language_id == 4:  # Python (3.8.1)
        language_id = 71
    else:
        submit_judge_mission_resp['err_msg'] = 'language_id未知'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))
    real_req['language_id'] = language_id
    time_limit = submit_judge_mission_req.get('time_limit', 1)
    real_req['cpu_time_limit'] = time_limit
    memory_limit = submit_judge_mission_req.get('memory_limit', 128)  #MB
    real_req['memory_limit'] = memory_limit * 1024
    ques_id = submit_judge_mission_req.get('ques_id', None)
    if ques_id == None:
        submit_judge_mission_resp['err_msg'] = 'ques_id为空'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))

    ques_detail = examination.models.Question.objects.filter(ques_id=ques_id).values()
    if (ques_detail.count() == 0):
        submit_judge_mission_resp['err_msg'] = '找不到题目信息'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))
    elif(ques_detail.count() > 1):
        submit_judge_mission_resp['err_msg'] = '题目信息异常'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))
    ques_detail = ques_detail[0]
    if ques_detail['ques_type'] != 4:
        submit_judge_mission_resp['err_msg'] = '此题不是编程题'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))
    test_set_id = ques_detail['test_set_id']
    test_set_detail = examination.models.TestSet.objects.filter(test_set_id=test_set_id).values()
    if (test_set_detail.count() == 0):
        submit_judge_mission_resp['err_msg'] = '找不到测试集信息'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))
    elif(test_set_detail.count() > 1):
        submit_judge_mission_resp['err_msg'] = '测试集信息异常'
        return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))
    test_set_detail = test_set_detail[0]

    url = 'http://127.0.0.1:2358/submissions'
    is_async = submit_judge_mission_req.get('is_async', False)
    if is_async == False:
        url = url + '?wait=true'
    result_list = []
    for i in range(1, 6, 1):
        input_name = 'test_set_input' + str(i)
        output_name = 'test_set_output' + str(i)
        if test_set_detail[input_name] == '' or test_set_detail[output_name] == '':
            break
        in_file_path = '/home/ubuntu/final_project/exam/media/' + test_set_detail[input_name]
        out_file_path = '/home/ubuntu/final_project/exam/media/' + test_set_detail[output_name]
        in_data = ''
        with open(in_file_path, 'r', encoding='utf-8') as f:
            in_data = in_data + f.read()
        real_req['stdin'] = in_data
        out_data = ''
        with open(out_file_path, 'r', encoding='utf-8') as f:
            out_data = out_data + f.read()
        real_req['expected_output'] = out_data
        judge_resp = EasyCurl(json.dumps(real_req, cls=ComplexEncoder, ensure_ascii=False), url, 'POST')
        result_list.append(judge_resp)
    submit_judge_mission_resp['err_msg'] = '判题任务提交成功'
    submit_judge_mission_resp['judge_info_list'] = list(result_list)
    return HttpResponse(json.dumps(submit_judge_mission_resp, cls=ComplexEncoder, ensure_ascii=False))


def GetJudgeResult(request):
    get_judge_result_req = json.loads(request.body.decode('utf_8'))
    get_judge_result_resp = {}
    ticket = get_judge_result_req.get('ticket')
    account_name = ''
    account_name = TeacherAccount.logic.CheckTicket(ticket)
    try:
        account_name = TeacherAccount.logic.CheckTicket(ticket)
    except Exception:
        get_judge_result_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_judge_result_resp, cls=ComplexEncoder, ensure_ascii=False))
    if (account_name == ''):
        get_judge_result_resp['err_msg'] = '票据验证失败'
        return HttpResponse(json.dumps(get_judge_result_resp, cls=ComplexEncoder, ensure_ascii=False))

    token = get_judge_result_req.get('token', None)
    if token == None:
        get_judge_result_resp['err_msg'] = 'token为空'
        return HttpResponse(json.dumps(get_judge_result_resp, cls=ComplexEncoder, ensure_ascii=False))
    url = 'http://127.0.0.1:2358/submissions/' + token
    get_judge_result_resp = EasyCurl('', url, 'GET')
    return HttpResponse(get_judge_result_resp)
