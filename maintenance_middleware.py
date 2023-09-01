from django.shortcuts import redirect
from django.urls import reverse


is_maintenance_mode = True

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != reverse('maintenance_page'):
            # check maintenance status, and if True, redirect to maintenance
            if is_maintenance_mode:
                return redirect(reverse('maintenance_mode'))
        return self.get_response(request)