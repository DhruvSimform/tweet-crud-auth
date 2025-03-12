from .models import Profile  # Import Profile model

def global_user_context(request):
    """Pass authenticated user and profile image globally to templates."""
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        profile_img = getattr(profile, 'profile_picture', None)  # Use correct field name
        
        return {
            'auth_user': request.user,  # Authenticated user object
            'profile_img': profile_img.url if profile_img else ""  # Profile image URL
        }
    return {}  # Return an empty dictionary if no user is logged in
