from django.shortcuts import render
from django.db.models import Prefetch
from django.views.generic import ListView
from .models import GuideScenario, GuideQuestion
#from django.contrib.auth.models import User

class ScenarioQuestionListView(ListView):
    model = GuideScenario
    template_name = 'guides/emgs.html'
    context_object_name = 'scenarios'

    #def get_queryset(self):
    #    # Prefetch the foreign key relationship to keep it fast
    #    return GuideScenario.objects.prefetch_related('guidequestion_set').all

    def get_queryset(self):
            # 1. Define how the related questions should be filtered and sorted
            custom_question_queryset = GuideQuestion.objects.filter(
                is_active=True
            ).order_by('-creation_date')

            # 2. Apply this rule to the prefetch lookup
            return GuideScenario.objects.prefetch_related(
                Prefetch(
                    'guidequestion_set', 
                    queryset=custom_question_queryset
                )
            ).filter(is_active=True).order_by('-creation_date')

'''
    # Add this method to pass extra data to the template
    def get_context_data(self, **kwargs):
        # 1. Get the existing context data (contains your 'scenarios' list)
        context = super().get_context_data(**kwargs)
        
        # 2. Add the currently logged-in user to the context
        context['current_user'] = self.request.user
        
        # 3. (Optional) Example if you want to pull a specific target user by ID from the URL
        # user_id = self.kwargs.get('user_id')
        # context['target_user'] = User.objects.get(id=user_id)
        
        return context
'''    

# Create your views here.
def guide(request):
    context = {"input": ["Testing Guide"]}
    return render(request, "guides/guide.html", context)

'''
def emg(request):
    scenario = GuideScenario.objects.filter(is_active=True).order_by('-creation_date')
    question = GuideQuestion.objects.filter(is_active=True).order_by('-creation_date')
    context = {"input": ["Emgergency"]}
    return render(request, "guides/emg.html", context)
'''