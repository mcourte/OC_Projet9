from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def add_review(request):
    return render(request, 'review/add_review.html')


@csrf_protect
def delete_review(request):
    return render(request, 'review/delete_review.html')


class TicketView(View):
    def get(self, request):
        return render(request, 'review/ticket.html')
