from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

# Graphene/GraphQL is optional. Import only if available to avoid
# hard-failing when the package is not installed in the environment.
try:
    from graphene_django.views import GraphQLView
    from .schema import schema
    _graphql_available = True
except Exception:
    _graphql_available = False

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('hospital/<int:pk>/', views.hospital_detail, name='hospital_detail'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]

if _graphql_available:
    urlpatterns.append(path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)))