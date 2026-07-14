from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import connection

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.GET['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def create_poll(request):
    return render(request, 'polls/create-poll.html')

def commit_create_poll(request):
    poll = request.POST['title']
    created = timezone.now()
    asker = request.user.id

    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO polls_question (question_text, pub_date, asker_id) VALUES ('{poll}', '{created}', '{asker}')")

    question_id = cursor.lastrowid
    question = Question.objects.get(id=question_id)
    choices = request.POST.getlist('choice')

    for entry in choices:
        Choice.objects.create(question=question,
        choice_text = entry)

    return HttpResponseRedirect(reverse('polls:index'))

def user_page(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    polls = Question.objects.filter(asker=user_id)
    return render(request, 'polls/user-page.html', {'user': user, 'polls': polls})

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