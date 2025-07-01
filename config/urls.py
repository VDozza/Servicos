from app import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cadastrar-prestador/', views.cadastrar_prestador, name='cadastrar_prestador'),
    path('prestadores/', views.listar_prestadores, name='listar_prestadores'),
    path('solicitar-servico/', views.solicitar_servico, name='solicitar_servico'),
    path('agendar-servico/<int:solicitacao_id>/', views.agendar_servico, name='agendar_servico'),
    path('avaliar-servico/<int:solicitacao_id>/', views.avaliar_servico, name='avaliar_servico'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]