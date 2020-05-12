from django.urls import path

from files.views import DocumentUpload

app_name = 'files'
urlpatterns = [
    path('upload', DocumentUpload.as_view(), name='upload'),
    path('upload/<int:pk>', DocumentUpload.as_view(), name='upload-pk'),
]
