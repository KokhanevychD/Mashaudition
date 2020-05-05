from django.urls import path

from patern.views import (PatternTypeList,
                          PatternBodyCreate,
                          PatternTypeCreate,
                          PatternBodyDel,
                          PatternTypeDel,
                          action_type_remake,
                          )


app_name = 'pattern'
urlpatterns = [
    path('', PatternTypeList.as_view(), name='list'),
    path('create/body', PatternBodyCreate.as_view(), name='new-body'),
    path('create/type', PatternTypeCreate.as_view(), name='new-type'),
    path('del/body/<int:pk>', PatternBodyDel.as_view(), name='del-body'),
    path('del/type/<int:pk>', PatternTypeDel.as_view(), name='del-type'),
    path('remake/<int:pk>', action_type_remake, name='remake-action')
]