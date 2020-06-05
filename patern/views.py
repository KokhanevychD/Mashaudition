from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from patern.forms import PatternBodyForm, PatternTypeForm
from patern.models import PatternBody, PatternType
from audit.models import PlayerAudit


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
        self.object = form.save(commit=False)
        self.object.pattern_type = PatternType.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class PatternBodyDel(DeleteView):
    model = PatternBody
    success_url = reverse_lazy('pattern:list')


class PatternTypeDel(DeleteView):
    model = PatternType
    success_url = reverse_lazy('pattern:list')


def action_type_remake(request, **kwargs):
    pattern = PatternBody.objects.get(pk=kwargs['pk'])
    audit_query = PlayerAudit.objects.all()
    for item in audit_query:
        if pattern.pattern in item.action:
            item.action_type = pattern.pattern_type.pattern_name
            item.save()
    return redirect('player:list')
