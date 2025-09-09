# scraper/views.py

from django.shortcuts import render
from .models import Job
from django.db.models import Q

def job_list(request):
    search_query = request.GET.get('q', '')

    # the newest first.
    jobs = Job.objects.all().order_by('-created_at')

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query)
        )

    context = {
        'jobs': jobs,
        'search_query': search_query,
    }

    return render(request, 'scraper/job_list.html', context)