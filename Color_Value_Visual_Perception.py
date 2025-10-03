from psychopy import visual, core, event, gui
from psychopy.hardware import keyboard
import glob, os, random, pandas as pd
from datetime import datetime

# ===============================
# Dialogue box generation
# ===============================
dlg = gui.Dlg(title="Input Data")

# Add date
date = datetime.now().strftime('%Y%m%d_%H%M')

# Add fixed fields
dlg.addFixedField('expname', label='Task name', initial='Visual Task')
dlg.addFixedField('expdate', label='Date', initial=date)

# Add input fields
dlg.addField("Participant ID", label="Participant ID", initial="")
dlg.addField("Device Refresh Rate", 
             label="Device Refresh Rate \n (fill it empty, should be modified only by the supervisor)", 
             initial="60")

# Show dialog
data = dlg.show()

# Check if the user pressed Cancel
if not dlg.OK:
    print("User cancelled the experiment")
    core.quit()

# Convert dialog responses into dictionary
exp_info = {
    'expname': data[0],
    'expdate': data[1],
    'Participant': data[2],
    'RefreshRate': data[3]
}

# ===============================
# File saving
# ===============================
os.makedirs("data", exist_ok=True)
filename = f"data/{exp_info['Participant']}_results.csv"

# ===============================
# Stimuli loading
# ===============================
# Use the current working directory
stim_dir = os.getcwd()

# Load all JPG files from the current folder
image_files = glob.glob(os.path.join(stim_dir, "*.jpg"))

# Randomize trial order
random.shuffle(image_files)


# ===============================
# Window and stimuli
# ===============================
win = visual.Window(size=(1200, 800), color='black', units="pix", fullscr=False)
fixation = visual.TextStim(win, text='+', height=40, color='white')
stim = visual.ImageStim(win, size=(400, 400))

# ===============================
# Trial loop
# ===============================
results = []

for img in image_files:
    # Fixation cross (jittered 2–6s)
    jitter = random.uniform(2, 6)
    fixation_clock = core.Clock()
    while fixation_clock.getTime() < jitter:
        fixation.draw()
        win.flip()
        if 'escape' in event.getKeys():
            win.close()
            core.quit()

    # Present stimulus for 1s
    stim.image = img
    stim_clock = core.Clock()
    while stim_clock.getTime() < 1.0:   # 1 second
        stim.draw()
        win.flip()
        if 'escape' in event.getKeys():
            win.close()
            core.quit()

    # Phase 2: Show rating prompt only (1.5s response window)
    rating_text = visual.TextStim(
        win,
        text="How vivid was the image?\n\n1 = not vivid   4 = very vivid",
        color="white",
        height=28,
        pos=(0, 0)  # center, or adjust as you like
        )

    rating_text.draw()
    win.flip()

    # Collect response (1–4) during 1.5s response window
    keys = event.waitKeys(maxWait=3.5, keyList=['1','2','3','4','escape'], timeStamped=stim_clock)

    if keys:
        key, rt = keys[0]
        if key == 'escape':
            win.close()
            core.quit()
    else:
        key, rt = None, None

    # Store trial info
    results.append({
        "participant": exp_info['Participant'],
        "stimulus": os.path.basename(img),
        "response": key,
        "rt": rt,
        "jitter": jitter
    })

# ===============================
# Save results
# ===============================
df = pd.DataFrame(results)
df.to_csv(filename, index=False)

# End screen
end_text = visual.TextStim(win, text="Thank you!", color='white', height=40)
end_text.draw()
win.flip()
core.wait(2)

win.close()
core.quit()
