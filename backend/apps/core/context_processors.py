from datetime import date


def global_context(request):
    ctx = {}
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        ctx['user_profile'] = profile

        from srs.models import SRSCard
        ctx['cards_due_count'] = SRSCard.objects.filter(
            user=request.user,
            next_review_date__lte=date.today()
        ).count()

        ctx['streak'] = profile.current_streak if profile else 0
    return ctx
