#from django.urls import path
#from .views import UploadCSV

#urlpatterns = [
  #  path('upload/', UploadCSV.as_view(), name='upload_csv'),
#]

from django.urls import path
from .views import generate_chart, export_chart

urlpatterns = [
    path("visualize/", generate_chart, name="generate_chart"),
    path("export_chart/", export_chart, name="export_chart"),
]

