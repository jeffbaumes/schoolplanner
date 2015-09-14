from schoolplanner import *

days = [1, 1, 0, 1, 1]

generate_pdf(
    [
        subject('singapore-math-1', skip_weeks=[1, 2, 3], days=days),
        subject('singapore-math-3', skip_weeks=[1, 2, 3], days=days,
                start_lesson='3B.12'),
        subject('singapore-math-4', skip_weeks=[1, 2, 3], days=days),
        subject('CC Review')
    ],
    num_weeks=36,
    out_file='sample.pdf'
)
