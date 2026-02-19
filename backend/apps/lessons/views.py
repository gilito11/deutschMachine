from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def lessons_list_view(request):
    return render(request, 'lessons/list.html')
