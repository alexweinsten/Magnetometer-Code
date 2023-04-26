
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
from math import remainder
import os
import glob



filepath = os.getcwd()
list_of_files = glob.glob(os.path.join(filepath,'*mag_file.csv'))
latest_file = max(list_of_files, key=os.path.getctime)

#read in csv and create arrays
df = pd.read_csv(latest_file)

x_val = df['x'].values
y_val = df['y'].values
z_val = df['z'].values


#plotting raw data
x = x_val
y = y_val
z = z_val

fig = plt.figure()
ax = plt.axes(projection ='3d')

ax.plot3D(x, y, z, 'green')
ax.set_title('X vs. Y vs. Z Magnetic Field Raw Data')
ax.set_xlabel('x (Gauss)')
ax.set_ylabel('y (Gauss)')
ax.set_zlabel('z (Gauss)')
plt.show()

#plot each a diff color
total_time = 5
time_stamp = np.linspace(0,total_time, len(z_val))
plt.plot(time_stamp, x_val, label = "x: avg = {}".format(np.nanmean(x_val)))
plt.axhline(y=np.nanmean(x_val), color='red', linestyle='--', linewidth=0.75)
plt.plot(time_stamp, y_val, label = "y: avg = {}".format(np.nanmean(y_val)))
plt.axhline(y=np.nanmean(y_val), color='red', linestyle='--', linewidth=0.75)
plt.plot(time_stamp, z_val, label = "z: avg = {}".format(np.nanmean(z_val)))
plt.axhline(y=np.nanmean(z_val), color='red', linestyle='--', linewidth=0.75)
plt.title("Magnetic Field vs. Time Raw Data")
plt.xlabel("Time (seconds)")
plt.ylabel ("Magnetic Field (Gauss)")
plt.legend()
plt.show()


#remove outliers
x_outliers = []
y_outliers = []
z_outliers = []
    
threshold = 2

x_mean = np.mean(x_val)
y_mean = np.mean(y_val)
z_mean = np.mean(z_val)

x_std = np.std(x_val)
y_std = np.std(y_val)
z_std = np.std(z_val)

if x_std != 0:
    for i in x_val:
        z_score = (i-x_mean)/x_std
        if np.abs(z_score) > threshold:
            x_outliers.append(i)

if y_std != 0:
    for i in y_val:
        z_score = (i-y_mean)/y_std
        if np.abs(z_score) > threshold:
            y_outliers.append(i)

if z_std != 0:
    for i in z_val:
        z_score = (i-z_mean)/z_std
        if np.abs(z_score) > threshold:
            z_outliers.append(i)


x_clean = x_val[2:-2]
y_clean = y_val[2:-2]
z_clean = z_val[2:-2]

for i in range(len(x_clean)):
    if x_clean[i] in x_outliers:
        x_clean[i] = (x_clean[i+1]+x_clean[i-1])/2
    if y_clean[i] in y_outliers:
        y_clean[i] = (y_clean[i+1]+y_clean[i-1])/2
    if z_clean[i] in z_outliers:
        z_clean[i] = (z_clean[i+1]+z_clean[i-1])/2


#plotting the outlier removed data 

x = x_clean
y = y_clean
z = z_clean 

fig = plt.figure()
ax = plt.axes(projection ='3d')

ax.plot3D(x, y, z, 'green')
ax.set_title('X vs. Y vs. Z Magnetic Field with Outliers Removed')
ax.set_xlabel('x (Gauss)')
ax.set_ylabel('y (Gauss)')
ax.set_zlabel('z (Gauss)')
plt.show()
#plot each a diff color

total_time = 5 
time_stamp = np.linspace(0,total_time, len(z_clean))
plt.plot(time_stamp, x_clean, label = "x: avg = {}".format(np.nanmean(x_clean)))
plt.axhline(y=np.nanmean(x_clean), color='red', linestyle='--', linewidth=0.75)
plt.plot(time_stamp, y_clean, label = "y: avg = {}".format(np.nanmean(y_clean)))
plt.axhline(y=np.nanmean(y_clean), color='red', linestyle='--', linewidth=0.75)
plt.plot(time_stamp, z_clean, label = "z: avg = {}".format(np.nanmean(z_clean)))
plt.axhline(y=np.nanmean(z_clean), color='red', linestyle='--', linewidth=0.75)
plt.title('Magnetic Field vs. Time with Outliers Removed')
plt.xlabel("Time (seconds)")
plt.ylabel ("Magnetic Field (Gauss)")
plt.legend()
plt.show()


#averaging over every n elements to form smaller array 

rem_arr = len(x_clean) % 5 

if rem_arr != 0:
    x_clean_reduced = x_clean[:-rem_arr]
    y_clean_reduced = y_clean[:-rem_arr]
    z_clean_reduced = z_clean[:-rem_arr]
else: 
    x_clean_reduced = x_clean
    y_clean_reduced = y_clean
    z_clean_reduced = z_clean

x_clean_avg = np.average(x_clean_reduced.reshape(-1, 5), axis=1)
y_clean_avg = np.average(y_clean_reduced.reshape(-1, 5), axis=1)
z_clean_avg = np.average(z_clean_reduced.reshape(-1, 5), axis=1)

x = x_clean_avg
y = y_clean_avg
z = z_clean_avg

fig = plt.figure()
ax = plt.axes(projection ='3d')

ax.plot3D(x, y, z, 'green')
ax.set_title('X vs. Y vs. Z Magnetic Field with 5-Point Averages of Outlier-Removed Data')
ax.set_xlabel('x (Gauss)')
ax.set_ylabel('y (Gauss)')
ax.set_zlabel('z (Gauss)')
plt.show()

#plot each a diff color
total_time = 5 
time_stamp = np.linspace(0,total_time, len(z_clean_avg))
plt.plot(time_stamp, x_clean_avg, label = "x: avg = {}".format(np.nanmean(x_clean_avg)))
plt.axhline(y=np.nanmean(x_clean_avg), color='red', linestyle='--', linewidth=0.75)
plt.plot(time_stamp, y_clean_avg, label = "y: avg = {}".format(np.nanmean(y_clean_avg)))
plt.axhline(y=np.nanmean(y_clean_avg), color='red', linestyle='--', linewidth=0.75)
plt.plot(time_stamp, z_clean_avg, label = "z: avg = {}".format(np.nanmean(z_clean_avg)))
plt.axhline(y=np.nanmean(z_clean_avg), color='red', linestyle='--', linewidth=0.75)
plt.title('Magnetic Field vs. Time with 5-Point Averages of Outlier-Removed Data')
plt.xlabel("Time (seconds)")
plt.ylabel ("Magnetic Field (Gauss)")
plt.legend()
plt.show()


