import math

class Airship:
    def __init__(self, length, diameter, mass, xval, yval, xpos, ypos):
        self.length = length
        self.diameter = diameter
        self.mass = mass
        self.xval = xval
        self.yval = yval
        self.xpos = xpos
        self.ypos = ypos
        self.radius = diameter / 2  # Derived from diameter
        self.volume = math.pi * (diameter / 2)**2 * length  # Derived from dimensions

class Atmosphere:
    def __init__(self, pressure, density):
        self.pressure = pressure
        self.density = density

class BuoyancyData:
    def __init__(self, buoyancy_force, mass_lifted, acceleration):
        self.buoyancy_force = buoyancy_force
        self.mass_lifted = mass_lifted
        self.acceleration = acceleration

class Constants:
    gravity_on_earth = 3.711  # m/s^2
    air_density_sea_level = 0.988  # kg/m^3
    standard_pressure_sea_level = 93555  # Pascals
    gas_constant = 287.058  # J/(kg·K)