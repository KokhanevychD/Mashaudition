import os
from xlrd import XLRDError

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from files.forms import DocumentForm


class DocumentUpload(CreateView):
    # create PlayerAudit objects from uploaded file
    # after parsing delete file, and instance of DocumentForm
    form_class = DocumentForm
    template_name = 'files/upload.html'
    success_url = reverse_lazy('player:list')

    def form_valid(self, form):
        self.object = form.save()
        try:
            self.object.parse()
        except XLRDError:
            os.remove(self.object.excel.path)
            self.object.delete()
            return redirect('files:upload')
        os.remove(self.object.excel.path)
        self.object.delete()
        return redirect('player:list')
