# django
from django.http import Http404

# django extensions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

# local
from healthier.user.models import HealthierUser
from healthier.consumers.models import Consumer
from healthier.providers.models import Provider
from .serializers import UserSerializer, ConsumerSerializer, ProviderSerializer
from healthier.service.models import BaseHealthierService


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)


class AbstractDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def get_object(self, id):
        self.ID = {self.ID_NAME: id}
        print(self.ID)
        try:
            return self.MODEL.objects.get(**self.ID)
        except self.MODEL.DoesNotExist:
            raise Http404

    def get_all(self):
        return self.MODEL.objects.all()

    def get(self, request, format=None):
        id = request.query_params.get(self.ID_NAME, None)
        if id:
            matching_object = self.get_object(id)
            serializer = self.SERIALIZER(matching_object)
            return Response(serializer.data)
        else:
            matching_objects = self.get_all()
            serializer = self.SERIALIZER(matching_objects, many=True)
            return Response(serializer.data)

    def put(self, request, format=None):
        id = request.data.get(self.ID_NAME, None)
        try:
            matching_object = self.get_object(id)
        except self.MODEL.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.SERIALIZER(matching_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        id = request.data.get(self.ID_NAME, None)
        matching_object = self.get_object(id)
        matching_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsumerDetail(AbstractDetail):
    def __init__(self):
        self.MODEL = Consumer
        self.SERIALIZER = ConsumerSerializer
        self.ID_NAME = 'healthier_id'
        self.ID_VALUE = None
        AbstractDetail.__init__(self)


class ProviderDetail(AbstractDetail):
    def __init__(self):
        self.MODEL = Provider
        self.SERIALIZER = ProviderSerializer
        self.ID_NAME = 'healthier_id'
        self.ID_VALUE = None
        AbstractDetail.__init__(self)


class UserDetail(AbstractDetail):
    """
    This endpoint presents user details.
    Supported methods: GET, PUT
    **GET**:
            - If user email is passed as argument, details of the particular user is returned.
            - If no user email is passed, returns details of all users in the database.
    **PUT**:
            - If no user email is specified or specified email doesn't exist, error 404 is raised

    """

    def __init__(self):
        self.MODEL = HealthierUser
        self.SERIALIZER = UserSerializer
        self.ID_NAME = 'email'
        self.ID_VALUE = None
        AbstractDetail.__init__(self)