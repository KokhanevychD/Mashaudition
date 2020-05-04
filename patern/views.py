from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy

from patern.forms import PatternBodyForm, PatternTypeForm
from patern.models import PatternBody, PatternType


class PatternTypeCreate(CreateView):
    form_class = PatternTypeForm
    template_name = 'patern/create.html'
    success_url = reverse_lazy('pattern:list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PatternTypeList(ListView):
    model = PatternType
    context_object_name = 'obj_list'
    template_name = 'patern/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Паттерны'
        return context


class PatternBodyCreate(CreateView):
    form_class = PatternBodyForm
    template_name = 'patern/create.html'
    success_url = reverse_lazy('pattern:list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PatternBodyDel(DeleteView):
    model = PatternBody
    success_url = reverse_lazy('pattern:list')
