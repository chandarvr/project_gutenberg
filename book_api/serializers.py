from typing import Dict
from rest_framework import serializers
from .models import BooksBook, BooksAuthor, BooksLanguage, BooksSubject, BooksBookshelf, BooksFormat, \
    BooksBookLanguages, BooksBookAuthors, BooksBookSubjects, BooksBookBookshelves


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksAuthor
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksLanguage
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksSubject
        fields = ('name',)


class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookshelf
        fields = ('name',)


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksFormat
        fields = ['url']
        depth = 2


class BooksBookLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookLanguages
        fields = ['language']
        depth = 3


class BooksAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksAuthor
        fields = ['code']


class BooksBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBook
        fields = ['title']
        depth = 2


class BooksBookAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookAuthors
        fields = ['author']
        depth = 1


class BooksSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksSubject
        fields = '__all__'
        depth = 2


class BooksBookSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookSubjects
        fields = ['subject']
        depth = 2


class BooksBookBookshelvesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookBookshelves
        fields = ('bookShelf')


class BookSerializer(serializers.ModelSerializer):
    subjects_data = serializers.SerializerMethodField()
    download_links = serializers.SerializerMethodField()
    language_data = serializers.SerializerMethodField()
    authors_data = serializers.SerializerMethodField()

    class Meta:
        model = BooksBook
        fields = ('id', 'title', 'download_count', 'download_links', 'language_data', 'authors_data', 'download_count',
                  'subjects_data')
        depth = 1

    def get_subjects_data(self, obj) -> Dict[str, str]:
        formats = BooksBookSubjects.objects.filter(book=obj)
        serializer = BooksBookSubjectsSerializer(formats, many=True)
        return serializer.data

    def get_authors_data(self, obj) -> Dict[str, str]:
        formats = BooksBookAuthors.objects.filter(book=obj)
        serializer = BooksBookAuthorsSerializer(formats, many=True)
        return serializer.data

    def get_download_links(self, obj) -> Dict[str, str]:
        formats = BooksFormat.objects.filter(book=obj)
        serializer = FormatSerializer(formats, many=True)
        return serializer.data

    def get_language_data(self, obj) -> Dict[str, str]:
        formats = BooksBookLanguages.objects.filter(book=obj)
        serializer1 = BooksBookLanguagesSerializer(formats, many=True)
        return serializer1.data
