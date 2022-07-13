from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.models import User
from users.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CurrentUserView(ViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        user = self.get_queryset()
        serializer = RegisterSerializer(user)
        serialized_data = serializer.data
        del serialized_data['password']
        serialized_data['username'] = user.username
        serialized_data['id'] = user.id
        return Response(data=serialized_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_queryset()
        serializer = RegisterSerializer(instance=user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            serialized_data['id'] = user.id
            serialized_data['username'] = user.username
            return Response(data=serialized_data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
