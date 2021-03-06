"""fornax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from sip_assembly.views import (CleanupRequestView, CleanupRoutineView,
                                CreatePackageView, RemoveCompletedIngestsView,
                                RemoveCompletedTransfersView, SIPAssemblyView,
                                SIPViewSet)

router = routers.DefaultRouter()
router.register(r'sips', SIPViewSet)
schema_view = get_schema_view(
    title="Fornax API",
    description="Endpoints for Fornax microservice application."
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^assemble/', SIPAssemblyView.as_view(), name="assemble-sip"),
    url(r'^start/', CreatePackageView.as_view(), name="create-transfer"),
    url(r'^remove-transfers/',
        RemoveCompletedTransfersView.as_view(),
        name="remove-transfers"),
    url(r'^remove-ingests/',
        RemoveCompletedIngestsView.as_view(),
        name="remove-ingests"),
    url(r'^cleanup/', CleanupRoutineView.as_view(), name="cleanup"),
    url(r'^request-cleanup/',
        CleanupRequestView.as_view(),
        name="request-cleanup"),
    url(r'^status/', include('health_check.api.urls')),
    url(r'^schema/', schema_view, name='schema'),
]
