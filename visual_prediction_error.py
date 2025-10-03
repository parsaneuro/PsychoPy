# -*- coding: utf-8 -*-
from psychopy import visual, core, event, gui, data
import os, random, csv

# ============================
# Literature Documantation
# ============================
# The documentation related to this project and underlying literature for that can be found in the same repository in a file named "facilitated_visual_perception_prediction"


# ============================
# Participant Info
# ============================
expInfo = {'Participant': '', 'Session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title='fMRI Task')
if not dlg.OK:
    core.quit()

filename = f"{expInfo['Participant']}_session{expInfo['Session']}_{data.getDateStr()}.csv"

# ============================
# Window
# ============================
win = visual.Window(
    size=(1024, 768),
    color='grey',
    units='pix',
    fullscr=False,
    monitor="testMonitor"
)

# ============================
# Load PNG Images
# ============================
this_dir = os.getcwd()

# Map intact images to their blurred counterparts
conditions = [
    {"stim": "congruent.png", "mask": "congruent_blur.png", "label": "congruent"},
    {"stim": "incongruent.png", "mask": "incongruent_blur.png", "label": "incongruent"}
]

stimuli = []
# Fixed display size for all images
img_size = (512, 512)

for cond in conditions:
    stim_path = os.path.join(this_dir, cond["stim"])
    mask_path = os.path.join(this_dir, cond["mask"])
    if not (os.path.exists(stim_path) and os.path.exists(mask_path)):
        raise RuntimeError(f"⚠ Missing file: {cond['stim']} or {cond['mask']} in {this_dir}")

    stim_img = visual.ImageStim(win, image=stim_path, size=img_size, pos=(0, 0))
    mask_img = visual.ImageStim(win, image=mask_path, size=img_size, pos=(0, 0))
    stimuli.append({"stim": stim_img, "mask": mask_img, "label": cond["label"], "name": cond["stim"]})

# ============================
# Timing (doubled for testing)
# ============================
fix_dur = 1.0
stim_dur = 0.6
mask_dur = 0.988
resp_dur = 3.0
iti_min, iti_max = 4.0, 8.0

# ============================
# Visual Elements
# ============================
fixation = visual.TextStim(win, text='+', color='white', height=40)

response_text = visual.TextStim(
    win,
    text="Congruent = 1    Incongruent = 2",
    color='white',
    height=40,        # larger text
    pos=(0, 0),       # centered
    wrapWidth=2000    # prevent line break
)

# ============================
# Trial Loop
# ============================
results = []
globalClock = core.Clock()

# Randomize order
random.shuffle(stimuli)

for trial in stimuli:
    # Fixation
    fixation.draw()
    win.flip()
    core.wait(fix_dur)

    # Stimulus
    trial["stim"].draw()
    win.flip()
    core.wait(stim_dur)

    # Mask (blurred version)
    trial["mask"].draw()
    win.flip()
    core.wait(mask_dur)

    # Response window (instructions in center)
    response_text.draw()
    win.flip()
    trialClock = core.Clock()
    keys = event.waitKeys(maxWait=resp_dur, keyList=['1', '2'], timeStamped=trialClock)

    if keys:
        key, rt = keys[0]
    else:
        key, rt = None, None

    # ITI jitter
    iti = random.uniform(iti_min, iti_max)
    win.flip()
    core.wait(iti)

    # Save trial data
    results.append([expInfo['Participant'], expInfo['Session'], trial["name"], trial["label"], key, rt])

# ============================
# Save Results
# ============================
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Participant', 'Session', 'Stimulus', 'Condition', 'Response', 'RT'])
    writer.writerows(results)

win.close()
core.quit()
