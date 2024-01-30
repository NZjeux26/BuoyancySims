import pygame
import sys
from values import Airship, Atmosphere, Constants
import math

# Initialize pygame
pygame.init()

# Define screen size
screen_width = 1600
screen_height = 1600

# Create airship
airship = Airship(23.25, 3.05, 195, 0, 0, 100, 0)

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

trust = 0.0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                airship.yval += 0.2
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: 
                airship.yval -= 0.2

    dt = clock.tick(60) / 1000.0  # 60 frames per second 
    font = pygame.font.Font(None,32)
    
    #if the temp is not correct, the pressure will not be and thus the density will not either
    #Temp is the sea level temp - the (lasp rate * the altitude)
    atmosphere.temperature = Constants.standard_temperature_at_sea_level - (Constants.temperature_lapse_rate * airship.ypos)#now correct
    
    atmosphere.pressure = Constants.standard_pressure_sea_level * math.exp(
            -Constants.gravity_on_earth * Constants.molar_mass_of_air * airship.ypos / (Constants.gas_constant * (atmosphere.temperature + 273.15))#temp converted to kelvin for mathing
    )
    #density = pressure * molar_mass_of_air / gas constant * temperature(in kelvin)   
    atmosphere.density = (atmosphere.pressure * Constants.molar_mass_of_air) / (Constants.gas_constant * (atmosphere.temperature + 273.15))


    #Calculate buoyancy force of the object
    bforce = (atmosphere.density - Constants.hydrogen_density) * Constants.gravity_on_earth * airship.volume
    #Calculate the mass of the object in newtons which is mass * gravity
    force_gravity = airship.mass * Constants.gravity_on_earth
    #the net force is the difference between the two
    net_force = bforce - force_gravity
    
    #calculate acceleration which is the net force divided by the mass of the object
    acceleration = net_force / airship.mass
    
    #Update position and velocity. V is calculated bu taking the acceleration and multiplying it by the time.
    airship.yval += (acceleration + trust) * dt #V = a * t
    airship.ypos += airship.yval
    
    airrectangle.y = max(0, min(screen_height - airrectangle.height, airship.ypos))
    
    # Draw the rectangle on the screen
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, rectangle_color, airrectangle)

    alt_txt = font.render("Altitude: {} m".format(airship.ypos),True,(0, 0, 0))
    acc_txt = font.render("Acceleration: {} m/s^2".format(acceleration),True,(0, 0, 0))
    vertvelo_txt = font.render("Vertical Velocity: {} m/s".format(airship.yval),True,(0, 0, 0))
    trust_txt = font.render("Engine Trust: {} m/s".format(trust),True,(0, 0, 0))
    screen.blit(alt_txt, (screen_width - 800, 20))
    screen.blit(acc_txt, (screen_width - 800, 60))
    screen.blit(vertvelo_txt, (screen_width - 800, 100))
    screen.blit(trust_txt, (screen_width - 800, 140))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit pygame
pygame.quit()


#NOTES
#Something in the calculation for pressure is not right, it's dropping way to fast and doesn't match the suposed altitude of ship
#Change the values to use consistant values, either all Kelvin or all Celcius
 