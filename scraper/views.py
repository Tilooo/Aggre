from django.shortcuts import render
from .models import Job


def job_list(request):
    jobs = Job.objects.all().order_by('-created_at') # all jobs, newest first

    # the context is a dictionary that passes data to the template
    context = {
        'jobs': jobs
    }

    return render(request, 'scraper/job_list.html', context)