from schoolplanner import *

days = [1, 1, 0, 1, 1]
five_days = [1, 1, 0, 1, 2]
skip_weeks = [1, 2, 3, 4]

generate_pdf(
    [
        heading('History'),
        subject('Geography'),
        subject('story-of-the-world', skip_weeks=skip_weeks, days=days),
        heading('Science'),
        subject('Science'),
        heading('Visual Arts'),
        subject('Art'),
        heading('Music'),
        subject('Music'),
        heading('Physical Education'),
        subject('Physical Education'),
        heading('Bible'),
        subject('bible-quest', skip_weeks=skip_weeks, days=days),
        subject('Character Trait', skip_weeks=skip_weeks, days=days),
        heading('Reading'),
        subject('all-about-reading', skip_weeks=skip_weeks, days=days,
                start_lesson='1-42'),
        subject('all-about-reading', skip_weeks=skip_weeks, days=days,
                start_lesson='3-1'),
        subject('Read Alouds'),
        heading('Spelling'),
        subject('all-about-spelling', skip_weeks=skip_weeks, days=days,
                start_lesson='2-1'),
        subject('all-about-spelling', skip_weeks=skip_weeks, days=days,
                start_lesson='3-1'),
    ],
    num_weeks=36,
    out_file='2015a.pdf'
)

generate_pdf(
    [
        heading('Math'),
        subject('singapore-math', skip_weeks=skip_weeks, days=five_days,
                start_lesson='3B.12'),
        subject('singapore-math', skip_weeks=skip_weeks, days=days,
                start_lesson='1A Review 1'),
        subject('Programming'),
        heading('Language Arts'),
        subject('first-language-lessons', skip_weeks=skip_weeks, days=days,
                start_lesson='Level 1', start_part=52),
        subject('new-american-cursive', skip_weeks=skip_weeks, days=days),
        heading('Health'),
        subject('health-2015', skip_weeks=skip_weeks, days=days),
        heading('Latin'),
        subject('school-song-latin', skip_weeks=skip_weeks, days=days),
        heading('Classical Conversations'),
        subject('CC Review'),
        subject('Presentation')
    ],
    num_weeks=36,
    out_file='2015b.pdf'
)
