def user_roles(request):
    if request.user.is_authenticated:
        return {
            'is_admin': request.user.role in ['admin', 'superadmin'],
            'is_student': request.user.role == 'student'
        }
    return {}