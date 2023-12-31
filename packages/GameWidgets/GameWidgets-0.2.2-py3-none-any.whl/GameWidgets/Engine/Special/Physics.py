import pygame
import sys

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PhysicsObject:
    def __init__(self, position, mass=1.0):
        self.position = position
        self.mass = mass
        self.velocity = Vec2D(0, 0)
        self.forces = Vec2D(0, 0)

    def update(self, delta_time):
        raise NotImplementedError("Subclasses must implement the update method.")

class Circle(PhysicsObject):
    def __init__(self, position, radius, mass=1.0):
        super().__init__(position, mass)
        self.radius = radius

    def update(self, delta_time):
        # Gravity
        self.forces.x += world.gravity.x * self.mass
        self.forces.y += world.gravity.y * self.mass

        # Air resistance
        self.forces.x -= world.air_resistance * self.velocity.x
        self.forces.y -= world.air_resistance * self.velocity.y

        # Update velocity using Newton's second law
        self.velocity.x += self.forces.x / self.mass * delta_time
        self.velocity.y += self.forces.y / self.mass * delta_time

        # Update position using the new velocity
        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time

        # Reset forces for the next iteration
        self.forces.x = 0
        self.forces.y = 0

class Rectangle(PhysicsObject):
    def __init__(self, position, width, height, mass=1.0):
        super().__init__(position, mass)
        self.width = width
        self.height = height

    def update(self, delta_time):
        # Gravity
        self.forces.x += world.gravity.x * self.mass
        self.forces.y += world.gravity.y * self.mass

        # Air resistance
        self.forces.x -= world.air_resistance * self.velocity.x
        self.forces.y -= world.air_resistance * self.velocity.y

        # Update velocity using Newton's second law
        self.velocity.x += self.forces.x / self.mass * delta_time
        self.velocity.y += self.forces.y / self.mass * delta_time

        # Update position using the new velocity
        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time

        # Reset forces for the next iteration
        self.forces.x = 0
        self.forces.y = 0

class PhysicsWorld:
    def __init__(self, gravity=Vec2D(0, -9.8), air_resistance=0.02):
        self.gravity = gravity
        self.air_resistance = air_resistance
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self, delta_time):
        for obj in self.objects:
            obj.update(delta_time)

# Constants for Pygame
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def convert_world_to_screen(pos):
    scale_factor = 50  # Adjust this value based on your needs
    return int(pos.x * scale_factor) + SCREEN_WIDTH // 2, SCREEN_HEIGHT - int(pos.y * scale_factor)

def draw_objects(screen, objects):
    for obj in objects:
        if isinstance(obj, Circle):
            pygame.draw.circle(screen, RED, convert_world_to_screen(obj.position), int(obj.radius * 50))
        elif isinstance(obj, Rectangle):
            rect_pos = convert_world_to_screen(Vec2D(obj.position.x - obj.width / 2, obj.position.y - obj.height / 2))
            rect_size = (int(obj.width * 50), int(obj.height * 50))
            pygame.draw.rect(screen, BLUE, (rect_pos, rect_size))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Physics Simulation")

    world = PhysicsWorld()

    circle = Circle(position=Vec2D(0, 0), radius=1.0, mass=2.0)
    world.add_object(circle)

    rectangle = Rectangle(position=Vec2D(2, 0), width=2.0, height=1.0, mass=1.5)
    world.add_object(rectangle)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_objects(screen, world.objects)
        pygame.display.flip()

        # Simulate for 1 second with small time steps
        time_step = 0.01
        num_iterations = int(1 / time_step)

        for _ in range(num_iterations):
            world.update(time_step)

        clock.tick(60)  # Adjust the frame rate as needed

if __name__ == "__main__":
    main()
