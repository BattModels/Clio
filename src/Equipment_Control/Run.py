import os
import sys

from datetime import datetime
from collections import deque
from time import sleep
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)
from Database.TypeFunctions import verifyCompositionID
from Database.Pipeline import insert_new_data
import logging
id_queue = deque()

try:
    
    from Experiment import *
    from MixingSolver import verifyCompositionIDInside, pulp_solve_sorted
    from CandidateManager import *
    from Email import send_email
    from Utils import *
except ImportError as e:
    from .Experiment import *
    from .MixingSolver import verifyCompositionIDInside, pulp_solve_sorted
    from .CandidateManager import *
    from .Email import send_email
    from .Utils import *



def run(compositionID, log_file, trial=1):
    log_file_name = log_file
    try:
        candidate_pos = -1
        candidate_list = get_candidate_list()
        candidate_pos =  len(candidate_list) + 1
        composition = verifyCompositionIDInside(compositionID)
        start_time = datetime.now().replace(microsecond=0)
        if not log_file_name:
            log_file_name = start_time.strftime("%Y-%m-%d %H-%M-%S") + ".log"
        result = experiment(compositionID, pulp_solve_sorted(compositionID, prime=PRIME_VOLUME_VALVE + SONICATOR_TUBE_VOLUME, total_volume=TOTAL_VOLUME), candidate_pos, log_file_name, trial_num=trial, close=True)
        if result['Conductivity'] > CONDUCTIVITY_CUTOFF and result['Viscosity'] < VISCOSITY_CUTOFF:
            add_candidate(compositionID)
            candidate_list.append(compositionID)
            if len(candidate_list) < NUM_END:
                email_string =  f'{compositionID} is saved into candidate bottle {candidate_pos}. \nOther candidates:'
            else:
                email_string =  f'{compositionID} is saved into candidate list. \nOther candidates:'
            for i in range(len(candidate_list)):
                email_string += f'\n{candidate_list[i]}'
            send_email('Clio found a good candidate!', email_string)
            if len(candidate_list) == NUM_END:
                send_email('Clio runs into an error', 'No spaces for candidates')
        result['Date'] = start_time
        result['Trial'] = trial
        composition['experiments'] = result
        #raise BufferError('Please ignore this email')
        insert_new_data(composition)
        log_file_name = None
        return "No errors"
    except Exception as e:
        send_email('Clio runs into an error', str(e))
        initialize(log_file_name)
        return str(e)
        
    
def zero(log_file):
    global log_file_name
    log_file_name = log_file
    try:
        zeroVis(log_file_name)
        clean_up(log_file_name)
        #sleep(60)
        return "No errors"
    except Exception as e:
        send_email('Clio runs into an error', str(e))
        return str(e)
    
def halt(log_file):
    formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
    formatted_time += ' - ERROR - '
    with open(os.path.join(current_dir, '..', 'Logs', log_file), 'a') as file:
        file.write(formatted_time + "Experiment Halted. All equipment closed" + '\n')
    terminate()

def add_to_queue(compositionID):
    result = verifyCompositionID("", compositionID)
    if isinstance(result, str):
        return result
    id_queue.extend([compositionID])
    return "No errors"

def add_bulk_to_queue(compositionIDs):
    for i in range(len(compositionIDs)):
        result = verifyCompositionID("", compositionIDs[i])
        if isinstance(result, str):
            return f'Invalid ID on line {i + 2}'
    id_queue.extend(compositionIDs)
    return "No errors"

def get_queue_length():
    return len(id_queue)

def delete_ith_element(i):
    # Check if the index is within bounds
    if i < 0 or i >= len(id_queue):
        return
    del id_queue[i]
