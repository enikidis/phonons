import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
L = 0.01   # Length of the simulation region (in meters)
N = 1000   # Number of spatial grid points
dx = L/N   # Spatial grid spacing (in meters)
T = 1e-9   # Total simulation time (in seconds)
dt = dx**2/(2*np.pi)**2  # Time step (in seconds)
M = 10     # Mass of the particle (in kilograms)
hbar = 1.05e-34   # Planck's constant (in joule seconds)
k0 = 5/L   # Central wavenumber of the wave packet (in inverse meters)
sigma = 0.002   # Width of the Gaussian wave packet (in meters)
y0 = L/2   # Initial position of the particle (in meters)
v0 = 0     # Initial velocity of the particle (in meters per second)
S = lambda x, t: (M*v0*x/hbar + M*(x-y0)**2/(2*sigma**2) - M*k0*x - M*k0**2*hbar*t/(2*M))  # Action function

# Initialize the wave function and particle positions
x = np.arange(N)*dx
psi = np.exp(-(x-L/4)**2/(2*sigma**2)) + np.exp(-(x-3*L/4)**2/(2*sigma**2))
psi /= np.sqrt(np.sum(np.abs(psi)**2*dx))
q = np.random.choice(x, size=1000)

# Plot the initial wave function
plt.plot(x, np.abs(psi)**2)
plt.xlabel('Position (m)')
plt.ylabel('Probability density')
plt.show()

# Propagate the wave function and particle positions
for n in range(int(T/dt)):
    # Compute the velocity field
    v = hbar*np.imag(psi/np.conj(psi)*np.gradient(psi, dx))
    # Compute the Bohmian trajectories
    q += v/M*dt + np.sqrt(dt)*np.random.randn(len(q))*np.sqrt(hbar/M)
    # Apply periodic boundary conditions
    q = np.mod(q, L)
    # Compute the phase factor
    expS = np.exp(1j*S(x, n*dt)/hbar)
    # Update the wave function
    psi = psi*expS
    # Apply the Bohmian boundary condition
    psi[0] = psi[-1] = 0

# Plot the final wave function and particle positions
plt.plot(x, np.abs(psi)**2)
plt.scatter(q, np.zeros(len(q)), s=1)
plt.xlabel('Position (m)')
plt.ylabel('Probability density')
plt.show()
