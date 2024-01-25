import math

class Airship:
    def __init__(self, length, diameter, mass, xval, yval, xpos, ypos):
        self.length = length #in meters
        self.diameter = diameter #in meters
        self.mass = mass #in Kilograms
        self.xval = xval
        self.yval = yval
        self.xpos = xpos
        self.ypos = ypos
        self.radius = diameter / 2  # Derived from diameter
        self.volume = math.pi * (diameter / 2)**2 * length  # Derived from dimensions

class Atmosphere:
    def __init__(self, pressure, density, temperature):
        self.pressure = pressure
        self.density = density
        self.temperature = temperature

class BuoyancyData:
    def __init__(self, buoyancy_force, mass_lifted, acceleration):
        self.buoyancy_force = buoyancy_force
        self.mass_lifted = mass_lifted
        self.acceleration = acceleration

class Constants:
    gravity_on_earth = 9.81  # m/s^2
    air_density_sea_level = 1.225 # kg/m^3
    standard_pressure_sea_level = 101325  # Pascals
    gas_constant = 287.058  # J/(kg·K)
    temperature_lapse_rate = 0.0065  # degrees Celsius per meter
    standard_temperature_at_sea_level = 294.65 # Kelvin Might need ot change to Celsius
    exponent_constant = 0.19#5.255
    inertia_coefficient = 0.01
    #Troposphere (0 - 11 km): Lapse rate is -6.4914 K/km, so the exponent for pressure and density is ~5.2561.