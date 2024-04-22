from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Review, Ticket, UserFollows
from .forms import TicketReviewForm, TicketForm, DeleteTicketForm, FollowUsersForm
from authentication.models import User


class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class TicketView(LoginRequiredMixin, View):
    def post(self, request):
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

    def create_ticket(request):
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
        ticket = get_object_or_404(Ticket, id=ticket_id)
        edit_form = TicketForm(instance=ticket)
        delete_form = DeleteTicketForm()
        if request.method == 'POST':
            if 'edit_ticket' in request.POST:
                edit_form = TicketForm(request.POST, request.FILES, instance=ticket)
                if edit_form.is_valid():
                    edit_form.save()
                    return redirect('home_review')
            elif 'delete_ticket' in request.POST:
                delete_form = DeleteTicketForm(request.POST)
                if delete_form.is_valid():
                    ticket.delete()
                    return redirect('home_review')
        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
        }
        return render(request, 'ticket_update.html', context=context)


class FollowingView(LoginRequiredMixin, View):
    def get(self, request):
        followed_users = UserFollows.objects.filter(user=request.user)
        form = FollowUsersForm()
        context = {
            "form": form,
            "followed_users": followed_users
        }
        return render(request, "review/following.html", context=context)

    def post(self, request):
        form = FollowUsersForm(request.POST)
        followed_users = UserFollows.objects.filter(user=request.user)

        if form.is_valid():
            follows_username = form.cleaned_data['follows']
            try:
                followed_user = User.objects.get(username=follows_username)
                if followed_user != request.user:
                    UserFollows.objects.get_or_create(
                        user=request.user,
                        followed_user=followed_user
                    )
                    # Rediriger vers une autre vue ou effectuer une autre action après
                    # avoir suivi l'utilisateur avec succès
                    return redirect('following')
                else:
                    messages.error(
                        request, "Vous ne pouvez pas vous abonner à vous-même."
                    )
            except User.DoesNotExist:
                messages.error(
                    request, "L'utilisateur que vous souhaitez suivre n'existe pas."
                )

        # Si le formulaire n'est pas valide ou s'il y a une erreur, revenez à la page de suivi
        context = {
            "form": form,
            "followed_users": followed_users
        }
        return render(request, "review/following.html", context=context)


class HomeReviewView(CustomLoginRequiredMixin, View):
    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        return render(request, 'review/home_review.html', {'tickets': tickets})

    def posts_view(request):
        user = request.user
        following_users = UserFollows.objects.filter(user=user, blocked=False).values_list('followed_user', flat=True)
        following_tickets = Ticket.objects.filter(user__in=following_users)
        following_reviews = Review.objects.filter(ticket__user__in=following_users)
        return render(request, '/home_review.html', {'following_tickets': following_tickets,
                                                     'following_reviews': following_reviews})


class PostsView(LoginRequiredMixin, View):
    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)
        return render(request, 'review/posts.html', {'tickets': tickets, 'reviews': reviews})


class ReviewView(LoginRequiredMixin, View):
    def get(self, request):
        reviews = Review.objects.filter(user=request.user)
        return render(request, 'review/add_review.html', {'reviews': reviews})

    def post(self, request):
        if request.method == 'POST':
            headline = request.POST.get('headline')
            rating = request.POST.get('rating')
            body = request.POST.get('body')
            review = Review.objects.create(
                headline=headline,
                rating=rating,
                body=body,
                user=request.user
            )
            review.save()
            return redirect('home_review')
        else:
            return render(request, 'review/add_review.html')

    def create_ticket_review(request):
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
