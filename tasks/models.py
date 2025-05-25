from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# modele utilisateur personnalise 
class Utilisateur(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Relation avec l'équipe (un utilisateur = une équipe)
    equipe = models.ForeignKey('equipe', on_delete=models.SET_NULL,
    null=True, blank=True, related_name='membres')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',"first_name"]

    def __str__(self):
        return self.username

# modele principal pour la gestion des taches
class tache(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=20,choices=[('A Faire','A faire'),
    ('ACCOMPLIE','accomplie')],
    default='A Faire'
    )
    est_prive = models.BooleanField(default=False)
    creer_par=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='taches_crees')
    personne_assignee=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='taches_assignees',blank=True)
    equipes_assignees = models.ManyToManyField("equipe", related_name="taches", blank=True)
    sous_tache = models.ManyToManyField('self',symmetrical=False,blank=True,related_name='taches_parente')

    def __str__(self):
        return self.titre


class equipe(models.Model):
    nom = models.CharField(max_length=200)
    

    def __str__(self):
        return self.nom






    

    
    


# Create your models here.
