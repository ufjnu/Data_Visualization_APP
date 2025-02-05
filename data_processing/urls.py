from django.urls import path
from .views import DimensionalityReduction

urlpatterns = [
    path('reduce/', DimensionalityReduction.as_view(), name='dimensionality_reduction'),
]
