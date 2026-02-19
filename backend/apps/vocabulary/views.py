from django.db import models
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, VocabularyItem
from core.models import UserProfile


@login_required
def browse_view(request):
    user_langs = request.user.user_languages.select_related('language').filter(is_active=True)
    lang_code = request.GET.get('lang')
    category = request.GET.get('category')
    search = request.GET.get('q', '').strip()

    if not lang_code and user_langs.exists():
        lang_code = user_langs.first().language.code

    topics = Topic.objects.filter(
        language__code=lang_code, is_active=True
    ).select_related('language')

    if category:
        topics = topics.filter(category=category)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    country = profile.target_country
    topics = topics.filter(
        models.Q(country_context='') | models.Q(country_context=country)
    )

    items = None
    if search:
        items = VocabularyItem.objects.filter(
            language__code=lang_code
        ).filter(
            models.Q(word__icontains=search) | models.Q(translation_es__icontains=search)
        )[:50]

    return render(request, 'vocabulary/browse.html', {
        'topics': topics,
        'items': items,
        'user_langs': user_langs,
        'current_lang': lang_code,
        'current_category': category,
        'search': search,
    })


@login_required
def topic_detail_view(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    items = topic.vocabulary_items.all()

    from srs.models import SRSCard
    user_card_ids = set(
        SRSCard.objects.filter(user=request.user).values_list('vocabulary_item_id', flat=True)
    )

    return render(request, 'vocabulary/topic_detail.html', {
        'topic': topic,
        'items': items,
        'user_card_ids': user_card_ids,
    })
