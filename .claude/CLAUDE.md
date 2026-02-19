# deutschMachine

App web de aprendizaje de idiomas (English + German) con SRS (Spaced Repetition), diseñada para españoles que se mudan a Suiza/Alemania.

## Tech Stack
- **Backend**: Django 5.1 + Python 3.13
- **Frontend**: Django Templates + TailwindCSS CDN + HTMX 1.9 + Alpine.js
- **DB**: PostgreSQL (Neon serverless) / SQLite (dev local)
- **AI**: Claude API (Sonnet) para conversación y corrección
- **Deploy**: Cloudflare Tunnel → Contabo VPS (learn.fincaradar.com)

## Estructura
```
backend/
├── apps/{core,vocabulary,srs,lessons,conversations,stats}/
├── deutschmachine/{settings,urls,wsgi}.py
├── templates/
├── static/
├── fixtures/
└── manage.py
```

## Comandos frecuentes
```bash
cd backend && python manage.py runserver 0.0.0.0:8001
python manage.py seed_content  # Carga vocabulario inicial
python manage.py makemigrations && python manage.py migrate
docker-compose up  # Dev con PostgreSQL
```

## Patrones
- Views: function-based con @login_required
- Frontend: HTMX partials para interactividad sin JS
- SRS: Algoritmo SM-2 en srs/engine.py
- Mismos patrones que casa-teva-lead-system

## Convenciones
- Código y commits en inglés
- Templates con Tailwind utility classes
- Dark mode soportado en toda la UI
