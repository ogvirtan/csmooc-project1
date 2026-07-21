from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def create_poll(request):
    return render(request, 'polls/create-poll.html')

@login_required
def commit_create_poll(request):
    poll = Question.objects.create(
        #question_text = request.POST['title'],
        question_text = request.GET['title'],
        asker = request.user,
        pub_date = timezone.now()
    )

    #choices = request.POST.getlist('choice')
    choices = request.GET.getlist('choice')

    for entry in choices:
        Choice.objects.create(question=poll,
        choice_text = entry)

    return HttpResponseRedirect(reverse('polls:index'))

# @login_required
# def user_page(request):
#     user = request.user
#     search = request.GET.get('query', '')
    
#     polls = Question.objects.filter(
#         question_text__icontains=search,
#         asker=user
#     )
#     return render(request, 'polls/user-page.html', {'user': user, 'polls': polls, 'search': search})

@login_required
def user_page(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    search = request.GET.get('query', '')
    
    with connection.cursor() as cursor:
        query = f"SELECT * FROM polls_question WHERE asker_id = {user_id} AND question_text LIKE '%{search}%'"
        cursor.execute(query)
        polls = cursor.fetchall()
    return render(request, 'polls/user-page.html', {'user': user, 'polls': polls, 'search': search})

def new_user(request):
    return render(request, 'polls/new-user.html')

def create_user(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.create_user(username=username,
                    password=password)
    except:
        return render(request, 'polls/new-user.html', {
            'error_message': 'something went wrong'
        })
    return HttpResponseRedirect(reverse('polls:index'))

def log_in(request):
    return render(request, 'polls/login.html')

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:index'))

def commit_login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return render(request, 'polls/login.html', {
                'error_message': 'Invalid username or password.'
            })

    except:
        return render(request, 'polls/login.html', {
                'error_message': 'something went wrong'
            })