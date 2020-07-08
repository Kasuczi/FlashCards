from django.shortcuts import render, HttpResponse
from .models import FlashcardsModel
import random
from .forms import UserRegistrationForm, LoginForm
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def fiszka_main(request):
    login_form = LoginForm()
    request_data = request
    if "username" in dict(request.POST) and "password" in dict(request.POST):
        login_form_function(request_data)
    return render(request, 'main_flashcard/template.html',
                  {'login_form': login_form})


def fiszka_proper(request):
    #  Formularz w pop upie
    login_form = LoginForm()
    request_data = request
    if "username" in dict(request.POST) and "password" in dict(request.POST):
        login_form_function(request_data)

    #  Wyświetlanie kategorii
    get_categories = FlashcardsModel.objects.values('flashcard_category').distinct()
    list_of_categories = [category['flashcard_category'] for category in
                          get_categories]

    #  Losowanie fiszki i obsługa kategorii
    list_of_checked_values = dict(request.POST)
    flashcard_list = FlashcardsModel.objects.filter(flashcard_category__in=list_of_checked_values).values_list('flashcard_id', flat=True)
    try:
        flashcard_object = FlashcardsModel.objects.get(pk=random.choice(flashcard_list))
    except IndexError:
        flashcard_list = FlashcardsModel.objects.values_list('flashcard_id', flat=True)
        flashcard_object = FlashcardsModel.objects.get(pk=random.choice(flashcard_list))

    list_of_answers = flashcard_object.user_answer_1, flashcard_object.user_answer_2, flashcard_object.user_answer_3, flashcard_object.user_answer_4
    return render(request, 'main_flashcard/fiszka.html',
                  {'list_of_categories': list_of_categories,
                   'flashcard_object': flashcard_object,
                   'list_of_answers': list_of_answers,
                   'list_of_checked_values': list_of_checked_values,
                   'login_form': login_form})


def my_account(request):
    user = request.user
    return render(request, 'main_flashcard/my_account.html', {'altUser': user})


def login_form_function(request_data):
    login_form = LoginForm(request_data.POST)
    if login_form.is_valid():
        data = login_form.cleaned_data
        user = authenticate(username=data['username'],
                            password=data['password'])
        if user is not None:
            if user.is_active:
                login(request_data, user)
            else:
                return HttpResponse('Konto zablokowane')
        else:
            return HttpResponse('Nieprawidłowe dane')


def sign_up(request):
    if request.method == 'POST':
        f = UserRegistrationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('fiszka_main')

    else:
        f = UserRegistrationForm()

    return render(request, 'main_flashcard/signup.html', {'form': f})


def create_flash(request):
    if request.method == 'POST':
        title = request.POST['title']
        text_content = request.POST['text_content']
        answer = request.POST['answer']

        FlashcardsModel.objects.create(
            title=title,
            text_content=text_content,
            answer=answer
        )
    else:
        title = ''
        text_content = ''
        answer = ''
    return render(request, 'main_flashcard/adding_new_flashcard.html', {'title': title,
                                                                        'text_content': text_content,
                                                                        'answer': answer})


@login_required
@require_POST
def flashcard_like_system(request):
    flashcard_id = request.POST.get('id')
    action = request.POST.get('action')
    if flashcard_id and action:
        try:
            flashcard = FlashcardsModel.objects.get(flashcard_id=flashcard_id)
            if action == 'like':
                flashcard.users_like.add(request.user)
            else:
                flashcard.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})
