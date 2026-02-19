from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Lesson, Exercise, UserLessonProgress
from core.models import UserProfile
from stats.models import DailyActivity


@login_required
def lessons_list_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_langs = request.user.user_languages.select_related('language').filter(is_active=True)
    lang_code = request.GET.get('lang')

    if not lang_code and user_langs.exists():
        lang_code = user_langs.first().language.code

    lessons = Lesson.objects.filter(
        language__code=lang_code, is_active=True
    ).select_related('language', 'topic')

    # Attach user progress to each lesson
    progress_map = {}
    if request.user.is_authenticated:
        for p in UserLessonProgress.objects.filter(user=request.user, lesson__language__code=lang_code):
            progress_map[p.lesson_id] = p

    for lesson in lessons:
        lesson.progress = progress_map.get(lesson.id)

    return render(request, 'lessons/list.html', {
        'lessons': lessons,
        'user_langs': user_langs,
        'current_lang': lang_code,
    })


@login_required
def lesson_detail_view(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug, is_active=True)
    exercises = lesson.exercises.all()

    progress, created = UserLessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson
    )

    # If completed, show summary
    if progress.is_completed:
        return render(request, 'lessons/lesson_complete.html', {
            'lesson': lesson,
            'progress': progress,
            'exercises': exercises,
        })

    # Get current exercise
    current_idx = progress.current_exercise
    if current_idx >= exercises.count():
        # All done, mark complete
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.xp_earned = lesson.xp_reward + (progress.correct_answers * 2)
        progress.save()
        _update_activity(request.user, progress)
        return render(request, 'lessons/lesson_complete.html', {
            'lesson': lesson,
            'progress': progress,
        })

    exercise = exercises[current_idx]

    return render(request, 'lessons/lesson_session.html', {
        'lesson': lesson,
        'exercise': exercise,
        'progress': progress,
        'total': exercises.count(),
        'current_num': current_idx + 1,
        'options': exercise.get_shuffled_options(),
    })


@login_required
@require_POST
def check_answer_view(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    lesson = exercise.lesson
    progress, _ = UserLessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson
    )

    user_answer = request.POST.get('answer', '').strip()
    is_correct = _check_answer(exercise, user_answer)

    progress.total_answered += 1
    if is_correct:
        progress.correct_answers += 1
    progress.save()

    return render(request, 'lessons/partials/answer_feedback.html', {
        'exercise': exercise,
        'is_correct': is_correct,
        'user_answer': user_answer,
        'progress': progress,
        'lesson': lesson,
    })


@login_required
@require_POST
def next_exercise_view(request, lesson_slug):
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    progress, _ = UserLessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson
    )

    progress.current_exercise += 1
    progress.save()

    exercises = lesson.exercises.all()
    total = exercises.count()

    if progress.current_exercise >= total:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.xp_earned = lesson.xp_reward + (progress.correct_answers * 2)
        progress.save()
        _update_activity(request.user, progress)
        return render(request, 'lessons/partials/lesson_complete_partial.html', {
            'lesson': lesson,
            'progress': progress,
        })

    exercise = exercises[progress.current_exercise]
    return render(request, 'lessons/partials/exercise_card.html', {
        'exercise': exercise,
        'lesson': lesson,
        'progress': progress,
        'total': total,
        'current_num': progress.current_exercise + 1,
        'options': exercise.get_shuffled_options(),
    })


@login_required
@require_POST
def restart_lesson_view(request, lesson_slug):
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    UserLessonProgress.objects.filter(user=request.user, lesson=lesson).delete()
    return redirect('lessons:detail', slug=lesson_slug)


def _check_answer(exercise, user_answer):
    correct = exercise.correct_answer.strip().lower()
    answer = user_answer.strip().lower()

    if exercise.exercise_type == 'multiple_choice':
        return answer == correct
    elif exercise.exercise_type == 'fill_blank':
        # Allow minor typos: exact match or contained
        return answer == correct
    elif exercise.exercise_type == 'translation':
        # Accept if answer contains the correct translation or vice versa
        return answer == correct or correct in answer
    elif exercise.exercise_type == 'reorder':
        return answer == correct
    return answer == correct


def _update_activity(user, progress):
    activity, _ = DailyActivity.objects.get_or_create(
        user=user, activity_date=date.today()
    )
    activity.lessons_completed += 1
    activity.xp_earned += progress.xp_earned
    activity.save()
