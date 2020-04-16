# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 21:11:28 2020

@author: Seb Wilkes
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, colors
import winsound
import time

'''define starting parameters'''

number = int(100) #Starting Number of Particles
#Now we generate the particles as required
#Their label is their value - 1
table = np.arange(1,(number**2)+1, 1) 
decay_probability = 0.03
print("λ = " + str(decay_probability * len(table)))
#Graph colour settings
CMAP = colors.ListedColormap(['#d68213', '#7413eb'])
bounds = [0, 0.5, 1]
NORM = colors.BoundaryNorm(bounds, CMAP.N)
#Sound Settings
frequency = 1000 
duration = 250 


def random_pick(sample, p):
    '''This simulation uses a binomial distribution, and then picks, at random
    which particles are the ones that transmute'''
    
    activity  = np.random.binomial(len(sample), p)
    selection = np.random.choice(sample, size = activity, 
                                  replace = False) - 1
    selection.sort()
    
    return selection, activity
    
        
def tick(sample, p):
    '''On each tick, the simulation works out which particles decay'''
    
    particle_track = sample[sample.nonzero()]
    original_count = len(particle_track)
    # print(original_count)
    decayed_particle, activity = random_pick(particle_track, p)
    #This is used to assign the state of 'decay' for the sample

    return decayed_particle, original_count, activity


def particle_update(number_of_measurements, sample, p):
    
    ''' This command runs the "Experiment". The idea is that once the random
    number generator works out how many decay events there will be
    it then will randomly select of the remaining particles to decay;
    this will just be their particle status changing. This step is then 
    repeated until either no particles remain or the number of measurements
    (ticks of the clock) ends'''
    

    decayed_particles, starting_number, activity  = tick(sample, p)
#        print(decayed_particles)
    #print("%d particles decayed in the measurement #%d. Started with %d" % (len(decayed_particles), i, starting_number))
    
    sample[decayed_particles] = False
    remaining_particles = np.count_nonzero(sample)


    return sample, remaining_particles, activity, decayed_particles



def experimental_observation(particle_count, sample, probability):
    
    activity_count = []
    activity_labels = []
    particle_count_record = []
    particle_track = []
    # particle_count_record = [len(sample)]
    
    
    while particle_count > 0:
        
        sample, particle_count, activity, activity_label \
            = particle_update(particle_count,\
                              sample, probability)

        particle_track.append(sample.tolist())
        activity_count.append(activity)
        activity_labels.append(activity_label)
        particle_count_record.append(particle_count)  
        

    
    activity_count = np.asarray(activity_count)
    activity_labels = np.asarray(activity_labels)
    particle_count_record = np.asarray(particle_count_record)
    particle_track = np.asarray(particle_track)
    
    
    return activity_count, activity_labels, \
        particle_count_record, particle_track
        



def animate(i):
    

    title = str("Radioactive decay. Time-count: %d" % (i))
    plt.title(title)
    
    if i == 0:
                
        data = np.ones((number,number))
   
    else: 
        
        data = D[i-1]
    
        data[data>0]=True
                
        data = data.reshape((number,number))
        data = data.transpose()

    if i%5 == 0:
        
        percentage = 100*i/(len(A)+1)
            
        print("Percent complete: "  + str(percentage) + "%")
          
    return plt.imshow(data, cmap=CMAP, norm=NORM)
 

############## Mucking around below, still unfinished #################   
 
A,B,C,D = experimental_observation(number, table, decay_probability)


fig = plt.figure(figsize = (4,4))

plt.xticks([])
plt.yticks([])

anim_time = time.time()

anim = animation.FuncAnimation(fig, animate, frames=len(A)+1, interval=36,
                                repeat=False, blit=False)


anim.save('2D_decay.gif')
winsound.Beep(frequency, duration)
