from django.views import View
# from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm
from django.contrib.auth.mixins import AccessMixin


class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Handle unauthenticated users
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class HomeReviewView(CustomLoginRequiredMixin, View):
    def get(self, request):
        # Retrouvez tous les tickets en rapport avec l'utilisateur connecté pour les afficher sur home_review
        tickets = Ticket.objects.filter(user=request.user)
        return render(request, 'home_review.html', {'tickets': tickets})


class TicketView(LoginRequiredMixin, View):
    def get(self, request):
        # Récupérer tous les tickets de l'utilisateur connecté
        tickets = Ticket.objects.filter(user=request.user)
        return render(request, 'ticket', {'tickets': tickets})

    def post(self, request):
        print(request)
        print(request.user)
        if request.method == 'POST':
            # Récupérer les données du formulaire
            description = request.POST.get('description')
            image = request.FILES.get('image')

            # Créer une instance de Ticket avec les données du formulaire
            ticket = Ticket.objects.create(
                title="Titre par défaut",
                description=description,
                user=request.user,
                image=image
            )
            # Sauvegarder l'objet Ticket dans la base de données
            ticket.save()

            # Rediriger vers une page de succès ou toute autre page appropriée
            return redirect('home_review')
        else:
            # Afficher le formulaire vide
            return render(request, 'home_review')


@login_required
def ticket_update_view(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if ticket.user != request.user:
        message = "Vous n'êtes pas autorisé à modifier cette critique."
        pass
    if request.method == 'POST':
        form = Ticket(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = Ticket(instance=ticket)
    return render(request, 'ticket_update.html', {'form': form, 'message': message})


@login_required
def ticket_delete_view(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if ticket.user != request.user:
        message = "Vous n'êtes pas autorisé à supprimer cette critique."
        pass
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')
    return render(request, 'ticket_confirm_delete.html', {'ticket': ticket, 'message': message})


@login_required
def ticket_create_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home_review')
    else:
        form = TicketForm()
    return render(request, 'ticket_ask.html', {'form': form})
