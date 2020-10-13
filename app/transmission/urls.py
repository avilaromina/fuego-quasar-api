from django.urls import include, path
from rest_framework.routers import DefaultRouter

from transmission import views

router = DefaultRouter()

app_name = 'transmission'

urlpatterns = [
    path('', include(router.urls)),
    path('topsecret/', views.TopSecretView.as_view(), name="topsecret"),
]
