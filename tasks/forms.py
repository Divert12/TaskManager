from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import tache,equipe,Utilisateur

# formulaire pour la creation//modification des taches
class TacheForm(forms.ModelForm):
    class Meta:
        model = tache
        fields = ['titre', 'description', 'statut','personne_assignee', 'equipes_assignees', 'sous_tache', 'est_prive']

# formulaire dinscription avec validation demail unique
class InscriptionForm(UserCreationForm):
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    equipe = forms.ModelChoiceField(
        queryset=equipe.objects.all(),
        required=False,
        label="Équipe",
        empty_label="Aucune équipe",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    class Meta:
        model = Utilisateur
        fields = ['email', 'username', 'password1', 'password2', 'description', 'equipe']

    def clean_email(self):
        # verifie que lemail n'est pas deja utilise
        email = self.cleaned_data.get('email')
        if Utilisateur.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

# formulaire de profil utilisateur (modification)
class ProfilForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['email', 'username','description', 'equipe']

# formulaire de gestion des equipes avec gestion des membres
class EquipeForm(forms.ModelForm):
    membres = forms.ModelMultipleChoiceField(
        queryset=Utilisateur.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Membres de l'équipe"
    )

    class Meta:
        model = equipe
        fields = ['nom'] 

    def __init__(self, *args, **kwargs):
        # charge les membres existants pour la modification
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['membres'].initial = self.instance.membres.all()

    def save(self, commit=True):
        # sauvegarde l'equipe et met à jour ses membres
        equipe = super().save(commit=False)
        if commit:
            equipe.save()
        if 'membres' in self.cleaned_data:
            self.cleaned_data['membres'].update(equipe=equipe)
        return equipe

# formulaire de connexion personnalise
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Adresse e-mail",
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

