from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm, DeleteTicketForm, ReviewForm, DeleteReviewForm
from django.contrib.auth.mixins import AccessMixin


class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Gérer les utilisateurs non authentifiés
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class HomeReviewView(CustomLoginRequiredMixin, View):
    def get(self, request):
        # Retrouvez tous les tickets en rapport avec l'utilisateur connecté pour les afficher sur home_review
        tickets = Ticket.objects.filter(user=request.user)
        return render(request, 'review/home_review.html', {'tickets': tickets})


class TicketView(LoginRequiredMixin, View):
    def get(self, request):
        # Récupérer tous les tickets de l'utilisateur connecté
        tickets = Ticket.objects.filter(user=request.user)
        return render(request, 'add_ticket.html', {'tickets': tickets})

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
def edit_delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    delete_form = DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home_review')
            if 'delete_ticket' in request.POST:
                delete_form = DeleteTicketForm(request.POST)
                if delete_form.is_valid():
                    ticket.delete()
                    return redirect('home_review')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, '/ticket_update.html', context=context)


class ReviewView(LoginRequiredMixin, View):
    def get(self, request):
        # Récupérer toutes les critiques de l'utilisateur connecté
        reviews = Review.objects.filter(user=request.user)
        return render(request, 'add_review.html', {'reviews': reviews})

    def post(self, request):
        if request.method == 'POST':
            # Récupérer les données du formulaire
            headline = request.POST.get('headline')
            rating = request.POST.get('rating')
            body = request.POST.get('body')

            # Créer une instance de Review avec les données du formulaire
            review = Review.objects.create(
                headline=headline,
                rating=rating,
                body=body,
                user=request.user
            )

            # Sauvegarder l'objet Review dans la base de données
            review.save()

            # Rediriger vers une page de succès ou toute autre page appropriée
            return redirect('home_review')
        else:
            # Afficher le formulaire vide
            return render(request, 'add_review.html')


@login_required
def edit_delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    edit_form = ReviewForm(instance=review)
    delete_form = DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home_review')
            if 'delete_review' in request.POST:
                delete_form = DeleteReviewForm(request.POST)
                if delete_form.is_valid():
                    review.delete()
                    return redirect('home_review')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, '/review_update.html', context=context)
