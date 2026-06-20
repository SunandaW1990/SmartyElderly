from django.shortcuts import render
from django.db.models import Prefetch
from django.views.generic import ListView
from .models import Manual, LifeFilm

class ManualDetailListView(ListView):
    model = Manual
    template_name = 'manuals/learns.html'
    context_object_name = 'manuals'

    '''
    def get_queryset(self):
        # Filter the primary table before it is passed to the context
        return Manual.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
            # 1. Call the base implementation to get the default context dictionary
            context = super().get_context_data(**kwargs)
            
            # 2. Retrieve extra data from other tables and add them to context
            context['lifefilm'] = LifeFilm.objects.filter(is_active=True).order_by('-creation_date')
            context['manualdetail'] = ManualDetail.objects.filter(is_active=True).order_by('-creation_date')
            
            # 3. Return the updated context
            return context    
    '''

    def get_queryset(self):
            # 1. Define how the related questions should be filtered and sorted
            custom_lifefilm_queryset = LifeFilm.objects.filter(
                is_active=True
            ).order_by('seq')

            # 2. Apply this rule to the prefetch lookup
            return Manual.objects.prefetch_related(
                Prefetch(
                    'lifefilm_set', 
                    queryset=custom_lifefilm_queryset
                )
            ).filter(is_active=True).order_by('creation_date', 'id')



# Create your views here.
def manual(request):
    context = {"input": ["Testing Manual"]}
    return render(request, "manuals/manual.html", context)
