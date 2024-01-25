import pygame
import sys
from values import Airship, Atmosphere, Constants
import math

# Initialize pygame
pygame.init()

# Define screen size
screen_width = 600
screen_height = 1200

# Create airship
airship = Airship(23.25, 3.05, 183, 0, 0, 100, 0)

# Create the atmosphere
atmosphere = Atmosphere(
    pressure = Constants.standard_pressure_sea_level,
    density= Constants.air_density_sea_level,
    temperature=Constants.standard_temperature_at_sea_level
)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Buoyancy Simulation")

# Define color for the rectangle
rectangle_color = (255, 0, 0)

# Create the rectangle object
airrectangle = pygame.Rect(airship.xpos, airship.ypos, 100, 100)

# Set up the clock to control the frame rate
clock = pygame.time.Clock()

#clear the textfile
with open("output.txt", "w"):
    pass 

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    dt = clock.tick(60) / 1000.0  # 60 frames per second 
     
    # Calculate pressure and density at current altitude ** Note for later, precalculating this into a table in 100m increments and using a table lookup on the Amiga.
    atmosphere.pressure *= (1 - Constants.temperature_lapse_rate * airship.ypos / Constants.standard_temperature_at_sea_level) ** Constants.exponent_constant # something in the airpressure calculations is causing the pressure to drop huge amounts when it shouldn't.
    atmosphere.density = atmosphere.pressure / (Constants.gas_constant * Constants.standard_temperature_at_sea_level *
                                                (1 + 0.001 * airship.ypos / Constants.standard_temperature_at_sea_level))

    # Calculate buoyancy force
    bforce = atmosphere.density * Constants.gravity_on_earth * airship.volume
    
    #calculate the inertia of the airship
    if airship.yval > 0:
        inertia_force = Constants.inertia_coefficient * airship.yval
    else:
        inertia_force = 0
    
    net_force = bforce - inertia_force
    # Calculate acceleration
    a = (net_force/ airship.mass) - Constants.gravity_on_earth
    
    # Update position and velocity
    airship.yval += a * dt
    airship.ypos += airship.yval# * dt + 0.5 * a * dt**2
    
    airrectangle.y = max(0, min(screen_height - airrectangle.height, airship.ypos))
    # Draw the rectangle on the screen
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, rectangle_color, airrectangle)

    # Update the display
    pygame.display.flip()

    with open("output.txt", "a") as file:
        sys.stdout = file
        
        # Print relevant values for debugging
        print("Altitude:", airrectangle.y, "m")
        print("Vertical velocity:", airship.yval, "m/s")
        print("Buoyancy force:", bforce, "Newtons")
        print("Airship Mass", airship.mass, "KG")
        print("Acceleration:", a, "m/s^2")
        print("Denisty", atmosphere.density, "kg/m^3")
        print("Air Pressure", atmosphere.pressure, "Pascals \n")

        sys.stdout = sys.__stdout__
    
    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit pygame
pygame.quit()
