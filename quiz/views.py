# -*- coding: UTF-8 -*-

from random import Random
import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from .models import Question

# Create your views here.
DIFFICULTY = 50


def start(request):
    numbers = {question.pk for question in Question.objects.all()}
    question_to_render = Random().sample(numbers, 1)[0]

    #because Set is non-serializable
    request.session['non_seen'] = list(numbers - {question_to_render})
    request.session['current'] = question_to_render
    request.session['seen'] = [question_to_render]
    request.session['user_score'] = 0
    request.session['computer_score'] = 0

    context = dict()
    context['user_score'] = 0
    context['computer_score'] = 0
    context['question'] = Question.objects.get(pk=question_to_render)
    context['answers'] = context['question'].answer_set.all().order_by('?')

    return render(request, 'quiz/index.html', context)


@ensure_csrf_cookie
def handle_user_answer(request):
    if request.body:
        question_number = request.session.get('current')
        current_question_instance = Question.objects.get(pk=question_number)

        response = dict()

        received_data = json.loads(request.body.decode("utf-8"))
        user_answer = int(received_data.get('answer'))
        correct_answer_pk = current_question_instance.answer_set.get(is_correct=True).pk

        response['correct_answer'] = correct_answer_pk
        response['user_answer'] = user_answer
        if correct_answer_pk == user_answer:
            request.session['user_score'] += 1
            response['is_user_correct'] = True
        else:
            response['is_user_correct'] = False

        if is_computer_correct(DIFFICULTY):
            response['computer_answer'] = correct_answer_pk
            response['is_computer_correct'] = True
            request.session['computer_score'] += 1
        else:
            response['computer_answer'] = return_wrong_answer(current_question_instance)
            response['is_computer_correct'] = False

        response['user_score'] = request.session['user_score']
        response['computer_score'] = request.session['computer_score']

        return JsonResponse(response)


def render_next_question(request):
    numbers = request.session.get('non_seen')
    if len(numbers) == 0:
        numbers = {question.pk for question in Question.objects.all()}
    while True:
        question_number_to_render = Random().sample(numbers, 1)[0]
        if not Question.objects.filter(pk=question_number_to_render).exists():
            numbers -= {question_number_to_render}
        else:
            break
    current_question_instance = Question.objects.get(pk=question_number_to_render)

    request.session['non_seen'] = list(set(numbers) - {question_number_to_render})
    request.session['current'] = question_number_to_render

    context = dict()
    context['user_score'] = request.session['user_score']
    context['computer_score'] = request.session['computer_score']
    context['question'] = current_question_instance
    context['answers'] = context['question'].answer_set.all().order_by('?')

    return render(request, 'quiz/index.html', context)


def is_computer_correct(difficulty):
    if Random().randint(0, 99) < difficulty:
        return True


def return_wrong_answer(question):
    for answer in question.answer_set.all():
        if not answer.is_correct:
            return answer.pk
