from django.shortcuts import render

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from authentication.models import Account
from pods.models import Pod
from pods.serializers import PodSerializer
from pods.permissions import IsHost, IsMember

class PodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pods to be viewed or edited.
    """
    lookup_field = 'name'
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Pod.objects.all()
    serializer_class = PodSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),)

        if self.request.method == 'POST':
            return (permissions.IsAuthenticated(),)

        if self.request.method == 'DELETE':
            return (permissions.IsAuthenticated(), IsHost())

        return (permissions.IsAuthenticated(), IsMember())


    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        account = Account.objects.get(username=serializer.validated_data['host'])

        if account.username != request.user.username:
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to create a pod hosted by user: {}.'.format(account.username)
            }, status=status.HTTP_403_FORBIDDEN)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
