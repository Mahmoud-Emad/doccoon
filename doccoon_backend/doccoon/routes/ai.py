from django.urls import path

from doccoon.views.ai import AIDemoApiView, AIRefineApiView
from doccoon.views.ai_key import (
    AIProviderKeyDetailApiView,
    AIProviderKeyListCreateApiView,
)

urlpatterns = [
    path("refine/", AIRefineApiView.as_view()),
    path("demo/", AIDemoApiView.as_view()),
    path("keys/", AIProviderKeyListCreateApiView.as_view()),
    path("keys/<int:key_id>/", AIProviderKeyDetailApiView.as_view()),
]
