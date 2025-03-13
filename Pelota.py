import pygame
import math
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pelotas TikTok Estilo")

# Colores
BLACK = (0, 0, 0)
BRIGHT_COLORS = [(255, 100, 0), (0, 255, 100), (100, 0, 255), (255, 200, 0), (0, 200, 255)]  # Colores vivos

# Radio del círculo grande (centro en el medio de la pantalla)
CIRCLE_RADIUS = 300
CENTER = (WIDTH // 2, HEIGHT // 2)

# Clase para las pelotas
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(5, 15)  # Tamaño aleatorio
        self.color = random.choice(BRIGHT_COLORS)  # Color vivo aleatorio
        self.vx = random.uniform(-7, 7)  # Velocidad más rápida en x
        self.vy = random.uniform(-7, 7)  # Velocidad más rápida en y

    def move(self):
        # Actualizar posición
        self.x += self.vx
        self.y += self.vy

        # Calcular distancia al centro
        dx = self.x - CENTER[0]
        dy = self.y - CENTER[1]
        distance = math.sqrt(dx * dx + dy * dy)

        # Si toca el borde del círculo grande, rebota y genera una nueva pelota
        if distance + self.radius >= CIRCLE_RADIUS:
            # Normalizar el vector de dirección
            norm_dx = dx / distance
            norm_dy = dy / distance
            # Invertir la componente perpendicular al borde
            dot = self.vx * norm_dx + self.vy * norm_dy
            self.vx -= 2 * dot * norm_dx
            self.vy -= 2 * dot * norm_dy
            # Ajustar posición pa' que no se salga
            self.x = CENTER[0] + norm_dx * (CIRCLE_RADIUS - self.radius)
            self.y = CENTER[1] + norm_dy * (CIRCLE_RADIUS - self.radius)
            return True  # Indica que tocó el borde
        return False  # No tocó el borde

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# Lista de pelotas (inicia con una sola)
balls = [Ball(WIDTH // 2, HEIGHT // 2)]  # Comienza con una pelota en el centro

# Bucle principal
clock = pygame.time.Clock()
running = True
MAX_BALLS = 200  # Límite pa' no colapsar

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mover y dibujar pelotas
    screen.fill(BLACK)  # Fondo negro
    pygame.draw.circle(screen, (255, 0, 0), CENTER, CIRCLE_RADIUS, 2)  # Círculo rojo

    for ball in balls[:]:  # Usamos una copia pa' modificar la lista durante el bucle
        if ball.move() and len(balls) < MAX_BALLS:  # Si toca el borde y no se excede el límite
            # Generar una nueva pelota cerca del punto de contacto
            new_ball = Ball(ball.x + random.uniform(-20, 20), ball.y + random.uniform(-20, 20))
            balls.append(new_ball)  # Añadir nueva pelota
        ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()