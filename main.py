import serial
import pygame

joystick = serial.Serial("/dev/cu.usbserial-A600etVk", 9600)

pygame.init()
pygame.display.set_caption("Kart Game")
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()

class Kart:

    image = pygame.image.load("kart.png")
    x = (screen.get_width() / 2) - (image.get_width() / 2) #horizontal center
    y = screen.get_height() - (image.get_height() * 2)       #vertical bottom
    max_speed = 100 #pixels/frame
    speed_rate = 0 #...1

    def speed(self): #pixels/frame
        return self.max_speed * self.speed_rate

    def move(self):
        self.y -= self.speed()
    
        # move wrap
        if self.y < -self.image.get_height():
            self.y = screen.get_height()
        elif self.y > screen.get_height():
            self.y = -self.image.get_height()

kart = Kart()

pygame.mixer.music.load('horn.mp3')
horning = 0

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not running:
        break

    joystick.write(b'P')
    pot =  int(joystick.readline())
    kart.speed_rate = pot / 1023

    kart.move()

    if horning == 0:
        joystick.write(b'B')
        if int(joystick.readline()):
            horning = 15
            pygame.mixer.music.play(0)
    else:
        horning -= 1

    screen.fill((150,206,180))
    screen.blit(kart.image, (kart.x, kart.y))

    pygame.display.update()
    clock.tick(30) #frames/second

joystick.close()