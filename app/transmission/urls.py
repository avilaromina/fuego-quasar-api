from django.urls import path

from transmission import views

app_name = 'transmission'

urlpatterns = [
    path('topsecret/', views.TopSecretView.as_view(), name="topsecret"),
    path('topsecret_split/<name>', views.TopSecretSplitView.as_view(), name="topsecret_split"),
]
