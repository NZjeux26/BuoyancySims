import pygame
from values import Airship, Atmosphere, Constants
import math

# Initialize pygame
pygame.init()

# Define screen size
screen_width = 600
screen_height = 1200

# Create airship
airship = Airship(232.2, 30.5, 155, 0, 0, 100, 100)

# Create the atmosphere
atmosphere = Atmosphere(
    pressure=Constants.standard_pressure_sea_level,
    density=Constants.air_density_sea_level,
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
     
    # Calculate pressure and density at current altitude
    atmosphere.pressure *= (1 - 0.0065 * airship.ypos / 288.15) ** 5.255
    atmosphere.density = atmosphere.pressure / (Constants.gas_constant * 288.15 *
                                                (1 + 0.001 * airship.ypos / 288.15))

    # Calculate buoyancy force
    bforce = atmosphere.density * Constants.gravity_on_earth * airship.volume

    # Calculate acceleration
    a = (bforce / (airship.mass * 1000)) - Constants.gravity_on_earth

    # Update position and velocity
    airship.yval += a * dt
    airship.ypos += airship.yval
    airrectangle.y += airship.ypos
    airrectangle.y = max(0, min(screen_height - airrectangle.height, airship.ypos))
    # Draw the rectangle on the screen
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, rectangle_color, airrectangle)

    # Update the display
    pygame.display.flip()

    # Print relevant values for debugging
    print("Altitude:", airship.ypos, "m")
    print("Vertical velocity:", airship.yval, "m/s")
    print("Buoyancy force:", bforce, "Newtons")
    print("Acceleration:", a, "m/s^2")

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit pygame
pygame.quit()
