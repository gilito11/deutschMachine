import json
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .models import SRSCard, ReviewLog
from .engine import sm2
from stats.models import DailyActivity
from vocabulary.models import VocabularyItem, Topic


@login_required
def review_session_view(request):
    lang_code = request.GET.get('lang', '')
    cards = SRSCard.objects.filter(
        user=request.user,
        next_review_date__lte=date.today()
    ).select_related('vocabulary_item', 'vocabulary_item__topic', 'vocabulary_item__language')

    if lang_code:
        cards = cards.filter(vocabulary_item__language__code=lang_code)

    cards = cards.order_by('next_review_date')[:20]

    if not cards.exists():
        return render(request, 'srs/no_cards.html', {'lang_code': lang_code})

    first_card = cards.first()
    return render(request, 'srs/review_session.html', {
        'card': first_card,
        'total_cards': cards.count(),
        'current_index': 1,
        'lang_code': lang_code,
    })


@login_required
def card_front_partial(request, card_id):
    card = get_object_or_404(SRSCard, id=card_id, user=request.user)
    return render(request, 'srs/partials/card_front.html', {'card': card})


@login_required
def card_back_partial(request, card_id):
    card = get_object_or_404(SRSCard, id=card_id, user=request.user)
    return render(request, 'srs/partials/card_back.html', {'card': card})


@login_required
@require_POST
def rate_card_view(request, card_id):
    card = get_object_or_404(SRSCard, id=card_id, user=request.user)
    quality = int(request.POST.get('quality', 3))
    response_time = request.POST.get('response_time')

    result = sm2(quality, card.repetitions, card.easiness_factor, card.interval_days)

    card.easiness_factor = result.easiness_factor
    card.interval_days = result.interval_days
    card.repetitions = result.repetitions
    card.next_review_date = result.next_review_date
    card.last_review_date = date.today()
    card.last_quality = quality
    card.total_reviews += 1
    if quality >= 3:
        card.correct_count += 1
    card.save()

    ReviewLog.objects.create(
        srs_card=card,
        quality=quality,
        response_time_ms=int(response_time) if response_time else None,
    )

    # Update daily activity
    activity, _ = DailyActivity.objects.get_or_create(
        user=request.user, activity_date=date.today()
    )
    activity.cards_reviewed += 1
    activity.xp_earned += quality * 2
    activity.save()

    # Update streak
    _update_streak(request.user)

    # Get next due card
    lang_code = request.POST.get('lang_code', '')
    next_cards = SRSCard.objects.filter(
        user=request.user,
        next_review_date__lte=date.today()
    ).exclude(id=card_id).select_related('vocabulary_item', 'vocabulary_item__topic')

    if lang_code:
        next_cards = next_cards.filter(vocabulary_item__language__code=lang_code)

    next_card = next_cards.order_by('next_review_date').first()

    if next_card:
        return render(request, 'srs/partials/card_front.html', {'card': next_card})
    else:
        today_activity = DailyActivity.objects.get(user=request.user, activity_date=date.today())
        from core.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return render(request, 'srs/partials/session_complete.html', {
            'activity': today_activity,
            'streak': profile.current_streak,
        })


@login_required
@require_POST
def add_topic_cards_view(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    items = topic.vocabulary_items.all()
    created = 0
    for item in items:
        _, was_created = SRSCard.objects.get_or_create(
            user=request.user,
            vocabulary_item=item,
            defaults={'next_review_date': date.today()}
        )
        if was_created:
            created += 1

    return HttpResponse(
        f'<span class="text-green-600 font-medium">{created} cards added!</span>',
        content_type='text/html',
    )


@login_required
def review_stats_view(request):
    cards = SRSCard.objects.filter(user=request.user)
    total = cards.count()
    due = cards.filter(next_review_date__lte=date.today()).count()
    learned = cards.filter(repetitions__gte=3).count()
    learning = cards.filter(repetitions__gt=0, repetitions__lt=3).count()
    new = cards.filter(repetitions=0).count()

    recent_logs = ReviewLog.objects.filter(
        srs_card__user=request.user
    ).select_related('srs_card__vocabulary_item').order_by('-reviewed_at')[:20]

    return render(request, 'srs/stats.html', {
        'total': total,
        'due': due,
        'learned': learned,
        'learning': learning,
        'new': new,
        'recent_logs': recent_logs,
    })


def _update_streak(user):
    from core.models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    today = date.today()

    if profile.last_activity_date == today:
        return

    from datetime import timedelta
    yesterday = today - timedelta(days=1)

    if profile.last_activity_date == yesterday:
        profile.current_streak += 1
    elif profile.last_activity_date != today:
        profile.current_streak = 1

    profile.last_activity_date = today
    if profile.current_streak > profile.longest_streak:
        profile.longest_streak = profile.current_streak
    profile.save()
