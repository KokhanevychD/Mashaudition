from django.urls import path

from patern.views import (PatternTypeList,
                          PatternBodyCreate,
                          PatternTypeCreate,
                          PatternBodyDel)


app_name = 'pattern'
urlpatterns = [
    path('', PatternTypeList.as_view(), name='list'),
    path('create/body', PatternBodyCreate.as_view(), name='new-body'),
    path('create/type', PatternTypeCreate.as_view(), name='new-type'),
    path('del/<int:pk>', PatternBodyDel.as_view(), name='del-body')
]