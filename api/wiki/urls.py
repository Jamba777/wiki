from django.urls import path, include

from .views import (
    CreatePageApiView,
    ListPageApiView,
    GetPageVersionsApiView,
    UpdatePageApiView,
    GetPageSingleVersionApiView,
    PageSetCurrentVersionApiView,
)

app_name = 'api.wiki'

urlpatterns = [
    path('create/', CreatePageApiView.as_view(), name='page-create'),
    path('pages/', ListPageApiView.as_view(), name='pages-list'),
    path('page/<int:pk>/', include([

        path('', GetPageVersionsApiView.as_view(), name='pages-versions'),
        path('update/', UpdatePageApiView.as_view(), name='page-update'),
        path('version/<int:version_id>/', include([

            path('', GetPageSingleVersionApiView.as_view(), name='page-get-version'),
            path('current/', PageSetCurrentVersionApiView.as_view(), name='page-set-current')
        ])),

    ])),
]