
import numpy as np 
import matplotlib.pyplot as plt
import scipy.integrate 
import math
import serial
from serial import Serial
from scipy.fft import fft, ifft, fftfreq, rfft, irfft
import csv


def get_inertial_acceleration(yaw, pitch, roll, ax, ay,az):
    cr = math.cos(math.radians(roll))
    cy = math.cos(math.radians(yaw))
    cp = math.cos(math.radians(pitch))
    sr = math.sin(math.radians(roll))
    sy = math.sin(math.radians(yaw))
    sp = math.sin(math.radians(pitch))


    yawMatrix = np.matrix([
        [cy, -sy, 0],
        [sy, cy, 0],
        [0, 0 ,1]
    ])

    pitchMatrix = np.matrix([
        [cp, 0, sp],
        [0, 1 ,0],
        [-sp, 0, cp]
    ])

    rollMatrix = np.matrix([
        [1, 0, 0],
        [0, cr, -sr],
        [0, sp, cp]
    ])


    
    R = yawMatrix @ pitchMatrix @ rollMatrix
    #must transpose to get from inerital->body to body->inertial
    RT = np.matrix.transpose(R)

    #measured acceleration matrix
    am = np.matrix([
        [ax],
        [ay],
        [az]
    ])

    
    gm = np.matrix([
        [0],
        [0],
        [9.81]
        ])

    # gmr1 = RT @ gm
    # ai1 = RT @ am - gmr1



    gmr2 = R@gm
    ai2 = R@am - gm
    
    return ai2, gmr2




def main():

    #serial setup
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = 'COM10'
    ser.open()


    print("Serial Initialized")
    while(True):
        # data structures initialization
        ai = [] #inertial acceleration
        data = [] # data to be read over serial

        gmr = None
        gmrx = []
        gmry= []
        gmrz = []

        dTlist = []

        x_data = [] #accel data x
        y_data = [] #accel data y
        z_data = [] #accel data z

        rows = []
        fields = ['SAMPLE','ACCELX','ACCELY','ACCELZ', 'MICROSECONDS']
 
        reading = True

        while(reading):
            line = ser.readline().decode('UTF-8')
            line1 = line.rstrip().split()
            print(line1)
            if (line1[0] == 'END'):
                reading = False
            else:
                line1 = list(map(float, line1))
                data.append(line1)

        print("Finished reading")



        for i  in range(len(data)):
            yaw, pitch, roll, accelx, accely, accelz, dT = data[i]
            accelx *= 9.81
            accely *= 9.81
            accelz *= 9.81
            dT /= 1000000
            
            if (dT < 0.01):
                dTlist.append(dT)
            else:
                dT = 0.005

            ai.append(np.empty((3,1)))
            

            # ai[i], gmr = get_inertial_acceleration(yaw, pitch, roll, accelx, accely, accelz)
            ai[i] = np.matrix([
                    [accelx],
                    [accely],
                    [accelz - 9.81]
                ])

            x_data.append(ai[i].item(0,0))
            y_data.append(ai[i].item(1,0))
            z_data.append(ai[i].item(2,0))

            templist = [i,accelx, accely, accelz, dT]
            rows.append(templist)

            # gmrx.append(gmr.item(0,0))
            # gmry.append(gmr.item(1,0))
            # gmrz.append(gmr.item(2,0))


        filename = "data.csv"

        with open(filename, 'w', newline = '') as csvfile:
            csvwriter = csv.writer(csvfile)

            csvwriter.writerow(fields)

            csvwriter.writerows(rows)

        dtavg = np.mean(dTlist)
        print(dtavg)
        
        velx = None
        posx = None
        vely = None
        posy = None
        velz = None
        posz =dtavg



        velx = scipy.integrate.cumtrapz(x_data, dx = dtavg, initial = 0)
        posx = scipy.integrate.cumtrapz(velx, dx = dtavg, initial = 0)

        vely = scipy.integrate.cumtrapz(y_data, dx = dtavg, initial = 0)
        posy = scipy.integrate.cumtrapz(vely, dx = dtavg, initial = 0)

        velz = scipy.integrate.cumtrapz(z_data, dx = dtavg, initial = 0)
        posz = scipy.integrate.cumtrapz(velz, dx = dtavg, initial = 0)
        

        fig = plt.figure()
        

        N = len(x_data)
        T = 0.005
        W = fftfreq(N, T)


        axfft = None
        cutx = None
        cutxifft = None

        ayfft = None
        cuty = None
        cutyifft = None

        azfft = None
        cutz = None
        cutzifft = None

        #x accel filtering
        axfft = fft(x_data)

        cutx = axfft.copy()

        cutx[(W > 20)] = 0
        cutx[(W < -20)] = 0

        cutxifft = ifft(cutx)
        #y accel filtering
        ayfft = fft(y_data)

        cuty = ayfft.copy()

        cuty[(W > 20)] = 0
        cuty[(W < -20)] = 0

        cutyifft = ifft(cuty)
        #z accel filtering
        azfft = fft(z_data)

        cutz = azfft.copy()

        cutz[(W > 20)] = 0
        cutz[(W < -20)] = 0

        cutzifft = ifft(cutz)

        cutxifft = np.real(cutxifft)
        cutyifft = np.real(cutyifft)
        cutzifft = np.real(cutzifft)

        for i in range(len(cutxifft)):
            if abs(cutxifft[i]) < 0.6:
                cutxifft[i] = 0

        for i in range(len(cutyifft)):
            if abs(cutyifft[i]) < 0.6:
                cutyifft[i] = 0

        for i in range(len(cutzifft)):
            if abs(cutzifft[i]) < 0.6:
                cutzifft[i] = 0


        velx2 = None
        posx2 = None
        vely2 = None
        posy2= None
        velz2 = None
        posz2 = None

        

        velx2 = scipy.integrate.cumtrapz(cutxifft, dx = dtavg, initial = 0)
        for i in range(len(velx2)):
            if abs(velx2[i]) < 0.3:
                velx2[i] = 0

        posx2 = scipy.integrate.cumtrapz(velx2, dx = dtavg, initial = 0)

        vely2 = scipy.integrate.cumtrapz(cutyifft, dx = dtavg, initial = 0)
        for i in range(len(vely2)):
            if abs(vely2[i]) < 0.3:
                vely2[i] = 0

        posy2 = scipy.integrate.cumtrapz(vely2, dx = dtavg, initial = 0)

        velz2 = scipy.integrate.cumtrapz(cutzifft, dx = dtavg, initial = 0)
        for i in range(len(velz2)):
            if abs(velz2[i]) < 0.3:
                velz2[i] = 0

        posz2 = scipy.integrate.cumtrapz(velz2, dx = dtavg, initial = 0)


        plt.subplot(2,3,1)
        plt.plot(range(len(x_data)), list(zip(x_data, cutxifft)), label = ['measured', 'filtered'])
        plt.legend()
        plt.ylabel("Acceleration (m/s/s)")
        plt.xlabel("Sample")
        plt.title("X-Axis Acceleration")

        plt.subplot(2,3,2)
        plt.plot(range(len(y_data)), list(zip(y_data, cutyifft)), label = ['measured', 'filtered'])
        plt.legend()
        plt.ylabel("Acceleration (m/s/s)")
        plt.xlabel("Sample")
        plt.title("Y-Axis Acceleration")

        plt.subplot(2,3,3)
        plt.plot(range(len(z_data)), list(zip(z_data, cutzifft)), label = ['measured', 'filtered'])
        plt.legend()
        plt.ylabel("Acceleration (m/s/s)")
        plt.xlabel("Sample")
        plt.title("Z-Axis Acceleration ")

        plt.subplot(2,3,4)
        plt.plot(range(len(velx2)), list(zip(velx, velx2)), label = ['measured', 'filtered'])
        plt.legend()
        plt.ylabel("Velocity (m/s)")
        plt.xlabel("Sample")
        plt.title("X-Axis Velocity")

        plt.subplot(2,3,5)
        plt.plot(range(len(vely2)), list(zip(vely, vely2)), label = ['measured', 'filtered'])
        plt.legend()
        plt.ylabel("Velocity (m/s")
        plt.xlabel("Sample")
        plt.title("Y-Axis Velocity")

        plt.subplot(2,3,6)
        plt.plot(range(len(velz2)), list(zip(velz, velz2)), label = ['measured', 'filtered'])
        plt.legend()
        plt.ylabel("Velocity (m/s)")
        plt.xlabel("Sample")
        plt.title("Z-Axis Velocity")

        plt.figure()
        ax = plt.subplot(projection = '3d')
        # ax = plt.subplot2grid(shape = (3,3), loc = (2,0), projection = '3d', colspan = 3, rowspan = 3)
        for i in range(len(posx)):
            ax.scatter(posz2[i], posx2[i], posy2[i], s = 50)

        left, right = plt.xlim()
        ax.set_zlim(left, right)
        ax.set_ylim(left, right)

        ax.set_xlim([-0.5, 0.5])
        ax.set_ylim([-0.5, 0.5])
        ax.set_zlim([-0.5,0.5])


        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.title('3D Plot of filtered output')
        plt.show()


if __name__ == "__main__":
    main()