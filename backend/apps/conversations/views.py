import re
from datetime import date

import anthropic
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404

from .models import ConversationSession, Message
from core.models import UserLanguage
from stats.models import DailyActivity


def _get_system_prompt(session):
    scenario_prompts = {
        'free': 'Have a natural conversation.',
        'job_interview': 'Simulate a job interview. You are the interviewer at a Swiss/German company.',
        'supermarket': 'Simulate a conversation at a supermarket. You are a cashier or fellow shopper.',
        'apartment': 'Simulate apartment viewing. You are a landlord showing an apartment.',
        'restaurant': 'Simulate ordering at a restaurant. You are a waiter.',
        'doctor': 'Simulate a doctor visit. You are a doctor.',
        'friends': 'Simulate meeting someone new at a social event.',
        'transport': 'Simulate asking for directions or buying a ticket at a train station.',
    }

    lang_name = session.language.name
    level = session.user_level
    scenario_desc = scenario_prompts.get(session.scenario, 'Have a natural conversation.')

    return f"""You are a {lang_name} language tutor for a Spanish speaker at {level} level.

Rules:
1. Speak in {lang_name} adjusted to {level} level. Use simple vocabulary and short sentences for A1-A2, more complex for B1+.
2. {scenario_desc}
3. After each response, if the user made grammatical errors in their message, add a correction section starting with "Corrections:" explaining the errors in Spanish.
4. Keep responses concise (2-4 sentences max for conversation, then corrections if needed).
5. Be encouraging and natural.
6. If user writes in Spanish, gently encourage them to try in {lang_name}.
7. Use common everyday vocabulary appropriate for someone living in Switzerland/Germany."""


def _call_claude(session):
    if not settings.ANTHROPIC_API_KEY:
        raise ValueError("AI conversations require an API key. Contact the admin.")

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    messages_history = []
    for msg in session.messages.all():
        messages_history.append({"role": msg.role, "content": msg.content})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=_get_system_prompt(session),
        messages=messages_history,
    )
    return response.content[0].text


def _parse_corrections(text):
    """Separate the main response from corrections."""
    patterns = [
        r'(?:\n\n|\n)Corrections:\s*',
        r'(?:\n\n|\n)Correcciones:\s*',
    ]
    for pattern in patterns:
        match = re.split(pattern, text, maxsplit=1, flags=re.IGNORECASE)
        if len(match) == 2:
            return match[0].strip(), match[1].strip()
    return text.strip(), ''


@login_required
def chat_view(request):
    user_langs = request.user.user_languages.select_related('language').filter(is_active=True)
    sessions = ConversationSession.objects.filter(user=request.user).select_related('language')[:20]

    scenarios = [
        {'value': 'free', 'label': 'Free Conversation', 'emoji': '\U0001f5e3\ufe0f'},
        {'value': 'job_interview', 'label': 'Job Interview', 'emoji': '\U0001f4bc'},
        {'value': 'supermarket', 'label': 'At the Supermarket', 'emoji': '\U0001f6d2'},
        {'value': 'apartment', 'label': 'Apartment Hunting', 'emoji': '\U0001f3e0'},
        {'value': 'restaurant', 'label': 'At the Restaurant', 'emoji': '\U0001f37d\ufe0f'},
        {'value': 'doctor', 'label': 'Doctor Visit', 'emoji': '\U0001f3e5'},
        {'value': 'friends', 'label': 'Meeting Friends', 'emoji': '\U0001f465'},
        {'value': 'transport', 'label': 'Public Transport', 'emoji': '\U0001f686'},
    ]

    context = {
        'user_langs': user_langs,
        'sessions': sessions,
        'scenarios': scenarios,
    }
    return render(request, 'conversations/chat.html', context)


@login_required
@require_POST
def new_session_view(request):
    scenario = request.POST.get('scenario', 'free')
    language_id = request.POST.get('language')

    if not language_id:
        return redirect('conversations:chat')

    user_lang = get_object_or_404(
        UserLanguage, user=request.user, language_id=language_id, is_active=True
    )

    session = ConversationSession.objects.create(
        user=request.user,
        language=user_lang.language,
        scenario=scenario,
        user_level=user_lang.current_level,
        title=dict(ConversationSession.SCENARIO_CHOICES).get(scenario, 'Conversation'),
    )

    # Generate initial AI greeting
    greeting_msg = Message.objects.create(
        session=session,
        role='user',
        content='[Start the conversation. Greet me and set the scene for the scenario.]',
    )

    try:
        ai_response = _call_claude(session)
        content, correction = _parse_corrections(ai_response)
    except (ValueError, Exception) as e:
        greeting_msg.delete()
        session.delete()
        from django.contrib import messages as django_messages
        django_messages.error(request, str(e) if isinstance(e, ValueError) else 'AI service temporarily unavailable.')
        return redirect('conversations:chat')

    # Delete the hidden prompt message and save the AI greeting
    greeting_msg.delete()

    Message.objects.create(
        session=session,
        role='assistant',
        content=content,
        correction=correction,
    )
    session.message_count = 1
    session.save()

    return redirect('conversations:session', session_id=session.id)


@login_required
def session_view(request, session_id):
    session = get_object_or_404(ConversationSession, id=session_id, user=request.user)
    messages_list = session.messages.all()

    lang_name = session.language.name
    placeholder = {
        'German': 'Schreib etwas auf Deutsch...',
        'English': 'Write something in English...',
    }.get(lang_name, f'Write something in {lang_name}...')

    context = {
        'session': session,
        'messages_list': messages_list,
        'placeholder': placeholder,
    }
    return render(request, 'conversations/session.html', context)


@login_required
@require_POST
def send_message_view(request, session_id):
    session = get_object_or_404(ConversationSession, id=session_id, user=request.user)
    user_text = request.POST.get('message', '').strip()

    if not user_text:
        return render(request, 'conversations/partials/message_pair.html', {
            'error': True,
        })

    # Save user message
    user_msg = Message.objects.create(
        session=session,
        role='user',
        content=user_text,
    )

    # Call Claude
    try:
        ai_response = _call_claude(session)
    except (ValueError, Exception):
        return render(request, 'conversations/partials/message_pair.html', {
            'user_msg': user_msg,
            'ai_msg': type('Msg', (), {'content': 'AI service temporarily unavailable. Try again later.', 'correction': ''})(),
        })
    content, correction = _parse_corrections(ai_response)

    # Save assistant message
    ai_msg = Message.objects.create(
        session=session,
        role='assistant',
        content=content,
        correction=correction,
    )

    # Update session count
    session.message_count = session.messages.count()
    session.save()

    # Update daily activity
    activity, _ = DailyActivity.objects.get_or_create(
        user=request.user, activity_date=date.today()
    )
    activity.conversations_count += 1
    activity.xp_earned += 5
    activity.save()

    return render(request, 'conversations/partials/message_pair.html', {
        'user_msg': user_msg,
        'ai_msg': ai_msg,
    })
