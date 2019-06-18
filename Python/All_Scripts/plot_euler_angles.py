'''
Title: plot_euler_angles.py
Author: Conor Green
Description: Script to plot euler angles given in main parameters in an animation
Usage: Called through main of Chief_Drone
Version:
1.0 - June 18 2019 - Created
'''

import time

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from transforms3d import taitbryan

def main(flight_data , **kwargs):
    options = {'sleeptime' : .5}
    options.update(kwargs)

    euler_angles = parse_flight_data(flight_data)

    rotation_matricies = handle_angle_data(euler_angles)

    plot_3D(rotation_matricies , options['sleeptime'])

    return

def parse_flight_data(flight_data):
    euler_angles = []

    for dict in flight_data:
        angle_data_t_slice = dict['demo'][2]
        euler_angles.append(angle_data_t_slice)

    return euler_angles

def handle_angle_data(euler_angles ):
    #euler angles = [ [pitch_t0 , roll_t0 , yaw_t0] , [pitch_t1 , roll_t1 , yaw_t1] ...] in degrees

    list_of_rot_mats = []

    for t_slice in euler_angles:
        pitch = np.deg2rad(t_slice[0])
        roll = np.deg2rad(t_slice[1])
        yaw = np.deg2rad(t_slice[2])

        _rotmat = taitbryan.euler2mat(yaw,pitch,roll)

        list_of_rot_mats.append(_rotmat)

    return list_of_rot_mats

def plot_3D(rot_mats , sleeptime):
    fig = plt.figure()
    ax = Axes3D(fig)

    basis = np.array([[1,0,0] , [0,1,0] , [0,0,1]])
    basis = np.transpose(basis)

    for rot_mat_t_slice in rot_mats:
        plt.cla()
        ax.set_xlim([-1.5 , 1.5])
        ax.set_ylim([-1.5 , 1.5])
        ax.set_zlim([-1.5 , 1.5])
        #ax.view_init(0,90)

        for i in range(0,3):
            ax.quiver(0,0,0,rot_mat_t_slice[0] , rot_mat_t_slice[1] , rot_mat_t_slice[2] , length = 1)


        plt.show(block=False)
        plt.draw()
        plt.pause(.001)
        time.sleep(sleeptime)

    return

if __name__ == '__main__':
    pass