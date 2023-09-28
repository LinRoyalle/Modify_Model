'''
Program:
    1、Get the data from the sgy file
    2、Add ocean on the data list
    3、Add the abnormal signal into the sgy file including the density file & the velocity file
    4、Save the modified sgy file
History:
    12th Sep 2023 09:16 Royalle
'''

import segyio
import numpy as np
from shutil import copyfile
import random
import matplotlib.pyplot as plt

# select sgy file
location = '/home/hlyin/Artificial/DataSets/'
origin_vel_sgyfile = location + 'MODEL_P-WAVE_VELOCITY_1.25m.segy'
origin_den_sgyfile = location + 'MODEL_DENSITY_1.25m.segy'

# # the layer of ocean water put on the original data
# ocean_density = 1025
# ocean_deep = 160
# ocean_part = ocean_density * np.ones(ocean_deep)

# initialization list && open the original sgy file
data_vel_list = []
data_den_list = []
with segyio.open(origin_vel_sgyfile, 'r') as vel_src:
    for iv in range(len(vel_src.trace)):
        test_vel = 1500 * np.ones(2801,)# TEST THE PARAMETER
        data_vel_list.append(test_vel)
        # z = np.concatenate((ocean_part, f.trace[i]), axis=0)
    vel_src.close()
with segyio.open(origin_den_sgyfile, 'r') as den_src:
    for id in range(len(den_src.trace)):
        test_den = 1.0099993 * np.ones(2801,)
        # TEST THE PARAMETER
        data_den_list.append(test_den)
    den_src.close()


# add the abnormal signal into the sgy-file
abnormal_model_num = 1
for im in range(abnormal_model_num):
    ''' Create the new segy file'''
    copy_vel_sgyfile = location + 'new model/velocity/' + 'MODEL_VELOCITY_TEST' + str('%03d' % (im+1)) + '.segy'
    copy_den_sgyfile = location + 'new model/density/' + 'MODEL_DENSITY_TEST' + str('%03d' % (im+1)) + '.segy'
    copyfile(origin_vel_sgyfile, copy_vel_sgyfile)
    copyfile(origin_den_sgyfile, copy_den_sgyfile)
    ''' Parameter of expected signal'''
    iron_speed = 5120
    air_speed = 330
    iron_density = 7.874          # unit = t/m3
    air_density = 0.001293        # unit = t/m3
    zaxis = 13601
    xaxis = 2801
    iron_length = 12500             # unit = m
    iron_width = 2500               # unit = m
    air_length = 8000               # unit = m
    air_width = 2000               # unit = m
    iron_z1_loc = 1800                                 # random.randint(2, zaxis - (iron_length / 1.25) - 2)
    iron_x1_loc = 400                                # random.randint(2, xaxis - (iron_width / 1.25) - 2)
    iron_z2_loc = iron_z1_loc + int(iron_length / 1.25)
    iron_x2_loc = iron_x1_loc + int(iron_width / 1.25)
    air_z1_loc = iron_z1_loc + int((iron_length - air_length) / 2 / 1.25)
    air_x1_loc = iron_x1_loc + int((iron_width - air_width) / 2 / 1.25)
    air_z2_loc = air_z1_loc + int(air_length / 1.25)
    air_x2_loc = air_x1_loc + int(air_width / 1.25)
    for ir in range(iron_z1_loc, iron_z2_loc):
        (data_vel_list[ir])[iron_x1_loc:iron_x2_loc] = iron_speed
        (data_den_list[ir])[iron_x1_loc:iron_x2_loc] = iron_density
    for ia in range(air_z1_loc, air_z2_loc):
        (data_vel_list[ia])[air_x1_loc:air_x2_loc] = air_speed
        (data_den_list[ia])[air_x1_loc:air_x2_loc] = air_density

    # change the sgy data && save the sgy file as a new file
    with segyio.open(copy_vel_sgyfile, 'r+') as vel_cpf:
        for icv in range(len(vel_cpf.trace)):
            vel_cpf.trace[icv] = data_vel_list[icv]
        vel_cpf.close()

    with segyio.open(copy_den_sgyfile, 'r+') as den_cpf:
        for icd in range(len(den_cpf.trace)):
            den_cpf.trace[icd] = data_den_list[icd]
        den_cpf.close()

    print('Create ' + ' MODEL_VELOCITY_' + str('%03d' % (im+1)) + '.segy' + '\n')
    print('Create ' + ' MODEL_DENSITY_' + str('%03d' % (im+1)) + '.segy' + '\n')

# Test the saved sgy file && check the data
test_list = []
with segyio.open(copy_vel_sgyfile, mode='r') as test:
    for i in range(len(test.trace)):
        test_list.append(test.trace[i])

# 转为矩阵
data_numpy = np.array(test_list)
data_numpy = data_numpy.T

# plt.pcolor(data_numpy,cmap = 'jet')
plt.contourf(data_numpy, cmap = 'jet')
plt.colorbar()
plt.xlabel('position[m]')
ax = plt.gca()
# ax.xaxis.set_ticks_position('top')
ax.invert_yaxis()
ax.xaxis.tick_top()
plt.show()


