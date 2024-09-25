import pygame
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FOV = math.pi / 3  # 60 degrees field of view
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DISTANCE_PROJ_PLANE = (SCREEN_WIDTH // 2) / math.tan(HALF_FOV)
SCALE = SCREEN_WIDTH // NUM_RAYS

# Map (1 = wall, 0 = empty space)
MAP = [
    '11111111',
    '10001001',
    '10101001',
    '10000001',
    '10000001',
    '10101001',
    '10000001',
    '11111111'
]
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)
TILE = SCREEN_WIDTH // MAP_WIDTH

# Player attributes
player_x = 3 * TILE  # Start at x = 3 tiles from the left
player_y = 3 * TILE  # Start at y = 3 tiles from the top
player_angle = math.pi / 2  # Initial angle facing "east"



# Function to cast rays
def cast_rays(screen):
    start_angle = player_angle - HALF_FOV  # Starting angle for the raycasting

    

    for ray in range(NUM_RAYS):
        ray_angle = start_angle + ray * DELTA_ANGLE
        ray_angle = normalize_angle(ray_angle)

        for depth in range(1, MAX_DEPTH):
            target_x = player_x + depth * math.cos(ray_angle)
            target_y = player_y + depth * math.sin(ray_angle)

            map_x, map_y = int(target_x // TILE), int(target_y // TILE)

            if MAP[map_y][map_x] == '1':
                adjusted_depth = depth * math.cos(player_angle - ray_angle)

                # Wall height projection
                proj_height = TILE * DISTANCE_PROJ_PLANE / (adjusted_depth + 0.0001)

                # Check wall orientation based on map indices
                if (target_x // TILE) % 2 == 0:  # North-South walls
                    color = (200, 0, 0)  # Red for North-South walls
                else:  # East-West walls
                    color = (0, 200, 0)  # Green for East-West walls

                pygame.draw.rect(screen, color, (ray * SCALE, SCREEN_HEIGHT // 2 - proj_height // 2, SCALE, proj_height))
                break

    # Textures for Walls
    wall_texture = pygame.image.load('wall_texture.png')
    
    # Texture-based wall rendering
    tex_width, tex_height = wall_texture.get_size()

    # Inside cast_rays function (replacing the solid color wall rendering)
    texture_x = int((target_x % TILE) / TILE * tex_width)
    texture_slice = wall_texture.subsurface(texture_x, 0, 1, tex_height)

    # Scale the texture slice to the height of the projected wall
    texture_slice = pygame.transform.scale(texture_slice, (SCALE, int(proj_height)))

    # Draw the texture slice on the screen
    screen.blit(texture_slice, (ray * SCALE, SCREEN_HEIGHT // 2 - proj_height // 2))
            

    start_angle += DELTA_ANGLE

        


def normalize_angle(angle):
    while angle < 0:
        angle += 2 * math.pi
    while angle > 2 * math.pi:
        angle -= 2 * math.pi
    return angle


# Function to handle player movement
def handle_movement():
    keys = pygame.key.get_pressed()

    move_speed = 5
    rot_speed = 0.05

    global player_x, player_y, player_angle

    if keys[pygame.K_w]:  # Move forward
        new_x = player_x + move_speed * math.cos(player_angle)
        new_y = player_y + move_speed * math.sin(player_angle)
        if MAP[int(new_y // TILE)][int(new_x // TILE)] == '0':  # Check for collision
            player_x, player_y = new_x, new_y
    if keys[pygame.K_s]:  # Move backward
        new_x = player_x - move_speed * math.cos(player_angle)
        new_y = player_y - move_speed * math.sin(player_angle)
        if MAP[int(new_y // TILE)][int(new_x // TILE)] == '0':
            player_x, player_y = new_x, new_y
    if keys[pygame.K_a]:  # Rotate left
        player_angle -= rot_speed
    if keys[pygame.K_d]:  # Rotate right
        player_angle += rot_speed


def draw_minimap(screen):
    map_scale = 8  # Scale down the map for the minimap
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            color = (200, 200, 200) if MAP[y][x] == '1' else (50, 50, 50)
            pygame.draw.rect(screen, color, (x * map_scale, y * map_scale, map_scale, map_scale))

    # Draw player on minimap
    pygame.draw.circle(screen, (255, 0, 0), (int(player_x // TILE * map_scale), int(player_y // TILE * map_scale)), 5)

    # Draw player's field of view
    pygame.draw.line(screen, (255, 255, 0), 
                     (player_x // TILE * map_scale, player_y // TILE * map_scale),
                     ((player_x + 50 * math.cos(player_angle)) // TILE * map_scale, 
                      (player_y + 50 * math.sin(player_angle)) // TILE * map_scale), 2)


# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        handle_movement()  # Handle player movement
        screen.fill((135, 206, 235))  # Fill screen with a sky-blue color

        cast_rays(screen)  # Cast rays and draw walls
        draw_minimap(screen)  # Draw minimap

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Maintain 60 FPS



    pygame.quit()




if __name__ == "__main__":
    main()
