"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path

urlpatterns = [
    #    path('admin/', admin.site.urls),
]


from django.urls import path, include
from data_management.views import get_table_data, save_table_data
from .views import dimensionality_reduction

urlpatterns = [
    path('api/', include('data_visualization.urls')),
    path('api/process/', include('data_processing.urls')),
    path("api/get_table_data/", get_table_data, name="get_table_data"),
    path("api/save_table_data/", save_table_data, name="save_table_data"),
    path('data/', include('data_management.urls')),
    path("api/dimensionality_reduction/", dimensionality_reduction, name="dimensionality_reduction"),
]
