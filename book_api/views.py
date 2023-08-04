from django.db.models import QuerySet, Q
from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from .models import BooksBook
from .serializers import *


@extend_schema(
    parameters=[
        OpenApiParameter(name='page', description='The page that needs to be loaded',
                         required=False, type=int),
        OpenApiParameter(name='gutenbergid', description='GutenBerg ID',
                         required=False, type=int),
        OpenApiParameter(name='language', description='Language Code',
                         required=False, type=str),
        OpenApiParameter(name='mimetype', description='Mime Type',
                         required=False, type=str),
        OpenApiParameter(name='topic', description='Topic can be either Subject Name or BookShelf Name',
                         required=False, type=str),
        OpenApiParameter(name='author', description='Authors Name',
                         required=False, type=str),
    ],
    description='This API is used to retrieve Books meeting the respective criteria based on the filter'
)
class books_list(generics.ListAPIView):
    serializer_class = BookSerializer

    @extend_schema(request=None, responses=BookSerializer)
    def get_queryset(self) -> QuerySet:
        queryset = BooksBook.objects.all()
        gutenbergid = self.request.query_params.get('gutenbergid')
        title = self.request.query_params.get('title')
        languagecode = self.request.query_params.get('language')
        mimetype = self.request.query_params.get('mimetype')
        topic = self.request.query_params.get('topic')
        author = self.request.query_params.get('author')
        if gutenbergid is not None:
            queryset = queryset.filter(gutenberg_id=gutenbergid)
        if title is not None:
            queryset = queryset.filter(title=title)
        if languagecode is not None:
            queryset = queryset.filter(booksbooklanguages__language__code=languagecode)
        if mimetype is not None:
            queryset = queryset.filter(booksformat__mime_type=mimetype)
        if author is not None:
            queryset = queryset.filter(booksbookauthors__author__name=author)
        if topic is not None:
            queryset = queryset.filter(Q(booksbookbookshelves__bookshelf__name__icontains=topic) |
                                       Q(booksbooksubjects__subject__name__icontains=topic))
        return queryset
