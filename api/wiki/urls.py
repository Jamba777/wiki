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
    path('page/<int:pk>/', GetPageVersionsApiView.as_view(), name='pages-versions'),
    path('page/<int:pk>/update/', UpdatePageApiView.as_view(), name='page-update'),
    path('page/<int:pk>/version/<int:version_id>/', GetPageSingleVersionApiView.as_view(), name='page-update'),
    path('page/<int:pk>/version/<int:version_id>/current/', PageSetCurrentVersionApiView.as_view(), name='page-set-current'),
]