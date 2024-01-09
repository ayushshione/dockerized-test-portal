from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from .models import Test, Question, TestStatus, UserAnswers, Time
import random
import json


def err1_page(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'portal/err1.html')


def test_page(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (request.session.get('test_id') is None):
        return HttpResponseRedirect(reverse('err1'))

    test = Test.objects.filter(id=request.session.get('test_id')).first()
    question = (Question.objects.filter(test=test))
    user = request.user

    test_status = TestStatus.objects.filter(user=user, test=test).first()

    if (test_status.test_status == '2'):
        return HttpResponseRedirect(reverse('finish-test'))

    saved_options = list(UserAnswers.objects.filter(user=user))
    question_list = list(question)
    saved_answers = {}

    for option in saved_options:
        if (option.question in question_list):
            saved_answers[option.question.id] = option.user_option

    json_string = json.dumps(saved_answers)

    questions = []

    for i in question:
        q = {
            'id': i.id,
            'question': i.question,
            'questionIsCode': i.questionIsCode,
            'op1': i.op1,
            'op1IsCode': i.op1IsCode,
            'op2': i.op2,
            'op2IsCode': i.op2IsCode,
            'op3': i.op3,
            'op3IsCode': i.op3IsCode,
            'op4': i.op4,
            'op4IsCode': i.op4IsCode,
        }

        questions.append(q)

    if (request.session.get('questions') == None):
        random.shuffle(questions)
        request.session['questions'] = questions
    else:
        questions = request.session['questions']

    nums = []

    for i in range(1, len(question)+1):
        nums.append({
            'question_id': questions[i-1]["id"],
            'i': i,
        })

    time_check = Time.objects.filter(user=user, test=test)

    if (len(time_check) > 0):
        time_check.delete()

    Time.objects.create(
        user=request.user,
        test=test,
    )

    return render(request, 'portal/test.html', {
        'test': test,
        'nums': nums,
        'question_len': len(question),
        'saved_answers': json_string,
        'first_qid': questions[0]["id"]
    })


def user_page(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    test_status = TestStatus.objects.filter(user=request.user).first()

    if (test_status.test_status != '1'):
        return HttpResponseRedirect(reverse('err1'))

    test = Test.objects.filter(id=test_status.test.id).first()
    request.session["test_id"] = test.id

    return render(request, 'portal/user.html', {
        "test_status": test_status,
        "test": test,
    })


def admin_panel(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')

    test = Test.objects.all()

    return render(request, 'portal/admin.html', {
        "tests": test,
    })


def login_user(request):
    if request.user.is_authenticated:
        if (request.user.is_superuser):
            return HttpResponseRedirect(reverse('admin'))
        return HttpResponseRedirect(reverse('user'))

    if (request.method == 'POST'):
        username = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if (user.is_superuser):
                return HttpResponseRedirect(reverse('admin'))

            return HttpResponseRedirect(reverse('user'))
        else:
            return render(request, 'portal/login.html', {
                'error': True
            })

    return render(request, 'portal/login.html', {
        'error': False
    })


def logout_user(request):
    if (request.session.get('questions') is not None):
        del request.session['questions']
        request.session.modified = True
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def create_test(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')

    if (request.method == "POST"):
        test_name = request.POST["test-name"]
        Test.objects.create(test_name=test_name)

    return HttpResponseRedirect(reverse('admin'))


def edit_test(request, testID):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')

    test = Test.objects.filter(id=testID).first()
    question = Question.objects.filter(test=test)

    return render(request, 'portal/edit-test.html', {
        'tests': test,
        'questions': question
    })


def create_question(request, testID):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')

    test = Test.objects.filter(id=testID).first()

    if (request.method == "POST"):
        question = request.POST['question']
        op1 = request.POST['op1']
        op2 = request.POST['op2']
        op3 = request.POST['op3']
        op4 = request.POST['op4']

        whichAreCode = request.POST.getlist('checks[]')
        list_sh = ['question', 'op1', 'op2', 'op3', 'op4']
        dict_sh = {}

        for sh in list_sh:
            if (sh in whichAreCode):
                dict_sh[sh] = True
            else:
                dict_sh[sh] = False

        correct_op = request.POST['correct_op']

        Question.objects.create(
            test=test,
            question=question,
            op1=op1,
            op2=op2,
            op3=op3,
            op4=op4,
            correct_op=correct_op,
            questionIsCode=dict_sh['question'],
            op1IsCode=dict_sh['op1'],
            op2IsCode=dict_sh['op2'],
            op3IsCode=dict_sh['op3'],
            op4IsCode=dict_sh['op4'],
        )

        test.test_question_no += 1
        test.save()

    return redirect(reverse('edit-test', args=[test.id]))


def delete_question(request, questionID):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')

    question = Question.objects.filter(id=questionID).first()
    test = question.test

    question.delete()

    test.test_question_no -= 1
    test.save()

    return redirect(reverse('edit-test', args=[test.id]))

def user_details(request, testID):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')

    test = Test.objects.filter(id=testID).first()
    test_statuses = TestStatus.objects.filter(test=test)

    user_details = []

    for test_status in test_statuses:
        user = test_status.user
        test = test_status.test
        
        user_answers = UserAnswers.objects.filter(user=user)
        score = 0

        for user_answer in user_answers:
            question = user_answer.question
            correct_op = Question.objects.filter(question=question, test=test)

            if(correct_op == user_answer.user_option):
                score += 1
        
        user_details.append({"id": user.id, 
                                 "username": user.username, 
                                 "test_status": test_status.test_status, 
                                 "score": score})
    

    return render(request, "portal/user-details.html", {
        "user_details": user_details
    })

def get_next_question(request, questionnum):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    questions = request.session.get('questions')

    return JsonResponse(questions[questionnum-1])


def save_question(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (request.method == "POST"):
        data = json.loads(request.body)
        user_option = data["user_option"]

        question = Question.objects.filter(id=data["question_id"]).first()
        user = request.user

        user_answer = UserAnswers.objects.filter(
            question=question, user=user).first()

        if (user_answer is None):
            user_answer = UserAnswers()

        user_answer.user = user
        user_answer.question = question
        user_answer.user_option = user_option

        user_answer.save()

        return JsonResponse({
            "message": "User Answer Saved"
        })

    return JsonResponse({
        "message": "This method is not allowed"
    })


def finish_test(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (request.session.get('test_id') is None):
        return HttpResponseRedirect(reverse('test'))

    test = Test.objects.filter(id=request.session.get('test_id')).first()
    user = request.user

    test_status = TestStatus.objects.filter(test=test, user=user).first()

    if (test_status is not None):
        test_status.test_status = '2'
        test_status.save()
        return HttpResponseRedirect(reverse('logout'))

    return HttpResponseRedirect(reverse('test'))


def get_test_status(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    test = Test.objects.filter(id=request.session.get('test_id')).first()
    user = request.user

    test_status = TestStatus.objects.filter(test=test, user=user).first()

    return JsonResponse({
        "test_status": test_status.test_status
    })
