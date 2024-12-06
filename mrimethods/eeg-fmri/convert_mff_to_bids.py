#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 17:53:58 2023

@author: lj
"""

import os.path as op
#import shutil

import mne
import mne_bids

import matplotlib.pyplot as plt

import copy

import numpy as np
import ast

# use qt for matplotlib
# matplotlib.use('Qt5Agg')

subject_id = 'BHBMEG004'
weight = (56.699)

n_mr_runs = 8
n_eeg_runs = 8
tr  = 2
# enter the name(s) of the eeg file(s)
mff_fname = ["BHBMEG004_20190507_024832.mff", #MR run 3 rest eyes closed
             "BHBMEG004_20190507_025512.mff", #MR run 4 rest eyes closed
             #"BHBMEG004_20190507_030218.mff", #
             #"BHBMEG004_20190507_030358.mff", #
             "BHBMEG004_20190507_030548.mff", #MR run 5 rest eyes closed
             "BHBMEG004_20190507_030917.mff", #MR run 6 rest eyes closed
             "BHBMEG004_20190507_032039.mff", #MR run 7 rest eyes closed
             "BHBMEG004_20190507_032736.mff", #MR run 10 rest eyes closed
             "BHBMEG004_20190507_032910.mff", #MR run 11 rest eyes closed
             #"BHBMEG004_20190507_033145.mff", #
             #"BHBMEG004_20190507_033222.mff", # 
             "BHBMEG004_20190507_033707.mff"] #MR run 12 rest eyes closed

# get data directory
data_path = op.join("/", "Users", "lj", "data", "BIDS")
sourcedata_path = op.join(data_path, subject_id, "sourcedata", "eeg", "old")


# DO NOT CHANGE BELOW HERE

def write2bids(raw, tmin, tmax, subject_id, run, out_path, mff_fname, montage, event_id, mr_to_eeg):
    raw01 = copy.deepcopy(raw)
    
    if tmin != raw01.tmin and tmax != raw01.tmax:
        raw01.crop(tmin = tmin, tmax = tmax)
    
    events01 = mne.find_events(raw01)
    
    
    bids_path1 = mne_bids.BIDSPath(subject = subject_id,
              task = 'rest',
              run = int(mr_to_eeg[run]),
              suffix = 'eeg',
              datatype = 'eeg',
              root = out_path,
              space = 'fsaverageSym')


    mne_bids.write_raw_bids(raw01, 
                        bids_path = bids_path1,
                        events = events01,
                        event_id = event_id,
                        format = 'EDF',
                        allow_preload = True,
                        montage = montage,
                        acpc_aligned = True,
                        overwrite = True)
    
    return print('Finished!')


# if n_eeg_runs is less than the number n_mr_runs, label which mr runs go with which eeg run.
mr_to_eeg = {}
for run in range(n_eeg_runs):
     mr_to_eeg[run] = ast.literal_eval(
         input("MR runs in EEG run {:02d} (e.g., [1,2,3,4,5]. Include the square brackets)?".format(run + 1))
         ) 
     mr_to_eeg[run] = [x -1 for x in mr_to_eeg[run]]


for run, mff in enumerate(mff_fname):
    raw_fname = op.join(sourcedata_path, mff)

    # get path to the directory where the data should go
    out_path = op.join("/", "Volumes", "GrosDisque", "BHBMEG", subject_id)

    # Uncomment if you want to delete the BIDS root directory
    #if op.exists(out_path):
    #    shutil.rmtree(bids_root)
        
    subj_path = op.join(out_path, "sub-" + subject_id)


    # read in EEG data from .mff file
    raw = mne.io.read_raw_egi(raw_fname, 
                          eog = None, 
                          preload=True, 
                          channel_naming = 'EEG %03d')
    # add in power line frequency (in Hz)
    raw.info['line_freq'] = 60
    # add in details about our subject
    raw.info['subject_info'] = {
        "his_id" : subject_id,
        "weight" : weight, # in kg
        "sex" : 2, # female
        "hand"  : 1 # right
        }
    # Set initial reference channel to Cz
    raw.set_eeg_reference(ref_channels = ['VREF']) # Cz

    # find the events to plot to find cutoff points for each run
    events = mne.find_events(raw)
    event_dict = {
        "TR" : 1
        }

    # get the montage for all runs
    #montage = mne.channels.read_dig_egi(
    #    op.join(
    #        raw_fname, 
    #        "coordinates.xml"))
    montage = mne.channels.make_standard_montage('GSN-HydroCel-257')
    montage.plot()

    # rename the channels so that the montage and channel names match
    mapping = dict(zip(raw.info['ch_names'],montage.ch_names))
    raw.rename_channels(mapping = mapping)
    raw.set_montage(montage)
    
    raw.plot_sensors()
    
    # plot events
    mne.viz.plot_events(events, 
                        raw.info['sfreq'],
                        event_id = event_dict)
    plt.show()

    # Pause to record break points in .mff file
    print('Tmin for the EEG run is: ' + str(raw.tmin))
    print('Tmax for the EEG run is: ' + str(raw.tmax))
    
    tmin = []
    tmax = []
    if n_mr_runs == n_eeg_runs:
        tmin = [raw.tmin]
        tmax = [raw.tmax]
    else:
        tmin.append(ast.literal_eval(input("Enter tmin for mri in eeg run " + str(run + 1) + ": "))) 
        tmax.append(ast.literal_eval(input("Enter tmax for mri in eeg run " + str(run + 1) + ": "))) #486

    # if data has only 1 run
    # crop data into N runs corresponding to the fmri data
    # note to self, turn this into a function

    # Run 1
    length = [0]
    if n_eeg_runs == n_mr_runs:
        #for run in range(n_eeg_runs):
        write2bids(raw = raw, tmin = tmin[run], tmax = tmax[run], subject_id = subject_id, run = run, out_path = out_path, mff_fname = mff_fname, montage = montage, event_id = event_dict, mr_to_eeg = mr_to_eeg)
    elif n_eeg_runs < n_mr_runs:
        for eeg_run in range(len(mr_to_eeg)):
            if length == 1:
                write2bids(raw = raw, tmin = tmin[0 + length], tmax = tmax[0 + length], subject_id = subject_id, run = run, out_path = out_path, mff_fname = mff_fname, montage = montage, event_id = event_dict, mr_to_eeg = mr_to_eeg)   
            else:
                write2bids(raw = raw, tmin = tmin[0 + length[-1] - 1], tmax = tmax[0 + length[-1] - 1], subject_id = subject_id, run = run, out_path = out_path, mff_fname = mff_fname, montage = montage, event_id = event_dict, mr_to_eeg = mr_to_eeg)
                for mr_run in range(1, len(mr_to_eeg[eeg_run])):
                    mr_run = mr_run + length[-1] - 1
                    write2bids(raw = raw, tmin = tmin[run], tmax = tmax[run] + 0.001, subject_id = subject_id, run = run, out_path = out_path, mff_fname = mff_fname, montage = montage, event_id = event_dict, mr_to_eeg = mr_to_eeg)
                length.append = len(mr_to_eeg[eeg_run])    
            

# Run 2
#write2bids(raw = raw, tmin = tmax1 + 0.001, tmax = tmax2, subject_id = subject_id, run = '02', out_path = out_path, mff_fname = mff_fname, montage = montage, event_id = event_dict)


# Run 3
#write2bids(raw = raw, tmin = tmax2 + 0.001, tmax = None, subject_id = subject_id, run = '03', out_path = out_path, mff_fname = mff_fname, montage = montage, event_id = event_dict)


