from django.urls import path
from .views  import CardLookupView

urlpatterns = [
    path("look/" , CardLookupView.as_view())
]
