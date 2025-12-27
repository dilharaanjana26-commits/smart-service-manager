from django.urls import path
from . import views

urlpatterns = [
    # Customers
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/add/", views.customer_create, name="customer_create"),
    path("customers/<int:pk>/edit/", views.customer_update, name="customer_update"),
    path("customers/<int:pk>/delete/", views.customer_delete, name="customer_delete"),

    # Service Jobs
    path("jobs/", views.servicejob_list, name="servicejob_list"),
    path("jobs/add/", views.servicejob_create, name="servicejob_create"),
    path("jobs/<int:pk>/status/", views.servicejob_update_status, name="servicejob_update_status"),
    path("jobs/<int:pk>/", views.servicejob_detail, name="servicejob_detail"),
    path("", views.dashboard, name="dashboard"),
    path("jobs/export/", views.export_servicejobs_csv, name="export_servicejobs_csv"),

]
