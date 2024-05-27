import pygame
pygame.init()

win = pygame.display.set_mode((500,480))
pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

bulletSound = pygame.mixer.Sound("bullet.mp3")
hitSound = pygame.mixer.Sound("Game_hit.mp3")

music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # The elements in the hitbox are (top left x, top left y, width, height)
    
    def draw(self,win):
        # We have 9 images for our walking animation, I want to show the same image for 3 frames
        # so I use the number 27 as an upper bound for walkCount because 27 / 3 = 9. 9 images shown
        # 3 times each animation.

        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if not(self.standing):
            if self.left: # If we are facing left
                win.blit(walkLeft[self.walkCount//3], (man.x,man.y))  # We integer divide walkCount by 3 to ensure each
                self.walkCount += 1                           # image is shown 3 times every animation
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (man.x,man.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255,0,0), self.hitbox,2) # To draw the hit box around the player
    
    def hit(self):            # After we are hit we are going to display a message to the screen for
        self.isJump = False   # a certain period of time
        self.jumpCount = 10
        self.x = 60 
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans",100)
        text = font1.render("-5", 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
            
class projectile(object):
    def __init__(self,x,y,radius,colour,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 8 * facing
    
    def draw(self,win):
        pygame.draw.circle(win, self.colour, (self.x,self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end] # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x+17, self.y+2, 31, 57)
        self.health = 10
        self.visable = True
    
    def draw(self, win):
        self.move()
        if self.visable:
            if self.walkCount + 1 >= 33: # Since we have 11 images for each animtion our upper bound is 33. 
                                        # We will show each image for 3 frames. 3 x 11 = 33.
                self.walkCount = 0
                
            if self.vel > 0: # If we are moving to the right we will display our walkRight images
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:  # Otherwise we will display the walkLeft images
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0],self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10-self.health)), 10))

            self.hitbox = (self.x + 17, self.y + 2, 31, 57) 
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2) # Draws the hit box around the enemy
            
    def move(self):
        if self.vel > 0:  # If we are moving right
            if self.x < self.path[1] + self.vel: # If we have not reached the furthest right point on our path.
                self.x += self.vel
            else: # Change direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else: # If we are moving left
            if self.x > self.path[0] - self.vel: # If we have not reached the furthest left point on our path
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
    
    def hit(self):  # This will display when the enemy is hit
        hitSound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visable = False
        print("hit")

def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render("Score: " + str(score), 1, (0,0,0))  # Arguments are: text, anti-aliasing, color
    win.blit(text, (10, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

# Main Loop
font = pygame.font.SysFont("comicsans", 30, True) # Font, Size, Bold
man = player(200, 410, 64,64)
goblin = enemy(100, 410, 64, 64, 300)
bullets = []
shootLoop = 0
goblin_respawn = 0
run = True
while run:
    clock.tick(27)

    if not goblin.visable:
        pygame.time.delay(10)
        goblin_respawn += 1
        if goblin_respawn >= 300:
            goblin_respawn = 0
            goblin.health = 10
            goblin.visable = True

    if goblin.visable:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 5:
        shootLoop = 0

    for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
        if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
            run = False  # Ends the game loop
    
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel # Moves the bullet by its vel
        else:
            bullets.pop(bullets.index(bullet)) # This will remove the bullet if it is off the screen
        
        if goblin.visable:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:  # Checks x coords
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]: # Checks y coords
                    goblin.hit()  # calls enemy hit method
                    score += 1
                    bullets.pop(bullets.index(bullet)) # removes bullet from bullet list

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
            bulletSound.play()

            if man.left:
                facing = -1
            else:
                facing = +1
            
            if len(bullets) < 5:  # This will make sure we cannot exceed 5 bullets on the screen at once
                bullets.append(projectile(round(man.x+man.width//2), round(man.y+man.height//2), 6, (0,0,0), facing))
                # This will create a bullet starting at the middle of the character

    if keys[pygame.K_LEFT] and man.x > man.vel:  # Making sure the top left position of our character is greater than our vel so we never move off the screen.
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < 500 - man.vel - man.width: # Making sure the top right corner of our character is less than the screen width - its width 
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    
    else:  # If the character is not moving we will set both left and right false and reset the animation counter (walkCount)
        man.standing = True
        man.walkCount = 0 

    if not(man.isJump):  # Checks is user is not jumping  
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else: # This will execute if our jump is finished
            man.jumpCount = 10
            man.isJump = False
            # Resetting our Variables
    

    redrawGameWindow()

pygame.quit()  # If we exit the loop this will execute and close our game