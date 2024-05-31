from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.db import connection

from .models import Choice, Question
import json


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
        return Question.objects.all()
        # this leads to unauthorized preview of upcoming polls (flaw 4)
        '''
        return Question.objects.filter(pub_date__lte=timezone.now())
        '''

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    data = json.loads(request.body)
    choice_ids = data['choice']
    with connection.cursor() as cursor:
        for i, choice_id in enumerate(choice_ids):
            if i != 0:
                cursor.execute(choice_id)
            else:
                cursor.execute(f"UPDATE polls_choice SET votes = votes + 1 WHERE id = '{choice_id}'")
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
    # Raw SQL queries should not be allowed to run (flaw 5)
    '''
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
    '''