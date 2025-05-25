from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models
from itertools import chain
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate






def accueil(request):
    if request.user.is_authenticated:
        return redirect('tasks:liste_taches')
    return render(request, 'tasks/accueill.html')


@login_required
def liste_taches(request):
    taches_publiques = tache.objects.filter(est_prive=False)
    taches_privees = tache.objects.filter(
        est_prive=True
    ).filter(
        models.Q(creer_par=request.user) | 
        models.Q(personne_assignee=request.user) | 
        models.Q(equipes_assignees__membres=request.user)  
    ).distinct()

    taches = list(chain(taches_publiques, taches_privees))

    return render(request,'tasks/liste_taches.html',{'taches':taches})

@login_required
def ajouter_tache(request):
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.creer_par = request.user
            tache.save()
            return redirect('tasks:liste_taches')
    else:
        form = TacheForm()
    return render(request,'tasks/ajouter_tache.html',{'form':form})

@login_required
def modifier_tache(request,tache_id):
    tache_instance = get_object_or_404(tache, id=tache_id)
    if request.method == 'POST':
        form = TacheForm(request.POST or None, instance=tache_instance)
        if form.is_valid():
            form.save()
            return redirect('tasks:liste_taches')
    else:
        form = TacheForm(instance=tache_instance)
    return render(request,'tasks/modifier_tache.html',{'form':form})

@login_required
def supprimer_tache(request,tache_id):
    tache_instance = get_object_or_404(tache, id=tache_id)
    if request.method == 'POST':
        tache_instance.delete()
        return redirect('tasks:liste_taches')
    return render(request,'tasks/supprimer_tache.html',{'tache':tache_instance})

def detail_tache(request, tache_id):
    t = get_object_or_404(tache, id=tache_id)

    return render(request, 'tasks/detail_tache.html', {
        'tache': t
    })


@login_required
def creer_equipe(request):
    if request.method == 'POST':
        form = EquipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:liste_taches')
    else:
        form = EquipeForm()
    return render(request,'tasks/creer_equipe.html',{'form':form})

@login_required
def det_eq(request, equipe_id):
    equipe_obj = get_object_or_404(equipe, id=equipe_id)
    membres = equipe_obj.membres.all()
    taches = equipe_obj.taches.all()

    
    if request.method == "POST":
        utilisateur = request.user
        utilisateur.equipe = equipe_obj
        utilisateur.save()
        return redirect('tasks:equipe_detail', equipe_id=equipe_id)

    return render(request, 'tasks/detail_equipe.html', {
        'equipe': equipe_obj,
        'membres': membres,
        'taches': taches,
        'peut_rejoindre': request.user.equipe != equipe_obj,
    })

def liste_equipes(request):
    from django.urls import reverse
    print(reverse('tasks:equipe_detail', kwargs={'equipe_id': 1}))  # Test URL reversal
    equipes = equipe.objects.all()
    return render(request, 'tasks/liste_equipe.html', {'equipes': equipes})

@login_required
def rejoindre_equipe(request, equipe_id):
    equipe_obj = get_object_or_404(equipe, id=equipe_id)
    utilisateur = request.user
    utilisateur.equipe = equipe_obj
    utilisateur.save()
    return redirect('tasks:equipe_detail', equipe_id=equipe_id)

@login_required
def quitter_equipe(request, equipe_id):
    equipe_obj = get_object_or_404(equipe, id=equipe_id)
    utilisateur = request.user
    utilisateur.equipe = None
    utilisateur.save()
    return redirect('tasks:equipe_detail', equipe_id=equipe_id)



def signup(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        print("Form is valid?", form.is_valid())
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('tasks:profil')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = InscriptionForm()
    return render(request,'registration/signup.html',{'form':form})



def logout_view(request):
    logout(request)
    return redirect('tasks:accueil')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks:profil')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def profil(request):
    utilisateur = request.user
    
    # Statistiques des tâches
    total_taches = tache.objects.filter(
        models.Q(creer_par=utilisateur) | 
        models.Q(personne_assignee=utilisateur) | 
        models.Q(equipes_assignees__membres=utilisateur)
    ).distinct().count()
    
    taches_terminees = tache.objects.filter(
        models.Q(creer_par=utilisateur) | 
        models.Q(personne_assignee=utilisateur) | 
        models.Q(equipes_assignees__membres=utilisateur),
        statut='ACCOMPLIE'
    ).distinct().count()
    
    taches_en_cours = tache.objects.filter(
        models.Q(creer_par=utilisateur) | 
        models.Q(personne_assignee=utilisateur) | 
        models.Q(equipes_assignees__membres=utilisateur),
        statut='A Faire'
    ).distinct().count()
    
    
    nombre_equipes = equipe.objects.filter(
        models.Q(membres=utilisateur) | 
        models.Q(taches__personne_assignee=utilisateur)
    ).distinct().count()
    
    
    mes_equipes = equipe.objects.filter(membres=utilisateur)

    
    taches_privees = tache.objects.filter(
        est_prive=True
    ).filter(
        models.Q(creer_par=utilisateur) |
        models.Q(personne_assignee=utilisateur) |
        models.Q(equipes_assignees__membres=utilisateur)
    ).distinct().order_by('-id')
    
    context = {
        'utilisateur': utilisateur,
        'total_taches': total_taches,
        'taches_terminees': taches_terminees,
        'taches_en_cours': taches_en_cours,
        'nombre_equipes': nombre_equipes,
        'mes_equipes': mes_equipes,
        'taches_privees': taches_privees,
    }
    
    return render(request, 'tasks/profil.html', context)

@login_required
def profil_utilisateur(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    taches_publiques_assignees = tache.objects.filter(
        personne_assignee=utilisateur,
        est_prive=False
    ).distinct()
    return render(request, 'tasks/profil_utilisateur.html', {
        'utilisateur': utilisateur,
        'est_mon_profil': request.user == utilisateur,
        'taches_publiques_assignees': taches_publiques_assignees,
    })


