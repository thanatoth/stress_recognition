from rest_framework import routers
from django.urls import path
from .views import PredictedViewSet
from . import views

#http://{ip}/api/predictでアクセス
router = routers.DefaultRouter()
router.register(r'^result', PredictedViewSet)

urlpatterns = [
    path('upload', views.upload, name='upload'),
]
