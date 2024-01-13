from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from .models import Test, Question, TestStatus, UserAnswers, Time, TestHour, ExcelFile
from django.contrib.auth.models import User
import random
import json
from datetime import datetime, timedelta
import pytz
import pandas as pd
from django.conf import settings
from .forms import CreateTestForm, AddQuestionForm


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

    time = Time.objects.filter(user=user, test=test).first()

    if (time is None):
        time = Time.objects.create(
            user=request.user,
            test=test,
        )

    # test_hour = TestHour.objects.filter(test=test).first()
    time_a = datetime.now().astimezone(pytz.utc).replace(tzinfo=None)
    time_b = datetime(year=1, month=1, day=1, hour=time_a.hour,
                      minute=time_a.minute, second=time_a.second)

    # aware_datetime2 = target_timezone.localize(time.start_time)
    time_c = time.start_time.astimezone(pytz.utc).replace(tzinfo=None)
    time_d = datetime(year=1, month=1, day=1, hour=time_c.hour,
                      minute=time_c.minute, second=time_c.second)
    time_diff2 = time_b-time_d

    test_hour = TestHour.objects.get(test=test)

    time_diff = timedelta(hours=test_hour.time.hour, minutes=test_hour.time.minute,
                          seconds=test_hour.time.second) - time_diff2

    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds // 60) % 60
    seconds = time_diff.seconds % 60

    print(f"{hours}:{minutes}:{seconds}")

    return render(request, 'portal/test.html', {
        'test': test,
        'nums': nums,
        'question_len': len(question),
        'saved_answers': json_string,
        'first_qid': questions[0]["id"],
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
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
    is_form_invalid = False

    if (request.method == "POST"):
        form = CreateTestForm(request.POST)

        if (form.is_valid()):
            form_data = form.cleaned_data
            test_name = form_data["test_name"]
            test_form = Test.objects.create(test_name=test_name)
            time = datetime(year=1, month=1, day=1,
                            hour=1, minute=0, second=0)

            TestHour.objects.create(test=test_form, time=time)

            return HttpResponseRedirect(reverse('create-test'))
        else:
            is_form_invalid = True

    form = CreateTestForm()

    return render(request, 'portal/admin.html', {
        "tests": test,
        "form": form,
        "is_form_valid": is_form_invalid,
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


def edit_test(request, testID):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')

    test = Test.objects.filter(id=testID).first()
    question = Question.objects.filter(test=test)

    test = Test.objects.filter(id=testID).first()

    is_form_invalid = False
    if (request.method == "POST"):
        form = AddQuestionForm(request.POST)

        if(form.is_valid()):
            form_data = form.cleaned_data
            question = form_data['question']
            op1 = form_data['op1']
            op2 = form_data['op2']
            op3 = form_data['op3']
            op4 = form_data['op4']
            correct_op = int(form_data['correct_op'])

            questionIsCode = form_data['questionIsCode']
            op1IsCode = form_data['op1IsCode']
            op2IsCode = form_data['op2IsCode']
            op3IsCode = form_data['op3IsCode']
            op4IsCode = form_data['op4IsCode']

            Question.objects.create(
                test=test,
                question=question,
                op1=op1,
                op2=op2,
                op3=op3,
                op4=op4,
                correct_op=correct_op,
                questionIsCode=questionIsCode,
                op1IsCode=op1IsCode,
                op2IsCode=op2IsCode,
                op3IsCode=op3IsCode,
                op4IsCode=op4IsCode,
            )

            test.test_question_no += 1
            test.save()

            return HttpResponseRedirect(reverse('create-question', args=[test.id]))
        else:
            is_form_invalid = True
            print('=================================================')

    form = AddQuestionForm()

    return render(request, 'portal/edit-test.html', {
        'tests': test,
        'questions': question,
        'form': form,
        'is_form_invalid': is_form_invalid,
    })


def create_question(request, testID):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')


    return redirect(reverse('edit-test', args=[testID]))


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
            correct_op = Question.objects.filter(question=question, test=test).first().correct_op

            if (correct_op == user_answer.user_option):
                score += 1

        user_details.append({"id": user.id,
                             "username": user.username,
                             "test_status": test_status.test_status,
                             "score": score})

    return render(request, "portal/user-details.html", {
        "user_details": user_details,
        "tests": test,
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


def reset_user(request, userID, testID):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')

    user = User.objects.filter(id=userID).first()
    test = Test.objects.filter(id=testID).first()

    time = Time.objects.get(user=user, test=test)
    time.delete()

    ts = TestStatus.objects.filter(user=user, test=test).first()
    ts.test_status = '1'
    ts.save()

    return JsonResponse({
        "message": "User successfully reseted!"
    })


def set_time(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (request.method == "POST"):
        data = json.loads(request.body)

        test_id = data["test_id"]
        time_now = data["time_now"]

        hour = ""
        minute = ""
        second = ""

        i = 0

        while (time_now[i] != ':'):
            hour += time_now[i]
            i += 1

        i += 1

        while (time_now[i] != ':'):
            minute += time_now[i]
            i += 1
        i += 1

        while (i < len(time_now)):
            second += time_now[i]
            i += 1

        hour = int(hour)
        minute = int(minute)
        second = int(second)

        test = Test.objects.get(id=test_id)
        time = TestHour.objects.get(test=test)
        time.delete()

        tm = datetime(year=2024, month=12, day=12, hour=hour,
                      minute=minute, second=second)

        TestHour.objects.create(test=test, time=tm)

    return JsonResponse({
        'message': 'Time was set successfully'
    })


def upload_questions(request, testID):
    if (request.method == 'POST'):
        file = request.FILES['questions']
        obj = ExcelFile.objects.create(
            file=file
        )
        path = file.file
        df = pd.read_excel(path)
        test = Test.objects.get(id=testID)

        for d in df.values:
            question = d[0]
            questionIsCode = d[1]
            op1 = d[2]
            op1IsCode = d[3]
            op2 = d[4]
            op2IsCode = d[5]
            op3 = d[6]
            op3IsCode = d[7]
            op4 = d[8]
            op4IsCode = d[9]
            correct_op = d[10]

            questionObj = Question.objects.filter(
                test=test,
                question=question,
                op1=op1,
                op2=op2,
                op3=op3,
                op4=op4,
                correct_op=correct_op,
                questionIsCode=questionIsCode,
                op1IsCode=(op1IsCode),
                op2IsCode=op2IsCode,
                op3IsCode=op3IsCode,
                op4IsCode=op4IsCode,
            ).first()

            if (questionObj is None):
                Question.objects.create(
                    test=test,
                    question=question,
                    op1=op1,
                    op2=op2,
                    op3=op3,
                    op4=op4,
                    correct_op=correct_op,
                    questionIsCode=questionIsCode,
                    op1IsCode=op1IsCode,
                    op2IsCode=op2IsCode,
                    op3IsCode=op3IsCode,
                    op4IsCode=op4IsCode,
                )
                test.test_question_no += 1
                test.save()

    return HttpResponseRedirect(reverse('edit-test', args=[testID]))


def upload_users(request, testID):
    if (request.method == "POST"):
        file = request.FILES['questions']
        obj = ExcelFile.objects.create(
            file=file
        )
        path = file.file
        df = pd.read_excel(path)
        test = Test.objects.get(id=testID)

        for d in df.values:
            username = d[0]
            password = str(d[1])
            first_name = d[2]
            last_name = d[3]

            print("Password: ", password)

            user = User.objects.filter(
                username=username,
                password=password
            )

            if (user.first() is None):
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )

                TestStatus.objects.create(
                    user=user,
                    test=test,
                    test_status='1',
                )

    return HttpResponseRedirect(reverse('user-details', args=[testID]))


def create_test(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('login'))

    if (not request.user.is_superuser):
        return HttpResponseForbidden('You are not allowed to access this resource!')

    # if (request.method == "POST"):
    #     form = CreateTestForm(request.POST)
    #     is_form_valid = True

    #     if(form.is_valid()):
    #         form_data = form.cleaned_data
    #         test_name = form_data["test_name"]
    #         test = Test.objects.create(test_name=test_name)
    #         time = datetime(year=1, month=1, day=1,
    #                         hour=1, minute=0, second=0)

    #         TestHour.objects.create(test=test, time=time)
    #     else:
    #         is_form_valid = False

    return HttpResponseRedirect(reverse('admin'))
