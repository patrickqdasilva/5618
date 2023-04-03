import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

def spike_gen_single(freq, total_time):
    """
    Use:
        Probabilistically Generate a single spike train given a frequency
    Param:
        freq: firing frequency of a neruon
        total_time: total simulation time
    Return:
        list with the time in the index where a neuron spiked
    """
    # empty matrix of size total time
    spike_mat = [0] * total_time
    # return a time series with spike times for one neruon
    for idx, time in enumerate(range(0,total_time,1)):
        # the nueron "spikes" if this condition is true
        if np.random.rand() < freq*(1/60):
            spike_mat[idx] = time
    return spike_mat

def spike_gen_allplot(tuning_df, total_time, directions):
    data = []
    # generate the spike trains for each neuron at each direction
    for direction in directions:
        spike_trains = {}
        for neuron_idx in range(8):
            spike_trains[neuron_idx] = spike_gen_single(tuning_df[direction][neuron_idx], total_time)
        data.append(spike_trains)
    return data


def plot_spikes(all_spikes, directions):
    """
    Use:
        plot up to 8 Spike Train Raster Plots depending on how many were generated
    """
    # Set parameters for Raster Plot
    colors1 = [f'C{i}' for i in range(8)]
    lineoffsets1 = [x for x in range(1,9)]
    linelengths1 = [0.5 for x in range(8)]

    fig, ax = plt.subplots(nrows=2, ncols=4, figsize=(15, 10), dpi=80)
    ax[0][0].set_ylabel('Neuron')
    ax[1][0].set_ylabel('Neuron')
    fig.suptitle('Spike Train Raster Plots')
    count = 0
    for i in range(2):
        for j in range(4):
            if count < len(directions):
                # get data in correct format
                res = []
                for val in all_spikes[count].values():
                    res.append(val)
                # Draw a spike raster plot for each direction
                ax[i][j].eventplot(res, colors=colors1, lineoffsets=lineoffsets1, linelengths=linelengths1)    
                ax[i][j].set_title(f'{directions[count]} degrees')
                ax[i][j].set_xlabel('Time in msec')
                count += 1
    plt.show()

def binarizer(li):
    """
    Param:
        li: list with spike timings
    Return:
        0 when li == 0
        1 when li > 0
    """
    return (np.array(li) > 0)*1.0

def spike_gen_input(tuning_df, total_time, directions):
    """
    Use:
        generate input for the forward pass of the feed forward neural network
    Param:
        tuning_df: dataframe with frequencies of neurons at each direction
        total_time: total simulation time in msec
        directions: list of the angles of dot movement from simulation
    Returns:
        X: batched sum of spike timings ready to be input through model - shape [len(directions), 8]
        y: labels of spike timings at each direction - shape [len(directions),]
    """

    X = []
    y = []

    # generate the spike trains for each neuron in the directions determine by ball moving
    for direction in directions:
        # individual sum of spike timings for each neuron - shape [8,]
        spike_trains = []
        for neuron_idx in range(8):
            # append the scores of each neuron individually
            spike_trains.append(sum(binarizer(spike_gen_single(tuning_df[direction][neuron_idx], total_time))))
        # append all 8 neurons to the list of spike timings
        X.append(spike_trains)
        y.append(direction)

    return X, y