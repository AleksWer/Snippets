from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.forms import SnippetForm, UserRegistrationForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def index_page(request):
    context = {'pagename': 'PythonBin'}
    if request.method == 'POST':
        snippet_id = request.POST.get("snippet_id")
        return redirect("snippet-detail", snippet_id)
    else:
        return render(request, 'pages/index.html', context)


@login_required
def add_snippet_page(request):
    # Получаем чистую форму для заполнения
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    # Создаем новый Сниппет(данные от формы)
    if request.method == "POST":
        form = SnippetForm(request.POST, request.FILES)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
                return redirect("snippets-list")
        return render(request, 'pages/add_snippet.html', {'form': form})


@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets,
        'count': snippets.count()
        }
    return render(request, 'pages/view_snippets.html', context)


def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'count': snippets.count()
        }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippet': snippet,
        'type': 'view'
        }
    return render(request, 'pages/snippet_detail.html', context)


def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()
    return redirect("snippets-list")


def snippet_edit(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    # Получаем страницу с данными сниппета
    if request.method == "GET":
        context = {
            'pagename': 'Просмотр сниппетов',
            'snippet': snippet,
            'type': 'edit'
            }
        return render(request, 'pages/snippet_detail.html', context)  #snippet_detail.html
    # Изменяем атрибуты сниппета на основе данных из формы и сохраняем в базу
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        snippet.creation_date = data_form["creation_date"]
        snippet.public = data_form.get('public', False)
        snippet.save()
        return redirect("snippets-list")


def create_user(request):
    context = {'pagename': 'Создание нового пользователя'}
    # Получаем чистую форму для заполнения
    if request.method == "GET":
        form = UserRegistrationForm()      
        context['form'] = form
        return render(request, 'pages/registration.html', context)
    # Создаем нового пользователя(данные от формы)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        context['form'] = form
        return render(request, 'pages/registration.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            context = {
                'pagename': 'PythonBin',
                'errors': ['wrong username or password']

                }
            return render(request, 'pages/index.html', context)
    return redirect('home')




def logout(request):
    auth.logout(request)
    return redirect('home')
    # реализуем перенаправление на ту страницу, на которой логинился пользователь
    # return redirect(request.META.get('HTTP_REFERER', '/'))