from __future__ import (absolute_import, division, print_function, unicode_literals)
from future_builtins import *

from psychopy import visual, core, event, gui, logging, data
from collections import deque

def show_answer_clicked(pos):
    return pos[0] >= -183 and pos[0] <= 183 and pos[1] >= -347 and pos[1] <= -254

def again_clicked(pos):
    return pos[0] >= -307 and pos[0] <= -93 and pos[1] >= -347 and pos[1] <= -254

def good_clicked(pos):
    return pos[0] >= 93 and pos[0] <= 307 and pos[1] >= -347 and pos[1] <= -254

# Creates a Quiz in Psychopy
def quiz(questions, win):
    mouse = event.Mouse(True, win=win)
    units = win.units
    win.units = 'pix'
    # Question
    question = visual.TextStim(
        win,
        pos=(-400, +300),
        alignHoriz='left',
        alignVert='top',
        wrapWidth=800,
        height=30,
    )

    # Line
    line = visual.Line(win, start=(-500, +50), end=(+500, +50), lineColor='white')

    # Answer
    answer = visual.TextStim(
        win,
        pos=(-400, 0),
        alignHoriz='left',
        alignVert='top',
        wrapWidth=800,
        height=30,
    )

    # Show Answer
    show_answer = visual.ImageStim(win=win,
        image='show_answer.png',
        size=(365, 93),
        pos=(0, -300),
        name='Show Answer',
        units='pix'
    )

    # Again
    again = visual.ImageStim(win=win,
        image='again.png',
        size=(213, 93),
        pos=(-200, -300),
        name='Again',
        units='pix'
    )

    # Good
    good = visual.ImageStim(win=win,
        image='good.png',
        size=(213, 93),
        pos=(+200, -300),
        name='Good',
        units='pix'
    )

    qalist = deque(questions)
    while True:
        try:
            q, a = qalist.popleft()
        except IndexError:
            break

        question.text = q
        answer.text = a

        question.draw()
        line.draw()
        show_answer.draw()
        win.flip()
        core.wait(0.2)
        event.clearEvents()

        while True:
            if not mouse.getPressed()[0]:
                continue
            pos = mouse.getPos()
            if show_answer_clicked(pos):
                break

        question.draw()
        line.draw()
        answer.draw()
        again.draw()
        good.draw()
        win.flip()
        core.wait(0.2)
        event.clearEvents()

        while True:
            if not mouse.getPressed()[0]:
                continue
            pos = mouse.getPos()
            if again_clicked(pos):
                qalist.append((q, a))
                break
            elif good_clicked(pos):
                break

    win.units = units
    mouse.setVisible(False)
    return

def read_questions(fn):
    questions = []
    with open(fn) as f:
        while True:
            q, a = f.readline(), f.readline()
            if not q:
                break
            questions.append((q.strip(), a.strip()))
    return questions
