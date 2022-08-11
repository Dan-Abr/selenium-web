# third-party
from rest_framework import generics
from rest_framework import mixins

# local Django
from .models import *
from .serializers import *
from .permissions import IsUser


class E2ETestParamsList(mixins.ListModelMixin, 
                        generics.GenericAPIView):
    """ List all existing end-to-end tests, which belong to the user.
    """
    queryset = E2ETestParamsModel.objects.all()
    serializer_class = E2ETestParamsSerializer
    # Only logged-in users can access this API endpoint.
    # Users can only access their own end-to-end tests.
    permission_classes = [IsUser]

    def get_queryset(self):
        # Filter for end-to-end tests which belong to the logged-in user
        return self.queryset.filter(user=self.request.user).order_by('-created')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class E2ETestParamsID(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    """ A specific end-to-end test, which belong to the user,
        based on the end-to-end ID.
        Allow to update, delete and retrieve the end-to-end test result.
    """
    queryset = E2ETestParamsModel.objects.all()
    serializer_class = E2ETestParamsSerializer
    # Only logged-in users can access this API endpoint.
    # Users can only access their own end-to-end tests.
    permission_classes = [IsUser]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class E2ETestResultsList(mixins.ListModelMixin,
                         generics.GenericAPIView):
    """ List all existing end-to-end test results, which belong to the user.
    """
    queryset = E2ETestResultsModel.objects.all()
    serializer_class = E2ETestResultsSerializer
    # Only logged-in users can access this API endpoint.
    # Users can only access their own end-to-end test results.
    permission_classes = [IsUser]

    def get_queryset(self):
        # Filter for end-to-end test results which belong to the logged-in user
        return self.queryset.filter(user=self.request.user).order_by('-created')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class E2ETestResultID(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    """ A specific end-to-end test result, which belong to the user,
        based on the end-to-end result ID.
        Allow to update, delete and retrieve the end-to-end test result.
    """
    queryset = E2ETestResultsModel.objects.all()
    serializer_class = E2ETestResultsSerializer
    # Only logged-in users can access this API endpoint.
    # Users can only access their own end-to-end test results.
    permission_classes = [IsUser]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)