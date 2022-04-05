"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from library.views import *
from graphene_django.views import GraphQLView
from django.views.generic import TemplateView

router = DefaultRouter()
router.register('authors', AuthorModelViewSet)
router.register('books', BookViewSet)
router.register('bios', BioViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Library',
        default_version='1.0',
        description='description',
        contact=openapi.Contact(email='test@mail.com'),
        license=openapi.License(name='MIT')
    ),
    public=True,
    permission_classes=(AllowAny, )
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # re_path(r'^api/(?P<version>\d\.\d)/authors/', AuthorModelViewSet.as_view({'get': 'list'})),
    # path('api/v1/', include('library.urls', namespace='1.0')),
    # path('api/v2/', include('library.urls', namespace='2.0.2')),
    # path('api/v3/', include('library.urls', namespace='2.1.2')),
    path('api-auth-token/', obtain_auth_token),
    path('swagger/', schema_view.with_ui()),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    re_path(r'^swagger(?P<format>\.json|\.yaml)', schema_view.without_ui()),
    path('', TemplateView.as_view(template_name='index.html')),

    # path('api_get/<str:first_name>/', AuthorViewSet.as_view({'get': 'list'})),
    # path('api_get/<int:pk>/', AuthorViewSet.as_view({'get': 'retrieve'})),
    # path('api_get/', get_view),
    # path('api_post/', post_view)
]
