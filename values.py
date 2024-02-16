import math
import pygame
class Projectile:
    def __init__(self, x, y, velocity, angle):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.angle = angle
    def update(self):
        self.x += self.velocity * math.cos(math.radians(self.angle))
        self.y += self.velocity * math.sin(math.radians(self.angle))
    
class Weapons:
    def __init__(self,dry_mass,barrel_length,type,max_ammo,mag_size,rate_of_fire,catridge_mass,reload_time,muzzle_velocity,crew_requirement):
        self.xval = 0
        self.yval = 0
        self.xpos = 0
        self.ypos = 0
        self.dry_mass = dry_mass
        self.barrel_length = barrel_length #in meters
        self.type  = type #types are for later so restrictions etc can be generalised.
        self.max_ammo = max_ammo#max ammo the weapon can "carry"
        self.mag_size = mag_size #max mag size before reloading
        self.current_mag = [mag_size]
        self.rate_of_fire = rate_of_fire #how many rounds are fire in a sec
        self.catridge_mass = catridge_mass #mass of the entire catridge
        self.bullet_mass = self.catridge_mass - 0.015 #mass of just the bullet
        self.ammo_mass = self.catridge_mass * self.max_ammo #mass of the entire ammo supply of the weapon
        self.total_mass = self.dry_mass + self.ammo_mass #total mass of the weapon, dry mass plus the ammo
        self.reload_time = reload_time #time to reload mags in seconds
        self.muzzle_velocity = muzzle_velocity #velocity of the round in m/s
        self.muzzle_energy = (self.ammo_mass / 2) * muzzle_velocity**2
        self.crew_requirement = crew_requirement
        self.projectiles = None
    def cal_recoil_force(self):
        d_t = self.barrel_length / self.muzzle_velocity
        recoil_force = self.bullet_mass / (self.muzzle_velocity / d_t)
    def weapon_pos(self, X, Y):
        self.xpos = X / 2
        self.ypos = Y / 2
    def fire_projectile(self,mousex,mousey):
        if self.projectile is None:
            angle = math.degrees(math.atan2(mousey - self.ypos, mousex - self.xpos))
            self.projectile = Projectile(self.xpos,self.ypos, self.muzzle_velocity, angle)
        
    def update_projectile(self):
      if self.projectile:
        self.projectile.update()
        if not (0 <= self.projectile.x < 1200 and 0 <= self.projectile.y < 1080):
            self.reset_projectile()
            
    def reset_projectile(self):
        self.projectile = None

class Engine:
    def __init__(self, mass, fuelflow, prop_diameter, prop_efficiency, HP, thrust):
        self.mass = mass
        self.fuelflow = fuelflow
        self.prop_diameter = prop_diameter
        self.prop_area = math.pi * (prop_diameter / 2) **2
        self.prop_efficiency = prop_efficiency
        self.hp = HP
        self.thrust = thrust
    def cal_engine_thrust(self,density,velocity): #this is the max thrust from ONE engine. 3.5m/s is a random value It should be Ve which is the exit velocity of the moved mass by the propellor sanding still.
        return 0.5 * density * self.prop_area * (3.5**2 - velocity**2)

class Airship:
    def __init__(self, length, diameter,height,dry_mass,ballast,fuelmass,num_engines,cd,engine,xval, yval, xpos, ypos):
        self.length = length #in meters
        self.diameter = diameter #in meters
        self.height = height #in meters Not used but if i wanted to switch to using math for an Elliposid then i need it
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
         #the frontal area and lateral area are assuming a cylinder when most airships are infact Ellipsoid. To keep this simple i have stuck with a cylinder
        self.volume = math.pi * (diameter / 2)**2 * length  # Derived from dimensions
        self.frontal_area = math.pi * self.radius**2 
        self.lateral_area = 2 * math.pi * self.radius * self.length # Lateral surface area
    #returns the drag on the Y or X axis. 
    def cal_drag_y(self, density):
        return (density / 2) * self.yval**2 * self.cd * self.lateral_area
    def cal_drag_x(self, density):
        return (density / 2) * self.xval**2 * self.cd * self.frontal_area
        
class Atmosphere:
    def __init__(self, pressure, density, temperature):
        self.pressure = pressure
        self.density = density
        self.temperature = temperature
    def cal_temperature(self,altitude): #Temp is the sea level temp - the (lasp rate * the altitude)
        return Constants.standard_temperature_at_sea_level - (Constants.temperature_lapse_rate * altitude)
    def cal_pressure(self,altitude):
        return Constants.standard_pressure_sea_level * math.exp(
            -Constants.gravity_on_earth * Constants.molar_mass_of_air * altitude / (Constants.gas_constant * (self.temperature + 273.15))#temp converted to kelvin for mathing
    )
    def cal_density(self): #density = pressure * molar_mass_of_air / gas constant * temperature(in kelvin) 
        return (self.pressure * Constants.molar_mass_of_air) / (Constants.gas_constant * (self.temperature + 273.15))
    
class BuoyancyData:
    def __init__(self, buoyancy_force, mass_lifted, acceleration):
        self.buoyancy_force = buoyancy_force
        self.mass_lifted = mass_lifted
        self.acceleration = acceleration
    def cal_buoyancy_force(density,volume):
        return (density - Constants.hydrogen_density) * Constants.gravity_on_earth * volume
    def cal_gravity_force(mass):
        return mass * Constants.gravity_on_earth

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