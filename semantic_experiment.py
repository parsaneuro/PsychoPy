# This experiment was designed by student id: 291928
# this code is designed based on PsychoPy version v2024.2.4
#-----importing all necessary libraries for the experiment---------------------------------------------------------------------

from psychopy import visual, core, gui
from datetime import datetime
from psychopy.hardware import keyboard
import numpy as np
import pandas as pd
import os


#-----making the dialogue box for fixed and input cells---------------------------------------------------------------------------------------------------

# dialogue box generation
dlg = gui.Dlg(title = "Input Data")

# adding date
date = datetime.now().strftime('%Y%m%d_%H%M')

# adding fixed fields
dlg.addFixedField('expname', label='Task name', initial='Semantic Task')
dlg.addFixedField('expdate', label='Date', initial=date)

# adding input cell
dlg.addField("Participant ID", label="Participant ID", initial="")
dlg.addField("Device Refresh Rate", label="Device Refresh Rate \n (fill it empty, should be modified only by the supervisor)", initial="60")

# displaying the dialogue box
data = dlg.show()

# Check if the user pressed Cancel
if not dlg.OK:
    print("User cancelled the experiment")
    core.quit()

# Data now contains the user input

# Generate a filename using participant ID, and experiment date from 'data' dictionary where id and date are saved there
# Create a "results" folder inside the current working directory
results_dir = os.path.join(os.getcwd(), 'results')
os.makedirs(results_dir, exist_ok=True)
# save the csv file in the created folder
filename = os.path.join(results_dir, f"Par_{data['Participant ID']}_{data['expdate']}.csv")

# making the refresh rate
# Attempt to convert input refresh rate to integer
try:
    refresh_rate = int(data["Device Refresh Rate"])
except (ValueError, TypeError):
    print("Invalid refresh rate input. Defaulting to 60 Hz.")
    refresh_rate = 60

# normalizing the referesh rate based on a 60 Hz monitor
refresh_rate_normalized = int(refresh_rate / 60)

#-----writing the header of our result file-------------------------------------------------------------------------------------------------------------

# 'a' used here instead of 'w' to if by any chance participant entered a wrong id, previous data is not goinig to be deleted and overwritten
with open(filename, 'a') as f:
    f.write('Condtion,Target,Word1,Word2,Word3,Answer,CorrectAnswer,RT,IsCorrect,Time\n')
    
#-----importing and reading the stimuli file------------------------------------------------------------------------------------------------------------

# important to note that the .stimuli csv' file should be in the folder of the code of the experiment
# also, your stimuli file should be saved in your code's directory with the following name: 'trials.csv'
# calling the working directory
working_dir = os.getcwd()
# make the path by concatenating working directory path with the file name 
trial_path = os.path.join(working_dir, 'trials.csv')
# reading the dataset based on its path
data_set = pd.read_csv(trial_path)

#-----creating the window format for the experiment-------------------------------------------------------------------------------------------------------

win = visual.Window([1024, 768], fullscr=True, units="pix", color=(0, 0, 0))

#-----activating keyboard for response teceiving----------------------------------------------------------------------------------------------------------

kb = keyboard.Keyboard()

#-----generating a core.Clock as a stop watch to be used in the study for stimuli presentation-----------------------------------------------------------

stimuli_clock = core.Clock()

#-----defining the escape function-----------------------------------------------------------------------------------------------------------------------

def escape_experiment():
    print("Experiment terminated by user.")
    win.close()
    core.quit()

#-----making the welcome window-------------------------------------------------------------------------------------------------------------------------

# writing the text which we want to show in the welcome window
welcome_instructions = (
                        "Welcome to our experiment.\n\n"
                        "You will see a target word and three choices.\n\n"
                        "Choose the word closest to the meaning or to a specific feature of the target word as fast as possible.\n\n"
                        "Left Answer: Keypress '1'. Middle Answer: Keypress '2'. Right Answer: Keypress '3'.\n\n"
                        "Press 'space' to start or 'escape' at any time to quit.")

# making the text-based stimuli on the window which we genrated earlier
# the wrapwidth here define the maximum width which is used by text.
instruction_text = visual.TextStim(win, text = welcome_instructions, color = (1,1,1) , height = 60, wrapWidth = 1800, pos = (0, 0))

# drawing the text
instruction_text.draw()
# flipping the window for illustration
win.flip()
# Wait until either 'space' or 'escape' is pressed
# wait relaese set to true to prevent multiplication in key responses due to long term press
keys = kb.waitKeys(keyList=["space", "escape"], waitRelease=True)
# Handle the pressed key
# this code handle the process, since it is waitkeys, it is not going to the next stage untill one of the requested keys is pressed
# by clicking on the 'space' it will execute the rest of the code
# the f.close will save the written file to that point
if 'escape' in [key.name for key in keys]:
    escape_experiment()
    
# generating the timer for the start of the experiment
# this is generated to show the time each stimuli was presented relative to this
start_time = core.getTime()

#-----before experiment fixation cross------------------------------------------------------------------------------------------------------------------

# generating the fixation cross stimuli
fixation_stimuli = visual.TextStim(win, "+", pos=(0,0), wrapWidth=1800, color = (1,1,1), height=60)

# using range and frame-based timing for showing this
for i in range (300 * refresh_rate_normalized): # this is 5 seconds for a screen with customized referesh rate but the default is for 60 HZ
    # waitrelease set to false since we want immediate stop
    keys = kb.getKeys(['escape'], waitRelease=False)
    for key in keys:
        if 'escape' in key.name:
            escape_experiment()
    fixation_stimuli.draw()
    win.flip()

#-----running the part related to blocks and trials-----------------------------------------------------------------------------------------------------

# defining the list of blocks based on their names in the trials.csv file
block_list = data_set['Condition'].unique()
block_list = list(block_list)
print(block_list)
# block_list = ["colour","size"]
# "high" , "low" , "shape" , "size" , "texture"
# defining the number of trials. 10 trial for each block
num_conditions = data_set['Condition'].nunique()
trial_num_total = len(data_set)
trial_num_per_condition = trial_num_total // num_conditions
trial_num_list = []
for i in range(trial_num_per_condition):
    trial_num_list.append(i)
print(trial_num_list)
# trial_num = [0,1,2,3,4,5,6,7,8,9]
# shuffling both blocks and trials to randomizing them
np.random.shuffle(block_list)
np.random.shuffle(trial_num_list)
# finding the index of columns.
condition_num = data_set.columns.get_loc("Condition")
target_num = data_set.columns.get_loc("Target")
word_1_num = data_set.columns.get_loc("Word1")
word_2_num= data_set.columns.get_loc("Word2")
word_3_num = data_set.columns.get_loc("Word3")
correct_num = data_set.columns.get_loc("Correct")
# making a block counter to identify the first and final blocks
block_counter = 0
# start the process of stimulus presentation based on shuffled blocks and trials
for index, i in enumerate(block_list):
    # increases with one number for each run of iteration
    block_counter = block_counter + 1
    # compute the start time, it is the time when the each block started to work
    # Generating the dataset according to our current block
    # mask will be created based on rows where the condition column is the same as our current block stimuli
    current_mask = data_set["Condition"] == i
    # applying this mask to create a new and temporary dataset which is in accordance with the current block and changes in each iteration
    data_set_block = data_set[current_mask]
    # writing the text for the instruction of the current block
    experiment_begin_text = (
                            "The experiment is about to begin \n\n"
                            f"In the next block choose the word that has a similar\n {i}\n\n"
                            "Get READY!")
    # generating the text-based stimuli for instruction of the first block since for other blocks it will be shown at the end of the previous block
    instruction_stim = visual.TextStim(win, text = experiment_begin_text, pos=(0,0), color = (1,1,1), height=60)
    # the reason that we used block_counter is to show the instruction here only for the first block
    # for the next blocks, this instruction will be shown in the end off the previous block
    for time in range(300 * refresh_rate_normalized):
        if block_counter == 1:
            keys = kb.getKeys(['escape'], waitRelease=False)
            for key in keys:
                if 'escape' in key.name:
                    escape_experiment()
                
            instruction_stim.draw()
            win.flip()
        else:
            continue
    # getting stimuli for each trial based on the masked dataset within that block    
    for j in trial_num_list:
        # extracting the stimuli
        # here we are calling different columns of each row using their indices
        condition = data_set_block.iloc[j,condition_num]
        target = data_set_block.iloc[j,target_num]
        word_1 = data_set_block.iloc[j,word_1_num]
        word_2 = data_set_block.iloc[j,word_2_num]
        word_3 = data_set_block.iloc[j,word_3_num]
        correct = data_set_block.iloc[j,correct_num]
        # generating the stimuli for display
        target_stim = visual.TextStim(win, f"{target}", pos=(0,200), color = (1,1,1), height=60)
        condition_stim = visual.TextStim(win, f"{condition}", pos=(0,0), color = (1,1,1), height=40)
        word_1_stim = visual.TextStim(win, f"{word_1}", pos=(-300,-200), color = (1,1,1), height=60)
        word_2_stim = visual.TextStim(win, f"{word_2}", pos=(0,-200), color = (1,1,1), height=60)
        word_3_stim = visual.TextStim(win, f"{word_3}", pos=(300,-200), color = (1,1,1), height=60)
        # generating stimuli using draw
        target_stim.draw()
        condition_stim.draw()
        word_1_stim.draw()
        word_2_stim.draw()
        word_3_stim.draw()
        # resetting the kb clock prior to showing each trial to capture the unique reaction time of each trial
        kb.clock.reset()
        # flipping the window to show the trial
        win.flip()
        # the time when a trial is shown according to the start timepoint
        Time = core.getTime() - start_time
        # waiting for subject to press accepted keys within 10 seconds
        keys = kb.waitKeys(keyList = ["1" , "2" , "3" , "escape"], maxWait = 10.0)
        # if subject pressed any accepted key
        if keys:
            for key in keys:
                # if the subject presses escape, it will close the experiment and save the results
                if 'escape' in key.name:
                    escape_experiment()
                # if the subject presses any of the related keys to the experiment it will get the response, reaction time, and correctness   
                elif any(i in key.name for i in ["1", "2", "3"]):
                    response = key.name
                    RT = key.rt
                    # This part cheks if the given response is the same as the correct response which was given in the trials.csv
                    if response == str(correct):
                        IsCorrect = "1"
                    else:
                        IsCorrect = "0"
                    # this part will write the results in the file of participant's response
                    with open(filename, 'a') as f:
                        f.write(f'{condition},{target},{word_1},{word_2},{word_3},{response},{correct},{RT},{IsCorrect},{Time:.03f}\n')
                    break
        # if the participant does not give any response after 10 seconds,
        # the reaction time, response, and correctness will be saved to the file as follows:
        else:
            RT = "NaN"
            response = ""
            IsCorrect = ""
            with open(filename, 'a') as f:
                f.write(f'{condition},{target},{word_1},{word_2},{word_3},{response},{correct},{RT},{IsCorrect},{Time:.03f}\n')
        # generating a random interval of fixation cross between trials for 0.5 to 2.5 seconds
        # generating the fixation cross stimuli
        text_interval = visual.TextStim(win, "+", pos=(0, 0), color=(1, 1, 1), height=60)
        # generating a random number between -0.5 and -2.5
        random_time = np.random.uniform(-0.5,-2.5)
        # reseting stimuli_clock to 0
        stimuli_clock.reset()
        # turning stimuli clock back in time according to the generated random time interval
        stimuli_clock.addTime(random_time)
        # showing the fixation interval according to the random time interval
        while stimuli_clock.getTime() < 0:
            keys = kb.getKeys(['escape'], waitRelease=False)
            for key in keys:
                if 'escape' in key.name:
                    escape_experiment()
            text_interval.draw()
            win.flip()
    # defining a random time for time interval between blocks
    between_block_time_interval = np.random.uniform(-7.5,-12.5)
    # break the time into halves
    between_block_time_interval_in_half = between_block_time_interval / 2
    # generating the between-block stimuli
    first_half_text = (
                        "Take a short break, but please pay attention to the screen.\n\n"
                        "The experiment is going to start again in a few seconds")
    # finding the name of the next block from the block_list based on its index
    if index != (len(block_list) - 1):
        next_block = block_list[index + 1]
    # generate the stimuli for the instruction of the next block which will be shown in the second half
    second_half_text = (
                            "The experiment is about to begin \n\n"
                            f"In the next block choose the word that has a similar\n {next_block}\n\n"
                            "Get READY!")
    # generating the text_based stimuli for the between-block intervals
    first_half_stimuli = visual.TextStim(win, text = first_half_text ,wrapWidth=1800, pos=(0, 0), color=(1, 1, 1), height=60)
    second_half_stimuli = visual.TextStim(win, text = second_half_text ,wrapWidth=1800, pos=(0, 0), color=(1, 1, 1), height=60)
    # resetting and setting the time for the first half of the time interval  
    stimuli_clock.reset()
    stimuli_clock.addTime(between_block_time_interval_in_half)
    # showing the first half. the block_counter part is to not showing this between block intervals for the last block 
    while stimuli_clock.getTime() < 0 and block_counter != len(block_list):
        keys = kb.getKeys(['escape'], waitRelease=False)
        for key in keys:
            if 'escape' in key.name:
                escape_experiment()
        first_half_stimuli.draw()
        win.flip()
    # resetting and setting the time for the second half of the time interval
    stimuli_clock.reset()
    stimuli_clock.addTime(between_block_time_interval_in_half)
    # showing the first half. The block_counter part is to not showing this between block intervals for the last block
    while stimuli_clock.getTime() < 0 and block_counter != len(block_list):
        keys = kb.getKeys(['escape'], waitRelease=False)
        for key in keys:
            if 'escape' in key.name:
                escape_experiment()
        second_half_stimuli.draw()
        win.flip()

#-----final thank you message after the end of all blocks and their trials-----------------------------------------------------------------------------

# generating the text_based stimuli
thank_you_message = visual.TextStim(win, "Thanks for your participation" , pos=(0, 0), color=(1, 1, 1), height=60)
# resetting and setting the time
stimuli_clock.reset()
stimuli_clock.addTime(-5)
while stimuli_clock.getTime() < 0:
    keys = kb.getKeys(['escape'], waitRelease=False)
    for key in keys:
        if 'escape' in key.name:
            escape_experiment()
    thank_you_message.draw()
    win.flip()

win.close()
core.quit()