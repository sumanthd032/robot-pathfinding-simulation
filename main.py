import pygame
import random
from queue import PriorityQueue

# Initialize PyGame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600  # Dimensions of the window
CELL_SIZE = 30  # Size of each grid cell
GRID_WIDTH = WIDTH // CELL_SIZE  # Number of cells in width
GRID_HEIGHT = HEIGHT // CELL_SIZE  # Number of cells in height
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the display window
pygame.display.set_caption("Autonomous Path-Finding Robot Simulation")  # Title of the window

# Define colors used in the simulation
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BUTTON_COLOR = (50, 50, 200)  # Color for buttons

# Zone types: 0 = normal, 1 = safe, 2 = risky
SAFE_ZONE_COLOR = GREEN  # Color for safe zones
RISKY_ZONE_COLOR = RED    # Color for risky zones
NORMAL_ZONE_COLOR = WHITE  # Color for normal zones
BOT_COLOR = YELLOW        # Color for the robot
TARGET_COLOR = BLUE       # Color for the target

# Function to generate a random grid with zones
def generate_grid():
    grid = []
    for x in range(GRID_WIDTH):
        row = []
        for y in range(GRID_HEIGHT):
            zone_type = random.choice([0, 1, 2])  # Randomly assign zone type (normal, safe, risky)
            row.append(zone_type)
        grid.append(row)
    return grid

# Function to find a valid random target position that is not risky
def find_random_target(grid):
    while True:
        target_x = random.randint(0, GRID_WIDTH - 1)
        target_y = random.randint(0, GRID_HEIGHT - 1)
        # Ensure the target is not the start position and not in a risky zone
        if (target_x, target_y) != (0, 0) and grid[target_x][target_y] != 2:
            return (target_x, target_y)

grid = generate_grid()  # Generate the initial grid
target_position = find_random_target(grid)  # Get a random target position

# Dijkstra’s algorithm to find the shortest path while avoiding risky zones
def dijkstra(grid, start, end):
    distances = {start: 0}  # Initialize distances from start to all other points
    path = {}  # Store the path
    queue = PriorityQueue()  # Priority queue for processing nodes
    queue.put((0, start))  # Start processing from the starting position

    while not queue.empty():
        current_distance, current_position = queue.get()  # Get the node with the smallest distance

        if current_position == end:  # If we reach the destination
            break

        x, y = current_position
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Possible movements (up, down, left, right)
            nx, ny = x + dx, y + dy
            # Check if the new position is within bounds
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                # Only proceed if the zone is not risky
                if grid[nx][ny] != 2:
                    distance = current_distance + 1  # Calculate new distance
                    if (nx, ny) not in distances or distance < distances[(nx, ny)]:
                        distances[(nx, ny)] = distance  # Update the shortest distance
                        path[(nx, ny)] = current_position  # Track the path
                        queue.put((distance, (nx, ny)))  # Add to the queue

    # Reconstruct the path from end to start
    current = end
    path_seq = []
    while current != start:
        path_seq.append(current)
        current = path.get(current)  # Move backwards through the path
        if current is None:
            return []  # Return empty if no valid path
    path_seq.reverse()  # Reverse to get the path from start to end
    return path_seq

# Robot class with movement along path
class Robot:
    def __init__(self, start, end):
        self.position = start  # Current position of the robot
        self.end = end  # Target position
        self.path = dijkstra(grid, start, end)  # Calculate path to the target
        self.path_length = len(self.path)  # Length of the path
        self.index = 0  # Index to track current position in path

    def move(self):
        if self.index < len(self.path):  # Move along the path
            self.position = self.path[self.index]
            self.index += 1

# Set start point
start = (0, 0)

# Initialize robot
robot = Robot(start, target_position)  # Create a robot instance

# Function to draw the grid
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            color = NORMAL_ZONE_COLOR
            if grid[x][y] == 1:  # Safe zone
                color = SAFE_ZONE_COLOR
            elif grid[x][y] == 2:  # Risky zone
                color = RISKY_ZONE_COLOR
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw buttons on the screen
def draw_buttons(show_reconstruct):
    font = pygame.font.SysFont(None, 24)  # Font for buttons

    # Start button
    start_text = font.render("Start", True, WHITE)
    start_button_width = start_text.get_width() + 20
    start_button_height = start_text.get_height() + 10
    start_button = pygame.Rect(WIDTH // 4 - start_button_width // 2, HEIGHT - 80, start_button_width, start_button_height)
    pygame.draw.rect(screen, BUTTON_COLOR, start_button)  # Draw start button
    screen.blit(start_text, (start_button.x + 10, start_button.y + 5))  # Center the text in the button

    # Draw reconstruct button only if there is no valid path or the simulation has finished
    if show_reconstruct:
        reconstruct_text = font.render("Reconstruct", True, WHITE)
        reconstruct_button_width = reconstruct_text.get_width() + 20
        reconstruct_button_height = reconstruct_text.get_height() + 10
        reconstruct_button = pygame.Rect(3 * WIDTH // 4 - reconstruct_button_width // 2, HEIGHT - 80, reconstruct_button_width, reconstruct_button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, reconstruct_button)  # Draw reconstruct button
        screen.blit(reconstruct_text, (reconstruct_button.x + 10, reconstruct_button.y + 5))  # Center the text in the button
        return start_button, reconstruct_button
    
    return start_button, None

# Function to display information or messages on the screen
def display_info(message):
    font = pygame.font.SysFont(None, 24)  # Font for displaying messages
    text = font.render(message, True, BLUE)  # Render the message in blue color
    screen.blit(text, (10, HEIGHT - 30))  # Position the message at the bottom

# Main game loop
running = True
clock = pygame.time.Clock()  # Create a clock to control the frame rate
start_simulation = False  # Flag to check if simulation has started
show_reconstruct = False  # Flag to check if reconstruct button should be shown
finish_message = ""  # Message to display when the robot finishes
finish_timer = 0  # Timer to track how long to show the finish message

while running:
    screen.fill(BLACK)  # Clear the screen with a black background
    draw_grid()  # Draw the grid

    # Draw target and robot
    pygame.draw.rect(screen, TARGET_COLOR, (robot.end[0] * CELL_SIZE, robot.end[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Draw target
    pygame.draw.rect(screen, BOT_COLOR, (robot.position[0] * CELL_SIZE, robot.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Draw robot

    # Draw start and reconstruct buttons
    start_button, reconstruct_button = draw_buttons(show_reconstruct)

    # Check if the finish message should still be displayed
    if start_simulation:
        if robot.position == robot.end:  # If robot reaches the target
            finish_message = f"Finished! Path Length: {robot.path_length}"  # Set finish message
            finish_timer = pygame.time.get_ticks()  # Start the finish timer
            start_simulation = False  # Stop the simulation
            show_reconstruct = True  # Show the reconstruct button after finishing
        else:
            display_info(f"Moving to Target...")  # Update message while moving

    # Display finish message if available
    if finish_message and pygame.time.get_ticks() - finish_timer < 3000:  # Show for 3 seconds
        display_info(finish_message)
    elif pygame.time.get_ticks() - finish_timer >= 3000:
        finish_message = ""  # Clear finish message after 3 seconds

    # Display no path message if no valid path found
    if not robot.path and not start_simulation:
        display_info("No valid path for this maze. Please reconstruct.")
        show_reconstruct = True  # Show the reconstruct button if no valid path

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the window is closed
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button clicks
            if start_button.collidepoint(event.pos):  # If start button is clicked
                if robot.path:  # Only start if a valid path exists
                    start_simulation = True
                    show_reconstruct = False
            elif reconstruct_button and reconstruct_button.collidepoint(event.pos):  # If reconstruct button is clicked
                grid = generate_grid()  # Generate a new grid
                target_position = find_random_target(grid)  # Get a new random target position
                robot = Robot(start, target_position)  # Initialize robot with new target
                show_reconstruct = False  # Hide reconstruct button
                start_simulation = False  # Reset simulation

    # Move robot along the path if simulation has started
    if start_simulation:
        robot.move()  # Move the robot one step along the path

    pygame.display.flip()  # Update the display
    clock.tick(2)  # Slow down robot speed to 2 frames per second

pygame.quit()  # Exit the game when the loop ends
