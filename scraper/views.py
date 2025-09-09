# scraper/views.py

from django.shortcuts import render
from .models import Job
from django.db.models import Q
from django.core.paginator import Paginator


def job_list(request):
    search_query = request.GET.get('q', '')

    page_number = request.GET.get('page', 1)

    jobs_list = Job.objects.all().order_by('-created_at')

    if search_query:
        jobs_list = jobs_list.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query)
        )

    # Pagination Logic
    paginator = Paginator(jobs_list, 15)

    page_obj = paginator.get_page(page_number)


    context = {
        'jobs_page': page_obj,
        'search_query': search_query,
    }

    return render(request, 'scraper/job_list.html', context)