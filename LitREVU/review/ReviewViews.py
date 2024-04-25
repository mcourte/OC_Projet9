from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Review, Ticket, UserFollows
from .forms import TicketReviewForm, TicketForm, FollowUsersForm, ReviewForm
from authentication.models import User
from itertools import chain
from operator import attrgetter


class TicketView(LoginRequiredMixin, View):
    """Cette vue gère l'affichage des tickets, leur création, leur modification et leur suppression."""
    def get(self, request):
        """ Affiche les tickets des utilisateurs suivis."""
        # Récupérer les tickets des utilisateurs suivis
        following_tickets = Ticket.objects.filter(user__in=request.user.following.all())

        # Récupérer les critiques des utilisateurs suivis
        following_reviews = Review.objects.filter(ticket__user__in=request.user.following.all())

        # Combinez les tickets et les critiques dans une seule liste et triez-les par date de création
        combined_list = sorted(
            chain(following_tickets, following_reviews),
            key=attrgetter('time_created'),
            reverse=True
        )

        return render(request, 'ticket_review.html', {'combined_list': combined_list})

    def post(self, request):
        """Crée un nouveau ticket."""
        if request.method == 'POST':
            # Récupérer les données du formulaire
            description = request.POST.get('description')
            image = request.FILES.get('image')

            # Récupérer le nombre de tickets déjà créés par l'utilisateur
            user_ticket_count = Ticket.objects.filter(user=request.user).count()

            # Créer une instance de Ticket avec les données du formulaire
            ticket = Ticket.objects.create(
                title="Titre par défaut",
                description=description,
                user=request.user,
                image=image,
                user_ticket_number=user_ticket_count + 1  # Numéro de ticket incrémenté
            )
            # Sauvegarder l'objet Ticket dans la base de données
            ticket.save()

            # Rediriger vers une page de succès ou toute autre page appropriée
            return redirect('accounts:home_review')  # Mettez à jour ici
        else:
            # Afficher le formulaire vide
            return render(request, 'review/add_ticket.html')

    @classmethod
    def create_ticket(cls, request):
        """Méthode pour créer un nouveau ticket en utilisant un formulaire."""
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                return redirect('home_review')
        else:
            form = TicketForm()
        return render(request, 'review/create_ticket.html', {'form': form})

    def edit_delete_ticket(request, ticket_id):
        """Affiche le formulaire de confirmation de suppression d'un ticket."""
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if request.method == 'POST':
            # Vérifie si l'utilisateur a confirmé la suppression
            if 'confirm_delete' in request.POST:
                # Suppression du ticket
                ticket.delete()
                messages.success(request, "Le ticket a été supprimé avec succès.")
                return redirect('posts')  # Rediriger vers la page des posts après suppression
            else:
                messages.info(request, "La suppression du ticket a été annulée.")
                return redirect('posts')  # Rediriger vers la page des posts sans suppression

        context = {
            'ticket': ticket,
        }
        return render(request, 'review/edit_delete_ticket.html', context=context)

    def edit_ticket(request, ticket_id):
        """Affiche le formulaire de modification d'un ticket."""
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = TicketForm(instance=ticket)
        return render(request, 'review/edit_ticket.html', {'form': form, 'ticket': ticket})

    def update_ticket(request, ticket_id):
        """Met à jour les informations d'un ticket."""
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect('posts')
        else:
            form = TicketForm(instance=ticket)
        return render(request, 'review/edit_ticket.html', {'form': form, 'ticket': ticket})


class ReviewView(LoginRequiredMixin, View):
    """Cette vue gère l'affichage des critiques, leur création, leur modification et leur suppression."""
    def get(self, request):
        """Affiche les critiques de l'utilisateur actuel."""
        reviews = Review.objects.filter(user=request.user)
        return render(request, 'review/add_review.html', {'reviews': reviews})

    def post(self, request):
        """Crée une nouvelle critique."""
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                # Créer la critique
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('home_review')

    def create_ticket_review(request):
        """Crée à la fois un ticket et une critique associée."""
        if request.method == 'POST':
            form = TicketReviewForm(request.POST, request.FILES)
            if form.is_valid():
                # Créer le ticket
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()

                # Créer la critique associée au ticket
                review = Review.objects.create(
                    headline=form.cleaned_data['headline'],
                    rating=form.cleaned_data['rating'],
                    body=form.cleaned_data['body'],
                    user=request.user,
                    ticket=ticket
                )
                review.save()
                return redirect('home_review')
        else:
            form = TicketReviewForm()
        return render(request, 'review/create_ticket_review.html', {'form': form})

    def edit_delete_review(request, review_id):
        """Affiche le formulaire de confirmation de suppression d'une critique."""
        review = get_object_or_404(Review, id=review_id)

        if request.method == 'POST':
            # Vérifie si l'utilisateur a confirmé la suppression
            if 'confirm_delete' in request.POST:
                # Suppression de la critique
                review.delete()
                messages.success(request, "La critique a été supprimée avec succès.")
                return redirect('home_review')  # Rediriger vers la page des critiques après suppression
            else:
                messages.info(request, "La suppression de la critique a été annulée.")
                return redirect('home_review')  # Rediriger vers la page des critiques sans suppression

        context = {
            'review': review,
        }
        return render(request, 'review/edit_delete_review.html', context=context)


class FollowingView(LoginRequiredMixin, View):
    """Cette vue gère l'affichage et la gestion des utilisateurs suivis par l'utilisateur actuel."""
    def get(self, request):
        """Affiche les utilisateurs suivis par l'utilisateur actuel."""
        # Récupérer les utilisateurs que vous suivez
        followed_users = UserFollows.objects.filter(user=request.user)

        # Récupérer les utilisateurs qui vous suivent
        users_following = UserFollows.objects.filter(followed_user=request.user)

        form = FollowUsersForm()
        context = {
            "form": form,
            "followed_users": followed_users,
            "users_following_current_user": users_following
        }
        return render(request, "review/following.html", context=context)

    def post(self, request):
        """ Traite le formulaire pour suivre de nouveaux utilisateurs."""
        form = FollowUsersForm(request.POST)
        followed_users = UserFollows.objects.filter(user=request.user)

        if form.is_valid():
            follows_username = form.cleaned_data['follows']
            try:
                followed_user = User.objects.get(username=follows_username)
                if followed_user != request.user:
                    # Enregistrer la relation de suivi dans un seul sens
                    UserFollows.objects.get_or_create(user=request.user, followed_user=followed_user)
                    return redirect('following')
                else:
                    messages.error(request, "Vous ne pouvez pas vous abonner à vous-même.")
            except User.DoesNotExist:
                messages.error(request, "L'utilisateur que vous souhaitez suivre n'existe pas.")

        context = {
            "form": form,
            "followed_users": followed_users
        }
        return render(request, "review/following.html", context=context)


class UnfollowUserView(View):
    """ Cette vue gère la suppression du suivi d'un utilisateur par l'utilisateur actuel."""
    def post(self, request):
        """ Traite la demande de ne plus suivre un utilisateur. """
        followed_user_id = request.POST.get('followed_user_id')
        if followed_user_id:
            follow = UserFollows.objects.get(id=followed_user_id)
            follow.unfollow()
        return redirect("following")


class HomeReviewView(View):
    """ Cette vue gère l'affichage de la page d'accueil des critiques et des tickets."""
    def get(self, request):
        """ Affiche les critiques et les tickets associés aux utilisateurs suivis."""
        # Récupérer les utilisateurs suivis par l'utilisateur actuel
        following_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

        # Récupérer les tickets et les critiques associés aux utilisateurs suivis
        following_tickets = Ticket.objects.filter(user__in=following_users)
        following_reviews = Review.objects.filter(ticket__user__in=following_users)

        return render(request, 'review/home_review.html', {'following_tickets': following_tickets,
                                                           'following_reviews': following_reviews})

    def posts_view(self, request):
        """ Affiche les critiques et les tickets associés aux utilisateurs suivis (vue alternative)."""
        user = request.user
        following_users = UserFollows.objects.filter(user=user, blocked=False).values_list('followed_user', flat=True)
        following_tickets = Ticket.objects.filter(user__in=following_users)
        following_reviews = Review.objects.filter(ticket__user__in=following_users)
        return render(request, 'home_review.html', {'following_tickets': following_tickets,
                                                    'following_reviews': following_reviews})


class PostsView(LoginRequiredMixin, View):
    """ Cette vue gère l'affichage des tickets et des critiques de l'utilisateur actuel."""
    def get(self, request):
        """ Affiche les tickets et les critiques de l'utilisateur actuel."""
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)
        return render(request, 'review/posts.html', {'tickets': tickets, 'reviews': reviews})
