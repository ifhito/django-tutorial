from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template import loader
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
import csv
from django.views import generic
from django_pandas.io import read_frame
import pandas as pd
# # Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list':latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question':question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question':quesion})



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5] 

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(keyError, Choice.DoesNotExist):
        return render(request, 'poll/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def test(request):
    try:
        data = Question.objects.all()
    except Exception as e:
        print(e)
    else:
        df = read_frame(data)
        df['本番'] = '本'
        response = HttpResponse(content_type='text/csv; charset=CP932')
        response['Content-Disposition'] = 'attachment; filename ="' + "test" + '.csv"'
        df.to_csv(response, sep=",", index=False, encoding="utf-8-sig")
        return response