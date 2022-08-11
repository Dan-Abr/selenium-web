# third-party
from rest_framework import generics
from rest_framework import mixins

# local Django
from .models import *
from .serializers import *
from .permissions import IsUser


class E2ETestParamsList(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        generics.GenericAPIView):
    """ List all existing end-to-end tests, which belong to the user.
    """
    queryset = E2ETestParamsModel.objects.all()
    serializer_class = E2ETestParamsSerializer
    # Only logged-in users can access this API endpoint.
    permission_classes = [IsUser]

    # Filter for end-to-end tests which belong to the logged-in user
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)