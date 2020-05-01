import os
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from files.forms import DocumentForm


class DocumentUpload(CreateView):
    form_class = DocumentForm
    template_name = 'files/upload.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.parse()
        # del file and file obj, dont need it
        os.remove(self.object.excel.path)
        self.object.delete()
        return redirect('home:home')
