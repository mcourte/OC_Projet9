from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Review, Ticket, UserFollows, TicketReview
from .forms import TicketForm, FollowUsersForm, ReviewForm, TicketReviewForm
from django.urls import reverse_lazy
from authentication.models import User
from operator import attrgetter
from itertools import chain


class HomeReviewView(LoginRequiredMixin, View):
    def get(self, request):
        """Affiche les utilisateurs suivis par l'utilisateur actuel."""
        # Récupérer les utilisateurs que vous suivez
        followed_users = UserFollows.objects.filter(user=request.user)

        # Récupérer les ID des utilisateurs suivis
        followed_user_ids = followed_users.values_list('followed_user', flat=True)

        # Récupérer les tickets des utilisateurs suivis
        following_tickets = Ticket.objects.filter(user__in=followed_user_ids)

        # Récupérer les critiques associées à ces tickets
        following_reviews = Review.objects.filter(ticket__in=following_tickets)

        # Trier les tickets et les critiques par date de création de la plus récente à la plus ancienne
        following_tickets = following_tickets.order_by('-time_created')
        following_reviews = following_reviews.order_by('-time_created')

        # Ajouter une propriété 'type' à chaque élément pour distinguer les tickets des critiques
        for ticket in following_tickets:
            ticket.type = 'ticket'
            ticket.user_has_review = ticket.user_has_review(request.user)
        for review in following_reviews:
            review.type = 'review'
            review.user_has_review = True  # Vous pouvez ajuster cela si nécessaire

        # Combiner les tickets et les critiques dans une liste
        combined_list = sorted(
            chain(following_tickets, following_reviews),
            key=lambda x: x.time_created if isinstance(x, Review) else x.time_created,
            reverse=True
        )
        context = {
            'combined_list': combined_list
        }
        return render(request, 'review/home_review.html', context=context)


class PostsView(LoginRequiredMixin, View):
    """Cette vue gère l'affichage des tickets et des critiques de l'utilisateur actuel."""
    def get(self, request):
        """Affiche les tickets et les critiques de l'utilisateur actuel."""
        # Tri des tickets par date de création décroissante
        tickets = Ticket.objects.filter(user=request.user).order_by('-time_created')
        # Tri des critiques par date de création décroissante
        reviews = Review.objects.filter(user=request.user).order_by('-time_created')
        context = {
            'tickets': tickets,
            'reviews': reviews
        }
        return render(request, 'review/posts.html', context=context)


class TicketView(LoginRequiredMixin, View):
    """Cette vue gère l'affichage des tickets, leur création, leur modification et leur suppression."""
    def get(self, request):
        """Affiche les tickets de l'utilisateur et leur état."""
        # Récupérer les utilisateurs que vous suivez
        user = request.user
        following_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)

        # Récupérer les tickets des utilisateurs suivis
        following_tickets = Ticket.objects.filter(user__in=following_users)

        # Récupérer les critiques des utilisateurs suivis
        following_reviews = Review.objects.filter(ticket__user__in=following_users)

        # Combiner les tickets et les critiques dans une liste
        combined_list = list(chain(following_tickets, following_reviews))

        for ticket in combined_list:
            # Vérifie si le ticket a une critique
            ticket.has_review = ticket.reviews.exists()
            # Vérifie si l'utilisateur a posté une critique pour ce ticket
            ticket.user_has_review = ticket.reviews.filter(user=user).exists()

        combined_list = sorted(combined_list, key=attrgetter('time_created'), reverse=True)
        context = {
            'combined_list': combined_list
        }

        return render(request, 'ticket_review.html', context=context)

    def post(self, request):
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
        context = {
            'form': form,
        }
        return render(request, 'review/create_ticket.html', context=context)

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
                return redirect('edit_delete_ticket', ticket_id=ticket_id)  # Rediriger vers la page de confirmation

        context = {
            'ticket': ticket,
        }
        return render(request, 'review/edit_delete_ticket.html', context=context)

    def edit_ticket(request, ticket_id):
        """Affiche le formulaire de modification d'un ticket."""
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = TicketForm(instance=ticket)
        context = {
            'form': form,
            'ticket': ticket,
        }
        return render(request, 'review/edit_ticket.html', context=context)

    def update_ticket(request, ticket_id):
        """Met à jour les informations d'un ticket."""
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect('home_review')
        else:
            form = TicketForm(instance=ticket)

        context = {
            'form': form,
            'ticket': ticket,
        }

        return render(request, 'review/edit_ticket.html', context=context)


class ReviewView(LoginRequiredMixin, View):
    """Cette vue gère l'affichage des critiques, leur création, leur modification et leur suppression."""
    def get(self, request, ticket_id):
        """Affiche le formulaire pour créer une critique en réponse à un ticket."""
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = ReviewForm()
        # Vérifie si l'utilisateur à déjà créer une critique sur un ticket
        user_already_reviewed = Review.objects.filter(user=request.user, ticket=ticket).exists()
        context = {
            'form': form,
            'ticket': ticket,
            'user_already_reviewed': user_already_reviewed
        }

        return render(request, 'review/create_review.html', context=context)

    def post(self, request, ticket_id):
        """Crée une critique en réponse à un ticket."""
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                # Vérifie si l'utilisateur à déjà créer une critique sur un ticket
                if not Review.objects.filter(user=request.user, ticket=ticket).exists():
                    review = form.save(commit=False)
                    review.user = request.user
                    review.ticket = ticket
                    review.save()
                    return redirect('posts')
                else:
                    messages.error(request, "Vous avez déjà poster une critique en réponse à ce ticket.")
        else:
            form = ReviewForm()
        return render(request, 'review/create_review.html', {'form': form, 'ticket': ticket})

    def edit_delete_review(request, review_id):
        """Affiche le formulaire de confirmation de suppression d'un ticket."""
        review = get_object_or_404(Review, id=review_id)

        if request.method == 'POST':
            # Vérifie si l'utilisateur a confirmé la suppression
            if 'confirm_delete' in request.POST:
                # Suppression du ticket
                review.delete()
                messages.success(request, "La critique a été supprimé avec succès.")
                return redirect('posts')  # Rediriger vers la page des posts après suppression
            else:
                return redirect('edit_delete_review', review_id=review_id)  # Rediriger vers la page de confirmation

        context = {
            'review': review,
        }
        return render(request, 'review/edit_delete_review.html', context=context)

    def update_review(request, review_id):
        """Met à jour les informations d'une critique."""
        review = get_object_or_404(Review, id=review_id)
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                form.save()
                return redirect('home_review')
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form,
            'review': review
        }
        return render(request, 'review/edit_review.html', context=context)


class TicketReviewView(View):
    """Cette vue gère la publication, la modification et la suppression d'un ticket et d'une critique associée."""

    def get(self, request):
        """Affiche le formulaire pour publier un ticket et une critique associée."""
        ticket_review_form = TicketReviewForm()
        context = {
            'ticket_review_form': ticket_review_form
        }
        return render(request, 'review/create_ticket_review.html', context=context)

    def post(self, request):
        """Traite le formulaire soumis pour publier un ticket et une critique associée."""
        ticket_review_form = TicketReviewForm(request.POST, request.FILES)
        if ticket_review_form.is_valid():
            ticket = Ticket.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                image=request.FILES.get('image'),
                user=request.user
            )
            review = Review.objects.create(
                rating=request.POST['rating'],
                headline=request.POST['headline'],
                body=request.POST['body'],
                user=request.user,
                ticket=ticket
            )
            TicketReview.objects.create(ticket=ticket, review=review)
            return redirect(reverse_lazy('posts'))
        else:
            # If the form is not valid, return the form with errors
            context = {
                'ticket_review_form': ticket_review_form
            }
            return render(request, 'review/create_ticket_review.html', context=context)

    def delete_review(request, review_id):
        """Supprime une critique."""
        review = get_object_or_404(Review, id=review_id)
        if request.method == 'POST':
            # Vérifie si l'utilisateur a confirmé la suppression
            if 'confirm_delete' in request.POST:
                # Suppression du ticket
                review.delete()
                messages.success(request, "La critique a été supprimé avec succès.")
                return redirect('posts')  # Rediriger vers la page des posts après suppression
            else:
                return redirect('edit_delete_review', review_id=review_id)  # Rediriger vers la page de confirmation

        context = {
            'review': review,
        }
        return render(request, 'review/edit_delete_review.html', context=context)

    def update_review(request, review_id):
        """Met à jour les informations d'une critique."""
        review = get_object_or_404(Review, id=review_id)
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                form.save()
                return redirect('posts')
        else:
            form = ReviewForm(instance=review)

        context = {
            'form': form,
            'review': review
        }
        return render(request, 'review/edit_review.html', context=context)

    def delete_ticket(request, ticket_id):
        """Supprime un ticket et les critiques associées."""
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if request.method == 'POST':
            ticket.delete()
            messages.success(request, "Le ticket et ses critiques associées ont été supprimés avec succès.")
            return redirect('posts')
        context = {
            'ticket': ticket
        }
        return render(request, 'review/edit_delete_ticket.html', context=context)


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
            "users_following": users_following,
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
