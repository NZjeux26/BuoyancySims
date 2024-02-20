import sys
from values import Airship, Atmosphere, Constants
import math

# Create airship
airship = Airship(
    length = 23.25, 
    diameter = 3.05, 
    height = 3.35,
    dry_mass = 67,
    fuelmass = 36,
    ballast =  91,
    engine = None,
    num_engines = 4,
    cd = 0.029, #drag coefficent derived from the USS Los Angles (+ 0.05 for extras like gondalas and different shape)
    xval = 0, 
    yval = 0, 
    xpos = 100, 
    ypos = 0
)

# Create the atmosphere
atmosphere = Atmosphere(
    pressure = Constants.standard_pressure_sea_level,
    density= Constants.air_density_sea_level,
    temperature=Constants.standard_temperature_at_sea_level
)

#clear the textfile
with open("output.txt", "w"):
    pass 

altitude_increment = 100
altitude = 0

while altitude <= 5000:
    
    atmosphere.temperature = Constants.standard_temperature_at_sea_level - (Constants.temperature_lapse_rate * altitude)#now correct
        
    atmosphere.pressure = Constants.standard_pressure_sea_level_Hec * math.exp(
            -Constants.gravity_on_earth * Constants.molar_mass_of_air * altitude / (Constants.gas_constant * (atmosphere.temperature + 273.15))#temp converted to kelvin for mathing
    )
    #density = pressure * molar_mass_of_air / gas constant * temperature(in kelvin)   
    atmosphere.density = ((atmosphere.pressure * Constants.molar_mass_of_air) / (Constants.gas_constant * (atmosphere.temperature + 273.15))) * 1000


    # Calculate buoyancy force, and the netforce
    bforce = (atmosphere.density - Constants.hydrogen_density) * Constants.gravity_on_earth * airship.volume
    force_gravity = airship.mass * Constants.gravity_on_earth
    net_force = bforce - force_gravity
        
    acceleration = net_force / airship.mass
        
   
    with open("output.txt", "a") as file:
        sys.stdout = file

        # Print relevant values for debugging
        print("Altitude:", altitude, "m")
        print("Buoyancy force:", bforce, "Newtons")
        print("Airship Mass", airship.mass, "KG")
        print("Denisty", atmosphere.density, "kg/m^3")
        print("Air Pressure", atmosphere.pressure, "kPa")
        print("Air Temperature", atmosphere.temperature, "Celsius\n")

        sys.stdout = sys.__stdout__

    altitude += altitude_increment

#NOTES
#Something in the calculation for pressure is not right, it's dropping way to fast and doesn't match the suposed altitude of ship
#Change the values to use consistant values, either all Kelvin or all Celcius
 