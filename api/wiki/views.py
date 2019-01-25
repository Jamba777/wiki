from rest_framework.generics import (
    ListAPIView,
    GenericAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.response import Response

from .models import (
    PageModel,
    VersionModel,
)
from .serializers import (
    PageSerializer,
    PageVersionsSerializer,
    PageUpdateSerializer,
    PageSingleVersionsSerializer,
    PageSetCurrentVersionOutSerializer,
    VersionSerializer,
)


class CreatePageApiView(CreateAPIView):
    """
    Create wiki page method.
    """

    serializer_class = PageSerializer
    queryset = PageModel.objects.all()


class ListPageApiView(ListAPIView):
    """
    Return a list of all pages in system.
    """

    serializer_class = PageSerializer
    queryset = PageModel.objects.all()


class GetPageVersionsApiView(RetrieveAPIView):
    """
    Return all versions of given page in the system.
    """

    serializer_class = PageVersionsSerializer
    queryset = PageModel.objects.all()

    def get_queryset(self):
        qs = PageModel.objects.filter().prefetch_related('page_versions')
        return qs


class GetPageSingleVersionApiView(RetrieveAPIView):
    """
    Return page with given version number.
    """

    serializer_class = PageSingleVersionsSerializer
    queryset = PageModel.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['version_id'] = self.kwargs['version_id']
        return context


class UpdatePageApiView(UpdateAPIView):
    """
    Add new version of page.
    """

    serializer_class = PageUpdateSerializer
    queryset = PageModel.objects.all()


class PageSetCurrentVersionApiView(GenericAPIView):
    """
    Change current state for version.
    """

    serializer_class = VersionSerializer
    serializer_class_out = PageSetCurrentVersionOutSerializer
    queryset = PageModel.objects.all()

    def post(self, request, *args, **kwargs):
        version = get_object_or_404(VersionModel, id=kwargs['version_id'], page_id=kwargs['pk'])

        serializer = self.get_serializer(version)
        instance = serializer.set_current()

        out_data = self.serializer_class_out(instance.page).data

        return Response(out_data)


