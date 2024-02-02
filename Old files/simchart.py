import sys
from values import Airship, Atmosphere, Constants
import math

# Create airship
airship = Airship(23.25, 3.05, 100, 0, 0, 100, 0)

# Create the atmosphere
atmosphere = Atmosphere(
    pressure = Constants.standard_pressure_sea_level,
    density= Constants.air_density_sea_level,
    temperature=Constants.standard_temperature_at_sea_level
)

#clear the textfile
with open("buoyancytable.txt", "w"):
    pass 

altitude_increment = 100
altitude = 0

while altitude <= 2000:
    max_lift_mass = 0.0
    
    for test_mass in range(airship.mass, 1, 1001):
        airship.mass = test_mass
        atmosphere.temperature = Constants.standard_temperature_at_sea_level - (Constants.temperature_lapse_rate * altitude)#now correct
        
        atmosphere.pressure = Constants.standard_pressure_sea_level * math.exp(
                -Constants.gravity_on_earth * Constants.molar_mass_of_air * altitude / (Constants.gas_constant * (atmosphere.temperature + 273.15))#temp converted to kelvin for mathing
        )
        #density = pressure * molar_mass_of_air / gas constant * temperature(in kelvin)   
        atmosphere.density = (atmosphere.pressure * Constants.molar_mass_of_air) / (Constants.gas_constant * (atmosphere.temperature + 273.15))


        # Calculate buoyancy force, and the netforce
        bforce = (atmosphere.density - Constants.hydrogen_density) * Constants.gravity_on_earth * airship.volume
        force_gravity = airship.mass * Constants.gravity_on_earth
        net_force = bforce - force_gravity
        
        acceleration = net_force / airship.mass
        
        if acceleration >= 0.0:
            max_lift_mass = test_mass
        else:
            break
            
        with open("buoyancytable.txt", "a") as file:
            sys.stdout = file
                    
            # Print relevant values for debugging
            print("Altitude:", altitude, "m")
            print("Max Lift Mass:", max_lift_mass, "kg")

            sys.stdout = sys.__stdout__
 
        altitude += 100#altitude_increment * Constants.temperature_lapse_rate

#NOTES
#Something in the calculation for pressure is not right, it's dropping way to fast and doesn't match the suposed altitude of ship
#Change the values to use consistant values, either all Kelvin or all Celcius
 