import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
L = 0.01   # Length of the simulation region (in meters)
N = 100   # Number of spatial grid points per dimension
dx = L/N   # Spatial grid spacing (in meters)
T = 1e-9   # Total simulation time (in seconds)
dt = dx**2/(2*np.pi)**2  # Time step (in seconds)
M = 10     # Mass of the particle (in kilograms)
hbar = 1.05e-34   # Planck's constant (in joule seconds)
k0 = 5/L   # Central wavenumber of the wave packet (in inverse meters)
sigma = 0.002   # Width of the Gaussian wave packet (in meters)
y0 = L/2   # Initial position of the particle (in meters)
v0 = 0     # Initial velocity of the particle (in meters per second)

# Initialize the wave function and particle positions
x = np.arange(N)*dx
y = np.arange(N)*dx
X, Y = np.meshgrid(x, y)
psi = np.exp(-(X-L/4)**2/(2*sigma**2) - (Y-L/4)**2/(2*sigma**2)) + np.exp(-(X-3*L/4)**2/(2*sigma**2) - (Y-3*L/4)**2/(2*sigma**2))
psi /= np.sqrt(np.sum(np.abs(psi)**2*dx*dx))
qx = np.random.choice(x, size=1000)
qy = np.random.choice(y, size=1000)

# Plot the initial wave function
plt.imshow(np.abs(psi)**2)
plt.xlabel('Position (m)')
plt.ylabel('Probability density')
plt.show()

# Propagate the wave function and particle positions
for n in range(int(T/dt)):
    # Compute the velocity field
    vx = hbar*np.imag(psi/np.conj(psi)*np.gradient(psi, dx, axis=1))/M
    vy = hbar*np.imag(psi/np.conj(psi)*np.gradient(psi, dx, axis=0))/M
    # Compute the Bohmian trajectories
    qx += vx*dt + np.sqrt(dt)*np.random.randn(len(qx))*np.sqrt(hbar/M)
    qy += vy*dt + np.sqrt(dt)*np.random.randn(len(qy))*np.sqrt(hbar/M)
    # Apply periodic boundary conditions
    qx = np.mod(qx, L)
    qy = np.mod(qy, L)
    # Update the wave function
    expS = np.exp(1j*S(X, Y, n*dt)/hbar)
