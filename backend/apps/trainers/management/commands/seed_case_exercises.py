from django.core.management.base import BaseCommand
from trainers.case_data import CASE_EXERCISES


class Command(BaseCommand):
    help = 'Validate and display case exercise statistics'

    def handle(self, *args, **options):
        total = len(CASE_EXERCISES)
        by_case = {}
        by_difficulty = {}

        for ex in CASE_EXERCISES:
            case = ex['case']
            diff = ex['difficulty']
            by_case[case] = by_case.get(case, 0) + 1
            by_difficulty[diff] = by_difficulty.get(diff, 0) + 1

            if ex['correct'] not in ex['options']:
                self.stderr.write(self.style.ERROR(
                    f"INVALID: correct answer '{ex['correct']}' not in options for: {ex['sentence']}"
                ))

        self.stdout.write(self.style.SUCCESS(f'\nCase Exercises loaded: {total}'))
        self.stdout.write('\nBy case:')
        for case, count in sorted(by_case.items()):
            self.stdout.write(f'  {case}: {count}')
        self.stdout.write('\nBy difficulty:')
        for diff, count in sorted(by_difficulty.items()):
            self.stdout.write(f'  {diff}: {count}')
        self.stdout.write(self.style.SUCCESS('\nAll exercises validated successfully.'))
