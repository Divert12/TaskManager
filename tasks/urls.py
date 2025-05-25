from django.urls import path
from . import views
from .forms import LoginForm

app_name = 'tasks'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('taches/', views.liste_taches, name='liste_taches'),
    path('taches/ajouter/', views.ajouter_tache, name='ajouter_tache'),
    path('taches/<int:tache_id>/modifier/', views.modifier_tache, name='modifier_tache'),
    path('taches/<int:tache_id>/supprimer/', views.supprimer_tache, name='supprimer_tache'),
    path('taches/<int:tache_id>/', views.detail_tache, name='detail_tache'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('profil/', views.profil, name='profil'),
    path('profil/<int:user_id>/', views.profil_utilisateur, name='profil_utilisateur'),
    path('equipe/', views.liste_equipes, name='liste_equipes'),
    path('equipe/creer/', views.creer_equipe, name='creer_equipe'),
    path('equipe/<int:equipe_id>/', views.det_eq, name='equipe_detail'),
    path('equipe/<int:equipe_id>/rejoindre/', views.rejoindre_equipe, name='rejoindre_equipe'),
    path('equipe/<int:equipe_id>/quitter/', views.quitter_equipe, name='quitter_equipe'),
]

