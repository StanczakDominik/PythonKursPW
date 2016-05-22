import numpy as np

g=9.81
L=0.4
m=1.
a=0.
b=100.

def f(r, t=0):
    """ liczy pochodną czasową wektora stanu dla podwójnego wahadła
    r: tablica: kąt1, kąt2, prędkość kątowa 1, prędkość kątowa 2
    t: czas, niespecjalnie konieczny, dlatego z defaultem"""
    theta1=r[0]
    theta2=r[1]
    omega1=r[2]
    omega2=r[3]
    ftheta1=omega1
    ftheta2=omega2
    fomega1=-(omega1**2*np.sin(2.*theta1-2.*theta2)+2*omega2**2*np.sin(theta1-theta2)+g/L*(np.sin(theta1-2.*theta2)+3*np.sin(theta1)))/(3.-np.cos(2*theta1-2.*theta2))
    fomega2=(4*omega1**2*np.sin(theta1-theta2)+omega2**2.*np.sin(2*theta1-2.*theta2)+2.*g/L*(np.sin(2.*theta1-theta2)-np.sin(theta2)))/(3.-np.cos(2.*theta1-2.*theta2))
    return np.array([ftheta1,ftheta2,fomega1,fomega2],float)


def locations(r):
    """konwertuje tablicę stanu wahadełka na pozycje kartezjańskie (x1, y1, x2, y2)"""
    theta1=r[0]
    theta2=r[1]
    rod2pos=bob1pos=np.array([L*np.sin(theta1),-L*np.cos(theta1)], float) #also rod1
    rod2axis=np.array([L*np.sin(theta2),-L*np.cos(theta2)], float)
    bob2pos=bob1pos+rod2axis
    return np.array((*bob1pos, *bob2pos))
