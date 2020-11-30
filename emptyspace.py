#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import glob
import random as rand
import numpy as np

coords=glob.glob("../*.lmp")
runs = 10
trajs = 100
VDWfactor = 1

radii = {'H':[1.20],
         'HE':[1.40],
         'LI':[1.82],
         'BE':[1.53],
         'B':[1.92],
         'C':[1.70],
         'N':[1.55],
         'O':[1.52],
         'F':[1.47],
         'NE':[1.54],
         'NA':[2.27],
         'MG':[1.73],
         'AL':[1.84],
         'SI':[2.10],
         'P':[1.80],
         'S':[1.80],
         'CL':[1.75],
         'AR':[1.88],
         'BR':[1.85]
        }

def Unitless(lista, listb):
    distance = (np.linalg.norm([lista[j-1]-float(listb[j]) for j in [1,2,3]]))/(radii[listb[0]][0])
    if distance <= VDWfactor:
        return True
    elif distance > VDWfactor:
        return False

for coord in coords:
    readin = open(coord, "r")
    readin2 = readin.readlines()[:30000 * trajs]
    print(len(readin2))
    readin.close()
    SystemSize = int(readin2[3])
    hits = 0
    misses = 0
    bound = float(readin2[5].split()[1])
    volume = bound**3
    proportion = 0
    freespace = 0
    probe = [0,0,0]

    #First wrap the trajectory, and convert to a usable format
    for i in range(trajs):
        for k in range((SystemSize+9)*i + 9, (SystemSize+9)*(i+1)):
            for l in range(1,3):
                if float(readin2[k].split()[l]) < 0:
                    problem = float(readin2[k].split()[l])
                    while problem < 0:
                        problem = problem + bound
                    readin2[k] = readin2[k].split()
                    readin2[k][l] = str(problem)
                    readin2[k] = ' '.join(readin2[k]) + ' \n'
                elif float(readin2[k].split()[l]) > bound:
                    problem = float(readin2[k].split()[l])
                    while problem > bound:
                        problem = problem - bound
                    readin2[k] = readin2[k].split()
                    readin2[k][l] = str(problem)
                    readin2[k] = ' '.join(readin2[k]) + ' \n'
    
    #Now probe
    for m in [1,10,50,100,200,500]:
        for j in range(m):
            for i in range(trajs):
                probe = [ bound*rand.random() for x in range(3)]
                hit = False
                for k in range((SystemSize+9)*i + 9, (SystemSize+9)*(i+1)):
                    splut = readin2[k].split()
                    if Unitless(probe,splut):
                        hit = True
                        hits += 1
                        break
                if not(hit):
                    misses += 1

        proportion =  float(misses/(misses + hits))
        freespace = proportion*volume

        output = open(str(trajs) + 't' + str(m) + 'results.out', "w")
        output.write('From ' + str(int(hits + misses)) + ' samples \n')
        output.write('There were ' + str(hits) + ' hits and ' + str(misses) + ' misses \n')
        output.write('Proportion is ' + '%.5f' % (proportion) + ' meaning free space is ' + '%.5f' % (proportion*volume) + ' A^3 \n')

