import random
from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from vocabulary.models import VocabularyItem
from stats.models import DailyActivity
from .models import GenderDrillScore, CaseDrillScore
from .case_data import CASE_EXERCISES, CASE_COLORS


def _strip_article(word):
    for article in ('der ', 'die ', 'das '):
        if word.lower().startswith(article):
            return word[len(article):]
    return word


# Common German gender rules by suffix
_GENDER_RULES = {
    'der': [
        ('ling', 'Nouns ending in -ling are masculine'),
        ('ner', 'Nouns ending in -ner are masculine'),
        ('ler', 'Nouns ending in -ler are masculine'),
        ('er', 'Most nouns ending in -er (from verbs/agents) are masculine'),
        ('ismus', 'Nouns ending in -ismus are masculine'),
        ('ist', 'Nouns ending in -ist are masculine'),
        ('or', 'Nouns ending in -or are masculine'),
        ('ig', 'Nouns ending in -ig are masculine'),
        ('ich', 'Nouns ending in -ich are masculine'),
    ],
    'die': [
        ('ung', 'Nouns ending in -ung are always feminine'),
        ('heit', 'Nouns ending in -heit are always feminine'),
        ('keit', 'Nouns ending in -keit are always feminine'),
        ('schaft', 'Nouns ending in -schaft are always feminine'),
        ('taet', 'Nouns ending in -tät are always feminine'),
        ('tion', 'Nouns ending in -tion are always feminine'),
        ('ie', 'Nouns ending in -ie are feminine'),
        ('enz', 'Nouns ending in -enz are feminine'),
        ('anz', 'Nouns ending in -anz are feminine'),
        ('ik', 'Nouns ending in -ik are feminine'),
        ('ur', 'Nouns ending in -ur are feminine'),
        ('ei', 'Nouns ending in -ei are feminine'),
    ],
    'das': [
        ('chen', 'Nouns ending in -chen (diminutive) are always neuter'),
        ('lein', 'Nouns ending in -lein (diminutive) are always neuter'),
        ('ment', 'Nouns ending in -ment are neuter'),
        ('nis', 'Nouns ending in -nis are usually neuter'),
        ('tum', 'Nouns ending in -tum are neuter'),
        ('um', 'Nouns ending in -um are neuter'),
    ],
}


def _get_gender_hint(word, gender):
    noun = _strip_article(word).lower()
    rules = _GENDER_RULES.get(gender, [])
    for suffix, explanation in rules:
        if noun.endswith(suffix):
            return explanation
    return None


def _get_random_noun(user, exclude_ids=None):
    qs = VocabularyItem.objects.filter(
        language__code='de',
        part_of_speech='noun',
    ).exclude(gender='').exclude(gender__isnull=True)

    if exclude_ids:
        qs = qs.exclude(id__in=exclude_ids)

    item = qs.order_by('?').first()

    if item is None and exclude_ids:
        item = VocabularyItem.objects.filter(
            language__code='de',
            part_of_speech='noun',
        ).exclude(gender='').exclude(gender__isnull=True).order_by('?').first()

    return item


def _get_session_recent(request, key='gender_recent_ids', max_items=10):
    recent = request.session.get(key, [])
    return recent


def _add_to_session_recent(request, item_id, key='gender_recent_ids', max_items=10):
    recent = request.session.get(key, [])
    recent.append(item_id)
    if len(recent) > max_items:
        recent = recent[-max_items:]
    request.session[key] = recent


def _award_xp(user, points):
    activity, _ = DailyActivity.objects.get_or_create(
        user=user, activity_date=date.today()
    )
    activity.xp_earned += points
    activity.cards_reviewed += 1
    activity.save()


def _update_streak(user):
    from core.models import UserProfile
    from datetime import timedelta
    profile, _ = UserProfile.objects.get_or_create(user=user)
    today = date.today()

    if profile.last_activity_date == today:
        return

    yesterday = today - timedelta(days=1)
    if profile.last_activity_date == yesterday:
        profile.current_streak += 1
    elif profile.last_activity_date != today:
        profile.current_streak = 1

    profile.last_activity_date = today
    if profile.current_streak > profile.longest_streak:
        profile.longest_streak = profile.current_streak
    profile.save()


@login_required
def gender_drill_view(request):
    score, _ = GenderDrillScore.objects.get_or_create(user=request.user)

    request.session['gender_recent_ids'] = []

    item = _get_random_noun(request.user)
    if item:
        _add_to_session_recent(request, item.id)

    today_activity = DailyActivity.objects.filter(
        user=request.user, activity_date=date.today()
    ).first()
    today_count = today_activity.cards_reviewed if today_activity else 0

    return render(request, 'trainers/gender_drill.html', {
        'item': item,
        'noun_word': _strip_article(item.word) if item else '',
        'score': score,
        'today_count': today_count,
    })


@login_required
@require_POST
def gender_check_view(request):
    item_id = request.POST.get('item_id')
    user_answer = request.POST.get('answer', '').strip().lower()

    item = VocabularyItem.objects.select_related('topic').filter(id=item_id).first()
    if not item:
        return gender_next_view(request)

    score, _ = GenderDrillScore.objects.get_or_create(user=request.user)
    is_correct = user_answer == item.gender

    score.total_attempts += 1
    if is_correct:
        score.correct_attempts += 1
        score.current_streak += 1
        if score.current_streak > score.best_streak:
            score.best_streak = score.current_streak
        xp = 3
    else:
        score.current_streak = 0
        xp = 1
    score.save()

    _award_xp(request.user, xp)
    _update_streak(request.user)

    today_activity = DailyActivity.objects.filter(
        user=request.user, activity_date=date.today()
    ).first()
    today_count = today_activity.cards_reviewed if today_activity else 0

    gender_hint = _get_gender_hint(item.word, item.gender) if not is_correct else None

    return render(request, 'trainers/partials/gender_result.html', {
        'item': item,
        'noun_word': _strip_article(item.word),
        'is_correct': is_correct,
        'user_answer': user_answer,
        'xp_earned': xp,
        'score': score,
        'today_count': today_count,
        'gender_hint': gender_hint,
    })


@login_required
def gender_next_view(request):
    recent_ids = _get_session_recent(request)
    item = _get_random_noun(request.user, exclude_ids=recent_ids)

    if item:
        _add_to_session_recent(request, item.id)

    score, _ = GenderDrillScore.objects.get_or_create(user=request.user)

    today_activity = DailyActivity.objects.filter(
        user=request.user, activity_date=date.today()
    ).first()
    today_count = today_activity.cards_reviewed if today_activity else 0

    return render(request, 'trainers/partials/gender_card.html', {
        'item': item,
        'noun_word': _strip_article(item.word) if item else '',
        'score': score,
        'today_count': today_count,
    })


def _split_sentence(sentence):
    parts = sentence.split('___')
    return parts


def _get_random_exercise(case_filter=None, exclude_indices=None):
    exercises = CASE_EXERCISES
    if case_filter and case_filter != 'all':
        exercises = [e for e in exercises if e['case'] == case_filter]
    if not exercises:
        exercises = CASE_EXERCISES

    if exclude_indices:
        available = [(i, e) for i, e in enumerate(CASE_EXERCISES) if i not in exclude_indices and (not case_filter or case_filter == 'all' or e['case'] == case_filter)]
        if not available:
            available = [(i, e) for i, e in enumerate(CASE_EXERCISES) if not case_filter or case_filter == 'all' or e['case'] == case_filter]
        if available:
            idx, exercise = random.choice(available)
            return idx, exercise

    idx = CASE_EXERCISES.index(random.choice(exercises))
    return idx, CASE_EXERCISES[idx]


@login_required
def case_drill_view(request):
    score, _ = CaseDrillScore.objects.get_or_create(user=request.user)
    case_filter = request.GET.get('case', 'all')

    request.session['case_recent_indices'] = []
    request.session['case_filter'] = case_filter

    idx, exercise = _get_random_exercise(case_filter)
    _add_to_session_recent(request, idx, key='case_recent_indices', max_items=15)

    today_activity = DailyActivity.objects.filter(
        user=request.user, activity_date=date.today()
    ).first()
    today_count = today_activity.cards_reviewed if today_activity else 0

    colors = CASE_COLORS.get(exercise['case'], CASE_COLORS['Nominativ'])

    sentence_parts = _split_sentence(exercise['sentence'])

    return render(request, 'trainers/case_drill.html', {
        'exercise': exercise,
        'exercise_idx': idx,
        'score': score,
        'today_count': today_count,
        'case_filter': case_filter,
        'case_colors': colors,
        'sentence_parts': sentence_parts,
    })


@login_required
@require_POST
def case_check_view(request):
    exercise_idx = int(request.POST.get('exercise_idx', 0))
    user_answer = request.POST.get('answer', '').strip()
    case_filter = request.session.get('case_filter', 'all')

    if exercise_idx < 0 or exercise_idx >= len(CASE_EXERCISES):
        return case_next_view(request)

    exercise = CASE_EXERCISES[exercise_idx]
    score, _ = CaseDrillScore.objects.get_or_create(user=request.user)
    is_correct = user_answer == exercise['correct']

    score.total_attempts += 1
    if is_correct:
        score.correct_attempts += 1
        score.current_streak += 1
        if score.current_streak > score.best_streak:
            score.best_streak = score.current_streak
        xp = 3
    else:
        score.current_streak = 0
        xp = 1
    score.save()

    _award_xp(request.user, xp)
    _update_streak(request.user)

    today_activity = DailyActivity.objects.filter(
        user=request.user, activity_date=date.today()
    ).first()
    today_count = today_activity.cards_reviewed if today_activity else 0

    colors = CASE_COLORS.get(exercise['case'], CASE_COLORS['Nominativ'])

    sentence_parts = _split_sentence(exercise['sentence'])

    return render(request, 'trainers/partials/case_result.html', {
        'exercise': exercise,
        'is_correct': is_correct,
        'user_answer': user_answer,
        'xp_earned': xp,
        'score': score,
        'today_count': today_count,
        'case_colors': colors,
        'sentence_parts': sentence_parts,
    })


@login_required
def case_next_view(request):
    case_filter = request.session.get('case_filter', 'all')
    recent_indices = _get_session_recent(request, key='case_recent_indices')

    idx, exercise = _get_random_exercise(case_filter, exclude_indices=set(recent_indices))
    _add_to_session_recent(request, idx, key='case_recent_indices', max_items=15)

    score, _ = CaseDrillScore.objects.get_or_create(user=request.user)

    today_activity = DailyActivity.objects.filter(
        user=request.user, activity_date=date.today()
    ).first()
    today_count = today_activity.cards_reviewed if today_activity else 0

    colors = CASE_COLORS.get(exercise['case'], CASE_COLORS['Nominativ'])

    sentence_parts = _split_sentence(exercise['sentence'])

    return render(request, 'trainers/partials/case_card.html', {
        'exercise': exercise,
        'exercise_idx': idx,
        'score': score,
        'today_count': today_count,
        'case_colors': colors,
        'sentence_parts': sentence_parts,
    })
