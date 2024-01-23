import pygame
from values import Airship, Atmosphere, BuoyancyData, Constants

# Initialize pygame
pygame.init()

# Define screen size
screen_width = 600
screen_height = 1200

#create airship
airship = Airship(232.2,30.5,195,0,0,100,150)

atmosphere = Atmosphere(
    pressure = Constants.standard_pressure_sea_level,
    density = Constants.air_density_sea_level,
)

bforce = atmosphere.density * Constants.gravity_on_earth * airship.volume
masslift = bforce / Constants.gravity_on_earth
a = bforce / airship.mass
# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Pygame Rectangle")

# Define a color for the rectangle
rectangle_color = (255, 0, 0)

# Define rectangle position and size
rectangle_x = 100
rectangle_y = 150
rectangle_width = 200
rectangle_height = 100

# Create the rectangle object
airrectangle = pygame.Rect(airship.xpos, airship.ypos, 100, 100)
airrectangle.y = airship.ypos
# Draw the rectangle on the screen
pygame.draw.rect(screen, rectangle_color, airrectangle)

running = True
while running:
    # Check for events (e.g., quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    bforce = atmosphere.density * Constants.gravity_on_earth * airship.volume
    masslift = bforce / Constants.gravity_on_earth
    a = bforce / airship.mass
    
    # Print buoyancy and acceleration values
    print("Buoyancy force:", bforce, "Newtons")
    print("Mass lifted:", masslift, "kg")
    print("Acceleration:", a, "m/s^2")
    
    airship.yval = a
    #something not working around here, the rectangle isn't moving
    airrectangle.y += airship.yval
   
    
    # Print altitude and velocity
    print("Altitude:", airship.ypos, "m")
    print("Vertical velocity:", airship.yval, "m/s")
    
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
