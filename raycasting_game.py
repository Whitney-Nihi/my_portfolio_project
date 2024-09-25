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
        # Calculate ray angle
        ray_angle = start_angle + ray * DELTA_ANGLE
        ray_angle = normalize_angle(ray_angle)  # Ensure the angle stays between 0 and 2 * PI

        # Step in the direction of the ray and find the first wall it hits
        for depth in range(1, MAX_DEPTH):
            target_x = player_x + depth * math.cos(ray_angle)
            target_y = player_y + depth * math.sin(ray_angle)

            # Find which square in the map we're in
            map_x, map_y = int(target_x // TILE), int(target_y // TILE)

            # Check if we hit a wall
            if MAP[map_y][map_x] == '1':
                # Distance to the wall is adjusted to avoid fisheye effect
                adjusted_depth = depth * math.cos(player_angle - ray_angle)

                # Projected wall height
                proj_height = TILE * DISTANCE_PROJ_PLANE / (adjusted_depth + 0.0001)
                
                # Choose a color based on the wall hit (just using simple shades for now)
                if (map_x + map_y) % 2 == 0:
                    color = (255, 0, 0)  # Red for some walls
                else:
                    color = (0, 255, 0)  # Green for others

                # Draw the wall (vertical slice of the wall)
                pygame.draw.rect(screen, color, (ray * SCALE, SCREEN_HEIGHT // 2 - proj_height // 2, SCALE, proj_height))
                break  # Stop checking after the first wall hit

        start_angle += DELTA_ANGLE  # Move to the next ray

def normalize_angle(angle):
    while angle < 0:
        angle += 2 * math.pi
    while angle > 2 * math.pi:
        angle -= 2 * math.pi
    return angle


# Function to handle player movement
def handle_movement():
    keys = pygame.key.get_pressed()
    
    move_speed = 5  # Movement speed
    rot_speed = 0.05  # Rotation speed

    global player_x, player_y, player_angle

    if keys[pygame.K_w]:  # Move forward
        player_x += move_speed * math.cos(player_angle)
        player_y += move_speed * math.sin(player_angle)
    if keys[pygame.K_s]:  # Move backward
        player_x -= move_speed * math.cos(player_angle)
        player_y -= move_speed * math.sin(player_angle)
    if keys[pygame.K_a]:  # Rotate left
        player_angle -= rot_speed
    if keys[pygame.K_d]:  # Rotate right
        player_angle += rot_speed



# Main function
# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen
        handle_movement()  # Update player movement
        cast_rays(screen)  # Render the 3D walls

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()




if __name__ == "__main__":
    main()
