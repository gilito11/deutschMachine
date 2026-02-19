from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class ReviewResult:
    interval_days: int
    repetitions: int
    easiness_factor: float
    next_review_date: date


def sm2(quality: int, repetitions: int, easiness_factor: float, interval_days: int) -> ReviewResult:
    """
    SM-2 spaced repetition algorithm.

    quality: 0-5 (0=blackout, 5=perfect)
    """
    if quality < 3:
        repetitions = 0
        interval_days = 1
    else:
        if repetitions == 0:
            interval_days = 1
        elif repetitions == 1:
            interval_days = 6
        else:
            interval_days = round(interval_days * easiness_factor)
        repetitions += 1

    easiness_factor += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    easiness_factor = max(1.3, easiness_factor)

    return ReviewResult(
        interval_days=interval_days,
        repetitions=repetitions,
        easiness_factor=round(easiness_factor, 2),
        next_review_date=date.today() + timedelta(days=interval_days),
    )
