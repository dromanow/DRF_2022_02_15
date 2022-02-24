from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, StringRelatedField
from .models import Author, Book, Bio


class AuthorModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookModelSerializer(ModelSerializer):
    authors = AuthorModelSerializer(many=True)
    # authors = StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = '__all__'


class BioModelSerializer(ModelSerializer):
    author = AuthorModelSerializer()

    class Meta:
        model = Bio
        fields = '__all__'
