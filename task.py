# Behavioral task
# Carolina Feher da Silva <carolfsu@gmail.com>
# To run it, please download the Source Code Pro font or change the font below
# on line 77.

from __future__ import (absolute_import, division, print_function, unicode_literals)
from future_builtins import *

import random
import sys
import os

# ------------------------------------
# Parameters

# Initial states
INIT_STATES = ('AA', 'AB', 'BA', 'BB')
# Common transitions, given initial state and choice
COMMON_TRANS = {
    ('AA', 'left'): 'blue',
    ('AB', 'left'): 'pink',
    ('BA', 'left'): 'pink',
    ('BB', 'left'): 'blue',
    ('AA', 'right'): 'pink',
    ('AB', 'right'): 'blue',
    ('BA', 'right'): 'blue',
    ('BB', 'right'): 'pink',
}
# Reward probability
RWRD_PROB = 0.7
# Common transition probability
COMMON_PROB = 0.8
# Number of trials
NUM_TRIALS = 250
# Number of trials in a block
BLOCK = 50
# Results directory
RES_DIR = 'results'
# Money per trial
RWRD = 0.18

# ------------------------------------

# Round reward for easier paying
def get_money_reward(x):
    x *= RWRD
    return round(x, 1)

if __name__ == '__main__':
    from psychopy import visual, core, event, gui, logging, data
    from quiz import quiz, read_questions

    # Get experiment information
    info = {'Participant': '', 'Group': ['Experimental', 'Control']}
    dlg = gui.DlgFromDict(info, title='Experiment 1')
    if not dlg.OK:
        core.quit()

    if not os.path.exists(RES_DIR):
        os.mkdir(RES_DIR)
    filename = os.path.join(RES_DIR, '{}_{}_{}'.format(info['Participant'], info['Group'], data.getDateStr()))
    # Log information
    logFile = logging.LogFile(filename + '.log', level=logging.WARNING)

    # Condition
    control = (info['Group'] == 'Control')

    # Create window
    win = visual.Window(size=[1024, 768], fullscr=(info['Participant'] != 'test'), units='height', color=(0, 0, 0),
        checkTiming=False)

    # Create stimuli

    # Initial stimuli
    inistim = visual.TextStim(win=win,
        pos=(0, 0),
        height=0.3,
        fontFiles=['Source Code Pro.ttf'],
        font='Source Code Pro',
        name='Initial stimulus',
    )

    # Response stimulus
    respstim = visual.ImageStim(win=win,
        image='response.png',
        size=(0.4, 0.09),
        name='Response image'
    )

    # Slow feedback
    slow = visual.TextStim(win=win,
        text='SLOW',
        pos=(0, 0),
        height=0.15,
        name='Slow feedback',
    )

    # Final stimuli
    pink = visual.Rect(win=win, lineWidth=0, fillColor=(1, 0, 0.5), width=2/3, height=0.5, pos=(0, 0),
        name='Pink stimulus')
    blue = visual.Rect(win=win, lineWidth=0, fillColor=(0, 0.5, 1), width=2/3, height=0.5, pos=(0, 0),
        name='Blue stimulus')

    # Reward
    rwrd = visual.TextStim(win=win,
        text='$'.format(RWRD),
        color=(0, 1, 0),
        pos=(0, 0),
        height=0.3,
        name='Reward',
    )

    # No reward
    noRwrd = visual.TextStim(win=win,
        text='X'.format(RWRD),
        color=(-1, -1, -1),
        pos=(0, 0),
        height=0.5,
        name='No reward',
    )

    # Message
    msg = visual.TextStim(win=win,
        pos=(0, 0),
        height=0.06,
        name='Message',
    )

    # Quiz
    msg.text = 'QUIZ\nPress SPACE to start'
    msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=('space', 'escape'))
    # check for quit:
    if "escape" in keys:
        core.quit()
    win.flip()
    core.wait(1)

    quiz(read_questions('quiz.txt'), win)

    # Determine reward probabilities

    try:
        n = int(info['Participant'])
    except ValueError:
        if random.random() < 0.5:
            rwrd_probs = {'pink': RWRD_PROB, 'blue': 1 - RWRD_PROB}
        else:
            rwrd_probs = {'pink': 1 - RWRD_PROB, 'blue': RWRD_PROB}
    else:
        if n % 2 == 0:
            rwrd_probs = {'pink': RWRD_PROB, 'blue': 1 - RWRD_PROB}
        else:
            rwrd_probs = {'pink': 1 - RWRD_PROB, 'blue': RWRD_PROB}

    # Initial screen
    msg.text = 'EXPERIMENT\nPress SPACE to start'
    msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=('space', 'escape'))
    # check for quit:
    if "escape" in keys:
        core.quit()
    win.flip()
    core.wait(1)

    # Trial loop
    with open(filename + '.csv', 'w') as resultsFile:
        resultsFile.write('trial,reward_prob_pink,reward_prob_blue,init_state,common,'
            'choice,rt1,final_state,rt2,reward,slow\n')

        trial = 0
        slow_trials = 0
        rewards = 0
        while (trial - slow_trials) < NUM_TRIALS:
            # Initial state
            inist = random.choice(INIT_STATES)
            # Common transition
            common = random.random() < COMMON_PROB

            resultsFile.write('{},{},{},{},{}'.format(
                trial + 1, rwrd_probs['pink'], rwrd_probs['blue'], inist, int(common)))

            if not control:
                inistim.text = '{} '.format(inist[0])
                inistim.draw()
                win.flip()
                core.wait(1)
                win.flip()
                core.wait(1)
                inistim.text = ' {}'.format(inist[1])
                inistim.draw()
                win.flip()
                core.wait(1)
            else:
                inistim.text = inist
                inistim.draw()
                win.flip()
                core.wait(3)
            win.flip()
            core.wait(1)

            keys = event.getKeys()
            # check for quit:
            if "escape" in keys:
                core.quit()

            # Collect response

            respstim.draw()
            win.flip()
            keys_times = event.waitKeys(maxWait=2, keyList=('left', 'right', 'escape'),
                timeStamped=core.Clock())
            if keys_times is not None:
                assert len(keys_times) == 1
                choice, rt1 = keys_times[0]
                # check for quit:
                if choice == 'escape':
                    core.quit()
            else: # slow response
                slow_trials += 1
                slow.draw()
                win.flip()
                core.wait(1)
                trial += 1
                resultsFile.write(',{},{},{},{},{},{}\n'.format(
                    '',
                    '',
                    '',
                    '',
                    0,
                    1,
                ))
                continue

            # Final state

            finalst = COMMON_TRANS[(inist, choice)] # Common
            if not common: # Rare
                if finalst == 'pink':
                    finalst = 'blue'
                else:
                    finalst = 'pink'
            assert finalst in ('pink', 'blue')

            resultsFile.write(',{},{},{}'.format(choice, rt1, finalst))

            if finalst == 'pink':
                pink.draw()
            else:
                blue.draw()
            win.flip()

            key, rt2 = event.waitKeys(keyList=('up', 'escape'), timeStamped=core.Clock())[0]
            # check for quit:
            if key == 'escape':
                core.quit()

            # Reward
            reward = random.random() < rwrd_probs[finalst]
            rewards += int(reward)
            if reward:
                rwrd.draw()
            else:
                noRwrd.draw()
            win.flip()
            core.wait(2)

            trial += 1

            resultsFile.write(',{},{},{}\n'.format(rt2, int(reward), 0))

            # Interval
            if (trial - slow_trials) % BLOCK == 0 and (trial - slow_trials) < NUM_TRIALS:
                msg.text = 'INTERVAL\nPress any key to continue'
                msg.draw()
                win.flip()
                keys = event.waitKeys()
                # check for quit:
                if "escape" in keys:
                    core.quit()

    # Final screen
    msg.text = 'THANK YOU\nYou won CHF {:.2f}'.format(get_money_reward(rewards))
    msg.draw()
    win.flip()
    event.waitKeys(keyList=('escape',))
