#from django.shortcuts import render
#once I switch all views to use render I dont need HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from .models import Question

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list' : latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html",{'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html',{'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #redisplay the question voting form
        return render(request, 'polls/detail.html', {
                'question':question,
                'error_message': "You did not select a choice",
                })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #always return an HttpResponseRedirect after successfully dealing
        #with POST data. This prevents data from being posted twice if a 
        #user hits the back button.
        return HttpResponseRedirect(reverse('polls:results',
                    args=(question.id,)))

    return HttpResponse("You are voting on question %s." % question_id)
