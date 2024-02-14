import pygame
import sys
from values import Airship, Atmosphere, Constants, Engine, BuoyancyData, Weapons
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
    actual_thrust_txt = font.render("Y-Thrust: {} N".format(engine_thrust_y * airship.num_engines),True,(0, 0, 0))
    throttle_y_txt = font.render("Y-Throttle: {} %".format(throttle_y),True,(0, 0, 0))
    actual_thrustX_txt = font.render("X-Thrust: {} N".format(engine_thrust_x * airship.num_engines),True,(0, 0, 0))
    throttle_x_txt = font.render("X-Throttle: {} %".format(throttle_x),True,(0, 0, 0))
    mouse_x_text = font.render("X-PosM: {} %".format(mouse_x),True,(0, 0, 0))
   # trust_txt = font.render("Engine Trust: {} m/s".format(trust),True,(0, 0, 0))
   
    screen.blit(alt_txt, (screen_width - 800, 20))
    screen.blit(acc_txt, (screen_width - 800, 60))
    screen.blit(vertvelo_txt, (screen_width - 800, 100))
    screen.blit(horvelo_txt, (screen_width - 800, 140))
    screen.blit(mass_txt, (screen_width - 800, 180))
    screen.blit(maxthrust_txt, (screen_width - 800, 220))
    screen.blit(actual_thrust_txt, (screen_width - 800, 260))
    screen.blit(throttle_y_txt, (screen_width - 800, 300))
    screen.blit(actual_thrustX_txt, (screen_width - 800, 340))
    screen.blit(throttle_x_txt, (screen_width - 800, 380))
    screen.blit(mouse_x_text, (screen_width - 800, 400))

# Define screen size
screen_width = 1200
screen_height = 1080
#based on the Bofors L/70
autocannon = Weapons(
    dry_mass = 24,
    barrel_length = 3.25,
    max_ammo = 300,
    type = 1, 
    mag_size = 20000,
    rate_of_fire = 4, # rounds per second
    catridge_mass = 0.096,
    reload_time = 2.5,
    muzzle_velocity = 100,
    crew_requirement = 4
)

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
    ballast =  91,
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
fire_weapon = False
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
            elif event.key == pygame.K_SPACE:
                fire_weapon = True
                pygame.draw.rect(screen,rectangle_color, (190, 200, 20,20))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                increase_throttle_y = False
            elif event.key == pygame.K_DOWN: 
                decrease_throttle_y = False
            elif event.key == pygame.K_LEFT:
                decrease_throttle_x = False
            elif event.key == pygame.K_RIGHT:
                increase_throttle_x = False
            elif event.key == pygame.K_SPACE:
                fire_weapon = False
    
    #get the mouse X/Y
    mouse_x, mouse_y = pygame.mouse.get_pos()
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
    
    projectiles = []
    
    autocannon.weapon_pos(airship.xpos,airship.ypos)
  

    autocannon.update_projectile()
    
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
    ship_dragY = airship.cal_drag_y(atmosphere.density)
    ship_dragX = airship.cal_drag_x(atmosphere.density)
    
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
    
    if fire_weapon:
        autocannon.fire_projectile()
        pygame.draw.circle(screen,rectangle_color,(int(autocannon.projectile.x), int(autocannon.projectile.y)), 5)
        
    draw_things()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit pygame
pygame.quit()

 