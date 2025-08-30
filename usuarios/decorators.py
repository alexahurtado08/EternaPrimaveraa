# by mariana valderrama
from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    """
    Solo permite acceso a usuarios staff o superusuarios.
    """
    return user_passes_test(lambda u: u.is_staff or u.is_superuser)(view_func)
