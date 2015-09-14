from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus.flowables import PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

import json
import os
import glob

courses = {}


def load_courses():
    courses_path = os.path.join(os.path.split(__file__)[0], 'courses')
    for course_fname in glob.glob(os.path.join(courses_path, '*.json')):
        with open(course_fname) as course_file:
            print course_fname
            course = json.load(course_file)
            course_id = os.path.splitext(os.path.split(course_fname)[1])[0]
            courses[course_id] = course

load_courses()


def _create_pdfdoc(pdfdoc, story):
    """
    Creates PDF doc from story.
    """
    pdf_doc = BaseDocTemplate(
        pdfdoc, pagesize=letter,
        leftMargin=inch, rightMargin=inch,
        topMargin=inch, bottomMargin=inch)
    main_frame = Frame(
        inch, inch,
        letter[0] - 2 * inch, letter[1] - 2 * inch,
        leftPadding=0, rightPadding=0, bottomPadding=0,
        topPadding=0, id='main_frame')
    main_template = PageTemplate(id='main_template', frames=[main_frame])
    pdf_doc.addPageTemplates([main_template])

    pdf_doc.build(story)


def subject(info={}, skip_weeks=[], days=[1, 1, 1, 1, 1],
            start_lesson=0, start_part=1):
    if isinstance(info, (str, unicode)):
        if info in courses:
            info = courses[info]
        else:
            info = {'name': info}

    return {
        'name': info.get('name', ''),
        'lessons': info.get('lessons', []),
        'skip_weeks': skip_weeks,
        'days': days,
        'start_lesson': start_lesson,
        'start_part': start_part,
        'type': 'subject'
    }


def heading(name):
    return {'name': name, 'type': 'heading'}


def generate_pdf(subjects, num_weeks, out_file='out.pdf'):
    styleSheet = getSampleStyleSheet()
    story = []
    body = styleSheet['BodyText']
    body.fontSize = 8

    for subject in subjects:
        if subject['type'] == 'subject':
            subject['cur_lesson'] = 0
            subject['cur_part'] = subject['start_part']
            for i, lesson in enumerate(subject['lessons']):
                if lesson['name'] == str(subject['start_lesson']):
                    subject['cur_lesson'] = i

    for i in range(num_weeks):
        spans = []
        story.append(Paragraph('Week ' + str(i + 1), styleSheet['Heading2']))
        data = [[
            Paragraph('<b>Subject</b>', body),
            Paragraph('<b>Monday</b>', body),
            Paragraph('<b>Tuesday</b>', body),
            Paragraph('<b>Wednesday</b>', body),
            Paragraph('<b>Thursday</b>', body),
            Paragraph('<b>Friday</b>', body)
        ]]
        for si, s in enumerate(subjects):
            sdata = [Paragraph('<b>' + s['name'] + '</b>', body)]
            if s['type'] == 'subject':
                for day in range(5):
                    text = ''
                    if i + 1 not in s['skip_weeks'] and s['days'][day]:
                        for repeat in range(s['days'][day]):
                            if s['cur_lesson'] >= len(s['lessons']):
                                if 'default' in s:
                                    text += '<b>' + s['default'] + '</b>'
                                continue
                            lesson = s['lessons'][s['cur_lesson']]
                            if repeat > 0:
                                text += ', '
                            text += '<b>' + str(lesson['name'])
                            if lesson['parts'] > 1:
                                text += '-' + str(s['cur_part']) + '</b>'

                            s['cur_part'] += 1
                            if s['cur_part'] > lesson['parts']:
                                s['cur_lesson'] += 1
                                s['cur_part'] = 1
                    sdata.append(Paragraph(text, body))
            else:
                for day in range(5):
                    sdata.append(Paragraph('', body))
                spans.append(('BACKGROUND', (0, si + 1), (5, si + 1),
                              colors.gainsboro))
                spans.append(('SPAN', (0, si + 1), (5, si + 1)))

            data.append(sdata)

        t = Table(data, (6.5 / 6) * inch)
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
            ('VALIGN', (1, 1), (-1, -1), 'TOP'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOTTOMPADDING', (1, 1), (-1, -1), 0.3 * inch),
        ] + spans))

        story.append(t)
        story.append(PageBreak())

    _create_pdfdoc(out_file, story)
