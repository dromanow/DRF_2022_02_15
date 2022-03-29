from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'library'

router = DefaultRouter()
router.register('authors', AuthorModelViewSet)
router.register('books', BookViewSet)
router.register('bios', BioViewSet)

urlpatterns = [
    path('', include(router.urls))
]
