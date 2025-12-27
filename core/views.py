from .models import Customer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerForm
from .models import ServiceJob
from .forms import ServiceJobForm
from django.shortcuts import get_object_or_404
from django.db import models




@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by("-id")
    return render(request, "core/customer_list.html", {
        "customers": customers
    })

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "core/customer_list.html", {
        "customers": customers
    })

@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("customer_list")
    return render(request, "core/customer_form.html", {"form": form})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect("customer_list")
    return render(request, "core/customer_form.html", {"form": form})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("customer_list")
    return render(request, "core/customer_confirm_delete.html", {"customer": customer})

@login_required
def servicejob_list(request):
    jobs = ServiceJob.objects.select_related("customer").all()

    status = request.GET.get("status")
    query = request.GET.get("q")

    if status:
        jobs = jobs.filter(status=status)

    if query:
        jobs = jobs.filter(
            models.Q(customer__name__icontains=query) |
            models.Q(device__icontains=query)
        )

    jobs = jobs.order_by("-created_at")

    return render(request, "core/servicejob_list.html", {
        "jobs": jobs,
        "status": status,
        "query": query,
        "status_choices": ServiceJob.STATUS_CHOICES,
    })

import csv
from django.http import HttpResponse

@login_required
def export_servicejobs_csv(request):
    jobs = ServiceJob.objects.select_related("customer").all()

    status = request.GET.get("status")
    query = request.GET.get("q")

    if status:
        jobs = jobs.filter(status=status)

    if query:
        jobs = jobs.filter(
            models.Q(customer__name__icontains=query) |
            models.Q(device__icontains=query)
        )

    jobs = jobs.order_by("-created_at")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="service_jobs.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Customer",
        "Phone",
        "Device",
        "Problem",
        "Status",
        "Estimated Cost",
        "Created At",
    ])

    for job in jobs:
        writer.writerow([
            job.customer.name,
            job.customer.phone,
            job.device,
            job.problem,
            job.get_status_display(),
            job.estimated_cost,
            job.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    return response



@login_required
def servicejob_create(request):
    form = ServiceJobForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("servicejob_list")
    return render(request, "core/servicejob_form.html", {
        "form": form
    })

@login_required
def servicejob_update_status(request, pk):
    job = get_object_or_404(ServiceJob, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(ServiceJob.STATUS_CHOICES):
            job.status = new_status
            job.save()

    return redirect("servicejob_list")

@login_required
def servicejob_detail(request, pk):
    job = get_object_or_404(ServiceJob, pk=pk)
    return render(request, "core/servicejob_detail.html", {
        "job": job
    })

@login_required
def dashboard(request):
    total_jobs = ServiceJob.objects.count()
    pending_jobs = ServiceJob.objects.filter(status="pending").count()
    in_progress_jobs = ServiceJob.objects.filter(status="in_progress").count()
    completed_jobs = ServiceJob.objects.filter(status="completed").count()

    total_revenue = ServiceJob.objects.filter(
        status="completed"
    ).aggregate(total=models.Sum("estimated_cost"))["total"] or 0

    return render(request, "core/dashboard.html", {
        "total_jobs": total_jobs,
        "pending_jobs": pending_jobs,
        "in_progress_jobs": in_progress_jobs,
        "completed_jobs": completed_jobs,
        "total_revenue": total_revenue,
    })
