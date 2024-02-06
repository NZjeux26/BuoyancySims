import math
class Engine:
    def __init__(self, mass, fuelflow, prop_diameter, prop_efficiency, HP, thrust):
        self.mass = mass
        self.fuelflow = fuelflow
        self.prop_diameter = prop_diameter
        self.prop_area = math.pi * (prop_diameter / 2) **2
        self.prop_efficiency = prop_efficiency
        self.hp = HP
        self.thrust = thrust

class Airship:
    def __init__(self, length, diameter,height,dry_mass,ballast,fuelmass,num_engines,cd,engine,xval, yval, xpos, ypos):
        self.length = length #in meters
        self.diameter = diameter #in meters
        self.height = height #in meters
        self.fuelmass = fuelmass #in Kilograms
        self.dry_mass = dry_mass #in Kilograms
        self.ballest = ballast #in Kilograms
        self.engines = [engine for _ in range(num_engines)]
        self.num_engines = num_engines
        self.mass = fuelmass + dry_mass + ballast #+ engine_mass#in Kilograms
        self.cd = cd 
        self.xval = xval
        self.yval = yval
        self.xpos = xpos
        self.ypos = ypos
        self.radius = diameter / 2  # Derived from diameter
        self.volume = math.pi * (diameter / 2)**2 * length  # Derived from dimensions
        self.frontal_area = math.pi * self.radius**2
        self.lateral_area = 2 * math.pi * self.radius * self.length # Lateral surface area
        
class Atmosphere:
    def __init__(self, pressure, density, temperature):
        self.pressure = pressure
        self.density = density
        self.temperature = temperature
    def cal_temperature(self,altitude):
        return Constants.standard_temperature_at_sea_level - (Constants.temperature_lapse_rate * altitude)
    def cal_pressure(self,altitude,temperature):
        return Constants.standard_pressure_sea_level * math.exp(
            -Constants.gravity_on_earth * Constants.molar_mass_of_air * altitude / (Constants.gas_constant * (temperature + 273.15))#temp converted to kelvin for mathing
    )
    def cal_density(self,pressure,temperature):
        return (pressure * Constants.molar_mass_of_air) / (Constants.gas_constant * (temperature + 273.15))
    
class BuoyancyData:
    def __init__(self, buoyancy_force, mass_lifted, acceleration):
        self.buoyancy_force = buoyancy_force
        self.mass_lifted = mass_lifted
        self.acceleration = acceleration
    def cal_buoyancy_force(density,volume):
        return (density - Constants.hydrogen_density) * Constants.gravity_on_earth * volume

class Constants:
    gravity_on_earth = 9.80665  # m/s^2
    air_density_sea_level = 1.225 # kg/m^3
    hydrogen_density = 0.008375 #kg/m^3
    standard_pressure_sea_level = 101325  # Pascals
    gas_constant = 8.3144598  # J/(kg·K) 
    temperature_lapse_rate = 0.0065  # 6.5c per kilometer(0.0065c per meter) Also 0.0065 Kelvin per meter
    standard_temperature_at_sea_level = 15 #celsius (288.15 Kelvin)
    exponent_constant = 5.2561
    inertia_coefficient = 0.09
    molar_mass_of_air = 0.0289644  # kg/mol
    molar_mass_of_hydrogen = 0.00201588 #kg/mol