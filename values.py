import math

class Airship:
    def __init__(self, length, diameter,height,dry_mass,ballast,fuelmass,num_engines,xval, yval, xpos, ypos):
        self.length = length #in meters
        self.diameter = diameter #in meters
        self.height = height #in meters
        self.mass = fuelmass + dry_mass + ballast#in Kilograms
        self.fuelmass = fuelmass #in Kilograms
        self.dry_mass = dry_mass #in Kilograms
        self.ballest = ballast #in Kilograms
        self.num_engines = num_engines
        self.cd = 0.029 #drag coefficent derived from the USS Los Angles (+ 0.05 for extras like gondalas and different shape)
        self.xval = xval
        self.yval = yval
        self.xpos = xpos
        self.ypos = ypos
        self.radius = diameter / 2  # Derived from diameter
        self.volume = math.pi * (diameter / 2)**2 * length  # Derived from dimensions
        self.frontal_area = math.pi * self.radius**2
        self.lateral_area = 2 * math.pi * self.radius * self.length # Lateral surface area
class Engine:
    def __init__(self, mass, fuelflow, prop_diameter, HP, thrust, prop):
        self.mass = mass
        self.fuelflow = fuelflow
        self.prop_diameter = prop_diameter
        self.hp = HP
        self.thrust = thrust
        
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
  