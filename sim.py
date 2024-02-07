import pygame
import sys
from values import Airship, Atmosphere, Constants, Engine, BuoyancyData
import math

# Initialize pygame
pygame.init()

def draw_things():
    alt_txt = font.render("Altitude: {} m".format(airship.ypos),True,(0, 0, 0))
    acc_txt = font.render("Acceleration: {} m/s^2".format(acceleration_y),True,(0, 0, 0))
    vertvelo_txt = font.render("Vertical Velocity: {} m/s".format(airship.yval),True,(0, 0, 0))
    horvelo_txt = font.render("Horizontal Velocity: {} m/s".format(airship.xval),True,(0, 0, 0))
    mass_txt = font.render("Mass: {} KG".format(airship.mass),True,(0, 0, 0))
    maxthrust_txt = font.render("Max Power: {} N".format(engines.thrust * airship.num_engines),True,(0, 0, 0))
    actual_thrust_txt = font.render("Actual Thrust: {} N".format(engine_thrust_y * airship.num_engines),True,(0, 0, 0))
    throttle_y_txt = font.render("Throttle: {} %".format(throttle_y),True,(0, 0, 0))
   # trust_txt = font.render("Engine Trust: {} m/s".format(trust),True,(0, 0, 0))
   
    screen.blit(alt_txt, (screen_width - 800, 20))
    screen.blit(acc_txt, (screen_width - 800, 60))
    screen.blit(vertvelo_txt, (screen_width - 800, 100))
    screen.blit(horvelo_txt, (screen_width - 800, 140))
    screen.blit(mass_txt, (screen_width - 800, 180))
    screen.blit(maxthrust_txt, (screen_width - 800, 220))
    screen.blit(actual_thrust_txt, (screen_width - 800, 260))
    screen.blit(throttle_y_txt, (screen_width - 800, 300))

# Define screen size
screen_width = 1200
screen_height = 1080

#Based roughly on the Lycoming O-540
engines = Engine( #egines need to be created before the airship, done in this OO so airships can swap out engines
    mass = 2,
    fuelflow = 0.719, #this will change based on the max thrust
    prop_diameter = 2.032, #meters based on the C2R40500STP propeller
    HP = 419, #not actually sure this is going to be used
    prop_efficiency = 0.83,
    thrust = 0
    #thrust needs calcualted per frame as it changes based on height
) 

# Create airship Based around the LZ-129 Graf Zeppelin
airship = Airship(
    length = 23.25, 
    diameter = 3.05, 
    height = 3.35,
    dry_mass = 67,
    fuelmass = 36,
    ballast =  92,
    engine = engines,
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
throttle_y = 0
throttle_x = 0
# Flags to track key state
increase_throttle_y = False
decrease_throttle_y = False
increase_throttle_x = False
decrease_throttle_x = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                increase_throttle_y = True
            elif event.key == pygame.K_DOWN: 
                decrease_throttle_y = True
            elif event.key == pygame.K_LEFT:
                decrease_throttle_x = True
            elif event.key == pygame.K_RIGHT:
                increase_throttle_x = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                increase_throttle_y = False
            elif event.key == pygame.K_DOWN: 
                decrease_throttle_y = False
            elif event.key == pygame.K_LEFT:
                decrease_throttle_x = False
            elif event.key == pygame.K_RIGHT:
                increase_throttle_x = False

    # Adjust throttle based on key state
    if increase_throttle_y:
        throttle_y += 1
    if decrease_throttle_y:
        throttle_y -= 1
    if increase_throttle_x:
        throttle_x += 1
    if decrease_throttle_x:
        throttle_x -= 1

    dt = clock.tick(60) / 1000.0  # 60 frames per second 
    font = pygame.font.Font(None,32)
    
    #if the temp is not correct, the pressure will not be and thus the density will not either
  
    atmosphere.temperature = atmosphere.cal_temperature(airship.ypos)
    
    atmosphere.pressure = atmosphere.cal_pressure(airship.ypos)
    
    atmosphere.density = atmosphere.cal_density()

    engines.thrust = engines.cal_engine_thrust(atmosphere.density,airship.yval)#this is the max thrust from ONE engine. 3m/s is a random value 
    engine_thrust_y = engines.thrust * (throttle_y / 100.0)
    engine_thrust_x = engines.thrust * (throttle_x / 100.0)
    
    #Calculate buoyancy force of the object
    bforce = BuoyancyData.cal_buoyancy_force(atmosphere.density,airship.volume)
    
    #Calculate the mass of the object in newtons which is mass * gravity
    force_gravity = BuoyancyData.cal_gravity_force(airship.mass)
    
    #drag on ship in X and Y axis
    ship_dragY = (atmosphere.density / 2) * airship.yval**2 * airship.cd * airship.lateral_area #< this needs to be the top surfacearea not the front since it's traveling up not forwards
    ship_dragX = (atmosphere.density / 2) * airship.xval**2 * airship.cd * airship.frontal_area
    
    #the net force is the difference between the two
    net_force_y = bforce - force_gravity - ship_dragY + (engine_thrust_y * airship.num_engines)
    net_force_x = (engine_thrust_x * airship.num_engines) - ship_dragX 
    
    #calculate acceleration which is the net force divided by the mass of the object
    acceleration_y = net_force_y / airship.mass
    acceleration_x = net_force_x / airship.mass
    
    #Update position and velocity. V is calculated bu taking the acceleration and multiplying it by the time.
    airship.yval += acceleration_y * dt
    airship.xval += acceleration_x * dt
    airship.ypos += airship.yval
    airship.xpos += airship.xval
    
    airrectangle.y = max(0, min(screen_height - airrectangle.height, airship.ypos))
    airrectangle.x = max(0, min(screen_width - airrectangle.width, airship.xpos))
    
    # Draw the rectangle on the screen
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, rectangle_color, airrectangle)

    draw_things()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit pygame
pygame.quit()

#NOTES
#Something in the calculation for pressure is not right, it's dropping way to fast and doesn't match the suposed altitude of ship
#Change the values to use consistant values, either all Kelvin or all Celcius
 