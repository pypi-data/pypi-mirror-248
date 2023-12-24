from rest_framework.response import Response

from kfsd.apps.endpoints.views.common.model import ModelViewSet
from kfsd.apps.core.auth.token import TokenUser


class PermModelViewSet(ModelViewSet):
    lookup_field = "identifier"
    lookup_value_regex = "[^/]+"

    def getModelName(self):
        return self.queryset.model._meta.verbose_name

    def isPermEnabled(self, request):
        if (
            self.request.token_user.isAuthEnabled()
            and self.request.token_user.isAuthenticated()
        ):
            return True
        return False

    def getUser(self, request) -> TokenUser:
        return self.request.token_user

    def get_queryset(self):
        if self.isPermEnabled(self.request):
            user = self.getUser(self.request)
            resp = user.has_perm_all_resources("can_view", self.getModelName())
            print("Resp: {}".format(resp))
        else:
            print("Permission not enabled")

        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
