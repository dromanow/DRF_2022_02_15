from rest_framework.viewsets import ModelViewSet
from .serializers import AuthorModelSerializer
from .models import Author


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorModelSerializer
    queryset = Author.objects.all()
