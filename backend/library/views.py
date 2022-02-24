import io

from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer, CharField, IntegerField
from rest_framework.viewsets import ModelViewSet
from .serializers import AuthorModelSerializer, BookModelSerializer, BioModelSerializer
from .models import Author, Book, Bio


# client -> [url] -> [view] -> [serializer] -> [model]


class AuthorViewSet(ModelViewSet):
    # renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    serializer_class = AuthorModelSerializer
    queryset = Author.objects.all()


class BioViewSet(ModelViewSet):
    serializer_class = BioModelSerializer
    queryset = Bio.objects.all()


class BookViewSet(ModelViewSet):
    serializer_class = BookModelSerializer
    queryset = Book.objects.all()


class AuthorSerializer(Serializer):

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birthday_year = validated_data.get('birthday_year', instance.birthday_year)
        instance.save()
        return instance

    def create(self, validated_data):
        author = Author(**validated_data)
        author.save()
        return author

    def validate_birthday_year(self, value):
        if value < 1000:
            raise ValidationError('Must be gt 1000')
        return value

    def validate(self, attrs):
        if attrs['last_name'] == 'Достоеаский' and attrs['birthday_year'] != 1820:
            raise ValidationError('Must be 1820')
        return attrs

    first_name = CharField(max_length=64)
    last_name = CharField(max_length=64)
    birthday_year = IntegerField()


class BioSerializer(Serializer):
    text = CharField(max_length=64)
    author = AuthorSerializer()


class BookSerializer(Serializer):
    title = CharField(max_length=64)
    authors = AuthorSerializer(many=True)


def get_view(request):
    book = Book.objects.get(pk=1)
    serializer = BookSerializer(book)
    render = JSONRenderer()
    json_data = render.render(serializer.data)
    return HttpResponse(json_data)


    # author = Author.objects.get(pk=1)
    # return render_author(author)


@csrf_exempt
def post_view(request):
    data = JSONParser().parse(io.BytesIO(request.body))

    if request.method == 'POST':
        serializer = AuthorSerializer(data=data)
    elif request.method == 'PUT':
        author = Author.objects.get(pk=3)
        serializer = AuthorSerializer(author, data=data)
    elif request.method == 'PATCH':
        author = Author.objects.get(pk=3)
        serializer = AuthorSerializer(author, data=data, partial=True)

    if serializer.is_valid():
        print(serializer.validated_data)

        author = serializer.save()
        return render_author(author)
    else:
        return HttpResponseServerError(serializer.errors['non_field_errors'])


def render_author(author):
    serializer = AuthorSerializer(author)
    render = JSONRenderer()
    json_data = render.render(serializer.data)
    return HttpResponse(json_data)





