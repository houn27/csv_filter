from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.listRecord),
    path('detail/',views.fileDetail),
    path('upload/',views.upload),
    path('delete/',views.delFile)
]