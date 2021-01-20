import pygame
import math
import random
pygame.init()
screenHeight = 720
screenWidth = 1080
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("<--- Python")
clock = pygame.time.Clock()

colours = [(50,50,50), (255,0,0), (255,85,0), (255,208,0), (0,171,6), (0,255,179), (0,42,255), (111,0,255), (255,0,221), (255, 110, 250), (255,255,255)]

#pygame.mouse.set_visible(False)
#pygame.mouse.set_pos([0,0])
#draws mouse crosshair
#pygame.draw.line(screen, (255,0,0), [mousex + 9, mousey], [mousex - 8, mousey], 2)
#pygame.draw.line(screen, (255,0,0), [mousex, mousey + 9], [mousex, mousey - 8], 2)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100 
        self.r = 14

    
    def updateEnemy(self, px, py):
        #move
        dx = (self.x - px) 
        dy = (self.y - py) 
        hyp = math.sqrt(dx**2 + dy**2)
        xvelo = -((dx / hyp) * 1) 
        yvelo = -((dy / hyp) * 1)
        self.x += xvelo
        self.y += yvelo

        #draw
        if not self.health == 0:
            pygame.draw.circle(screen, colours[self.health % len(colours)], [self.x, self.y], self.r)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xmoveSpd = 0
        self.ymoveSpd = 0
        self.shotSpeed = 10

    def updatePlayer(self):
        #move
        self.x += self.xmoveSpd
        self.y += self.ymoveSpd

        #draw
        pygame.draw.circle(screen, (255,255,255), [self.x, self.y], 10)

class Bullet:
    def __init__(self, x, y, mousex, mousey):
        self.x = x
        self.y = y
        #There must be a nicer way to do this. Maybe in the mousedown event?
        self.x2 = mousex
        self.y2 = mousey
        dx = (self.x - self.x2) 
        dy = (self.y - self.y2) 
        hyp = math.sqrt(dx**2 + dy**2)
        self.xvelo = -((dx / hyp) * 12) + random.randint(-1,1)
        self.yvelo = -((dy / hyp) * 12) + random.randint(-1,1)
    def updateBullet(self):
        #move
        self.x += self.xvelo
        self.y += self.yvelo

        #draw teh bullet
        pygame.draw.rect(screen, (255,255,255), [(self.x), (self.y), 3, 3] )

def Main(): 
    # Loop until the user clicks the close button.
    frameCount = 0
    done = False
    player = Player(200, 200)
    bullets = []
    enemies = []
    isShooting = False
    shotCD = 0

    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                pygame.quit()  # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.ymoveSpd = -5
                if event.key == pygame.K_a:
                    player.xmoveSpd = -5
                if event.key == pygame.K_s:
                    player.ymoveSpd = 5
                if event.key == pygame.K_d:
                    player.xmoveSpd = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.ymoveSpd = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.xmoveSpd = 0 

            if event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append(Bullet(player.x, player.y, mousex, mousey))
                shotCD = 0
                isShooting = True
            if event.type == pygame.MOUSEBUTTONUP:
                isShooting = False
        
        pos = pygame.mouse.get_pos()
        mousex = pos[0]
        mousey = pos[1]

        if isShooting:
            shotCD += 1 
            if shotCD > player.shotSpeed:
                bullets.append(Bullet(player.x, player.y, mousex, mousey))
                bullets.append(Bullet(player.x, player.y, mousex, mousey))
                bullets.append(Bullet(player.x, player.y, mousex, mousey))
                bullets.append(Bullet(player.x, player.y, mousex, mousey))
                shotCD = 0

        if frameCount % 50 == 0:
            enemies.append(Enemy(random.randint(0,1000), random.randint(0,700)))

        
        screen.fill((0,0,0))


        #update player
        player.updatePlayer()

        #update enemies
        for e in enemies:
            e.updateEnemy(player.x, player.y)
            if e.health <= 0:
                enemies.remove(e)
                player.shotSpeed -= 1
        
        #update bullets
        for b in bullets:
            b.updateBullet()
            #check if bullet hit an enemy
            for e in enemies:
                if b.x > e.x - e.r and b.x < e.x + e.r and b.y > e.y - e.r and b.y < e.y + e.r:
                    e.health -= 1
                    try:
                        bullets.remove(b) 
                    except ValueError:
                        continue
        #Remove offscreen bullets
            if b.x > screenWidth + 200 or b.x < -200 or b.y > screenHeight + 200 or b.y < -200:
                bullets.remove(b)
                
        


        frameCount += 1
        pygame.display.flip()
        clock.tick(60)


Main()

