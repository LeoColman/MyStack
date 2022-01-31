from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsProjectAdmin
from .serializers import MemberSerializer
from .exceptions import RoleAlreadyAssignedException, RoleConstraintException
from .models import Member


class MemberList(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def filter_queryset(self, queryset):
        queryset = queryset.filter(project=self.kwargs['project_id'])
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        try:
            serializer.save(project_id=self.kwargs['project_id'])
        except IntegrityError:
            raise RoleAlreadyAssignedException

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data['ids']
        project_id = self.kwargs['project_id']
        Member.objects.filter(project=project_id, pk__in=delete_ids)\
            .exclude(user=self.request.user)\
            .delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemberDetail(generics.RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_url_kwarg = 'member_id'
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def perform_update(self, serializer):
        project_id = self.kwargs['project_id']
        member_id = self.kwargs['member_id']
        role = serializer.validated_data['role']
        if not Member.objects.can_update(project_id, member_id, role.name):
            raise RoleConstraintException
        try:
            super().perform_update(serializer)
        except IntegrityError:
            raise RoleAlreadyAssignedException
