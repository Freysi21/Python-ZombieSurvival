#special thanks to Julian Meyer the 13 year old, this is built on his project
#that you can find here
#http://www.raywenderlich.com/24252/beginning-game-programming-for-teens-with-python



# 1 - Import library
import pygame
from pygame.locals import *
import math
import random

# 2 - Initialize
keys = [False, False, False, False]
playerpos=[100,100]
acc=[0,0]
bullets=[]
ammo = 100
grenadeAmmo = 5
grenades = []
badtimer=100
badtimer1=0
zombies=[]
deadZombies = []
babies = []
healthvalue=194
lost = False
kills = 0
isBaby = False
spawnAmmo = 500
spawnGrenade = 650

ammoPos = (0, 0)
grenadePos = (0, 0)

gPickUp = False
aPickUp = False


walking = 0






grenadeImg = pygame.image.load('resources/images/grenadeAmmo.png')
ammoImg = pygame.image.load('resources/images/ammo.png')
baby = pygame.image.load('resources/images/baby.png')
player = pygame.image.load('resources/images/playerWithBaby.png')
zombieImg = pygame.image.load('resources/images/zombie.png')
grass = pygame.image.load("resources/images/grass.png")
deadZombieImg = pygame.image.load('resources/images/deadZombie.png')
bullet = pygame.image.load('resources/images/bullet.png')
bomb = pygame.image.load('resources/images/grenade.png')
gameover = pygame.image.load("resources/images/gameover1.png")
health = pygame.image.load("resources/images/health.png")
healthbar = pygame.image.load("resources/images/healthbar.png")

twoBabiesNames = ["resources/images/playerWithBabies.png",'resources/images/playerWithBabiesL.png', 'resources/images/playerWithBabiesR.png']
oneBabyNames = ['resources/images/playerWithBaby.png','resources/images/playerWithBabyL.png','resources/images/playerWithBabyR.png']
NoBabyNames = [] #To draw

boom_names = ["resources/images/e1.tiff", "resources/images/e2.tiff", "resources/images/e3.tiff",
			"resources/images/e4.tiff","resources/images/e5.tiff","resources/images/e6.tiff",
			"resources/images/e7.tiff","resources/images/e8.tiff","resources/images/e9.tiff",
			"resources/images/e10.tiff","resources/images/e11.tiff","resources/images/e12.tiff",
			"resources/images/e13.tiff","resources/images/e14.tiff","resources/images/e15.tiff",
			"resources/images/e16.tiff","resources/images/e17.tiff","resources/images/e18.tiff",
			"resources/images/e19.tiff","resources/images/e20.tiff","resources/images/e21.tiff",
			"resources/images/e22.tiff","resources/images/e23.tiff","resources/images/e24.tiff",]

twoBabies = []
oneBaby = []
boom_imgs = []

for img in twoBabiesNames:
	twoBabies.append(pygame.image.load(img))
for img in oneBabyNames:
	oneBaby.append(pygame.image.load(img))
for img in boom_names:
	boom_imgs.append(pygame.image.load(img))

pygame.init()
width, height = 1024, 768
screen=pygame.display.set_mode((width, height))
pygame.mixer.init()

myWalkNum = 0

# 3 - Game Loop
running = 1
exitcode = 0
ticks = 0
explosion_slide = -1
babyTicks = 0
babyLanded = False
ammoTicks = 0
grenadeTicks = 0
while running:
	badtimer -= 1
	# 4 - clear
	screen.fill(0)
	# 5 - Draw bodies
	for x in range(width//grass.get_width()+1):
		for y in range(height//grass.get_height()+1):
			screen.blit(grass,(x*100,y*100))
	for zombie in deadZombies:
		screen.blit(deadZombieImg, zombie)

	# Check if ammo should be spawned
	if ammoPos != (0, 0) and not aPickUp:
		screen.blit(ammoImg, ammoPos)
	if grenadePos != (0, 0) and not gPickUp:
		screen.blit(grenadeImg, grenadePos)
	
	if ammoTicks == spawnAmmo:
		ammoPos = (random.randint(1,width - 1), random.randint(1, height - 1))
		screen.blit(ammoImg, ammoPos)
		ammoTicks = 0
		aPickUp = False

	if grenadeTicks == spawnGrenade:
		grenadePos = (random.randint(1, width - 1), random.randint(1, height - 1))
		screen.blit(grenadeImg, grenadePos)
		grenadeTicks = 0
		gPickUp = False

	# 5.1  draw the player position
	position = pygame.mouse.get_pos()
	angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
	if myWalkNum < 10:
		player = oneBaby[0]
	elif myWalkNum < 20:
		player = oneBaby[1]
	elif myWalkNum < 30:
		player = oneBaby[2]
	else:
		myWalkNum = 0
	playerrot = pygame.transform.rotate(player, 360-angle*57.29)
	playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
	screen.blit(playerrot, playerpos1)
	playerRect = pygame.Rect(player.get_rect())
	playerRect.top=playerpos1[1]
	playerRect.left=playerpos1[0]
	if playerRect.collidepoint(ammoPos):
		ammoPos = (0,0)
		ammo += 100
		aPickUp = True
	if playerRect.collidepoint(grenadePos):
		grenadePos = (0,0)
		grenadeAmmo += 10 
		gPickUp = True
	# 5.1.1 draw the baby 
	print (len(babies))
	if len(babies) > 0:
		print(ticks)
		if babyTicks < 30:
			for babe in babies:
				babyTicks += 1
				velx=math.cos(babe[0])*5
				vely=math.sin(babe[0])*5
				babe[1]+=velx
				babe[2]+=vely
				for projectile in babies:
					baby1 = pygame.transform.rotate(baby, 360 - projectile[0]*57.29)
					#baby1 = pygame.transform.scale(baby, projectile[1]*BabyScale, projectile[])
					screen.blit(baby1, (projectile[1],projectile[2]))
		else:
			screen.blit(baby, (babies[0][1], babies[0][2]))
			babyLanded = True
	# 5.2 draw bullets
	for bull in bullets:
		index=0
		velx=math.cos(bull[0])*10
		vely=math.sin(bull[0])*10
		bull[1]+=velx
		bull[2]+=vely
		if bull[1]<-64 or bull[1]>width or bull[2]<-64 or bull[2]>height:
			bullets.pop(index)
		index+=1
		for projectile in bullets:
			screen.blit(bullet, (projectile[1], projectile[2]))
	# 5.2.2 draw grenade
	if explosion_slide == -1:
		for boom in grenades:
			index = 0
			velx=math.cos(boom[0])*5
			vely=math.sin(boom[0])*5
			boom[1]+=velx
			boom[2]+=vely
			index+=1
			ticks += 1
			for projectile in grenades:
				grenade1 = pygame.transform.rotate(bomb, 360 - projectile[0]*57.29)
				screen.blit(grenade1, (projectile[1],projectile[2]))
	# 5.2.3 draw explosion
	if explosion_slide > -1:
		if explosion_slide >23:
			grenades.pop()
			explosion_slide = -1
			ticks = 0
		else:
			boom = grenades[0]
			screen.blit(boom_imgs[explosion_slide], (boom[1] - 50, boom[2] - 50))
			explosion_slide += 1

	# 5.3 draw zombies
	if badtimer == 0:
		zombies.append([-50, random.randint(-50,height + 50)])
		zombies.append([width + 50, random.randint(-50,height + 50)])
		zombies.append([random.randint(-50,width + 50), -50])
		zombies.append([random.randint(0,width + 50), height + 50])

		badtimer=100-(badtimer1*2)
		if badtimer1>=35:
			badtimer1=35
		else:
			badtimer1+=5
	index=0
	for zombie in zombies:
		if not isBaby:
			if playerpos[1] - 25 > zombie[1]:
				zombie[1] += 2
			else:
				zombie[1] -= 2
			if playerpos[0] - 25 > zombie[0]:
				zombie[0] += 2
			else:
				zombie[0] -= 2
		else:
			if babies[0][2] + 3 > zombie[1]:
				zombie[1] += 2
			else:
				zombie[1] -= 2
			if babies[0][1] > zombie[0]:
				zombie[0] += 2
			else:
				zombie[0] -= 2

		#zombiepos1 = (zombie[0]-zombierot.get_rect().width/2, zombie[1]-zombierot.get_rect().height/2)
		#zombie[0] = zombiepos1[0]
		#zombie[1] = zombiepos1[1]
		# 5.3.1 - Attack player
		badrect=pygame.Rect(zombieImg.get_rect())
		badrect.top=zombie[1]
		badrect.left=zombie[0]
		#5.3.2 - Check collisions

		if babyLanded and len(babies) > 0:
			babe = babies[0]
			babeRect = pygame.Rect(baby.get_rect())
			babeRect.top = babe[1]
			babeRect.left = babe[2]
			tmp = (babe[1], babe[2] + 3)
			if badrect.collidepoint(tmp):
				babies.remove(babe)
				babyLanded = False
				babyTicks = 0
				isBaby = False
		if ticks > 30:
			if explosion_slide == -1:
				explosion_slide = 0
			else:
				grenade = grenades[0]
				boomRect = pygame.Rect(boom_imgs[17].get_rect())
				boomRect.top = grenade[2]
				boomRect.left = grenade[1]
				if badrect.colliderect(boomRect):
					deadZombies.append(zombie)
					zombies.remove(zombie)
					kills += 1
					continue

		index1 = 0
		for bull in bullets:
			bullrect = pygame.Rect(bullet.get_rect())
			bullrect.left = bull[1]
			bullrect.top = bull[2]
			if badrect.colliderect(bullrect):
				acc[0]+=1
				kills += 1
				deadZombies.append(zombies.pop(index))
				bullets.pop(index1)
			index1 += 1

		tmp = (playerpos1[0] + 25, playerpos1[1] + 25)
		if badrect.collidepoint(tmp):
			healthvalue -= 5
			deadZombies.append(zombies.pop(index))
		# 5.3.3 - Next zombie
		if not isBaby:
			angle = math.atan2(playerpos[1]-(zombie[1]+32),playerpos[0]-(zombie[0]+26))
		else:
			angle = math.atan2(babies[0][2]-(zombie[1]+32),babies[0][1]-(zombie[0]+26))
		zombierot = pygame.transform.rotate(zombieImg, 360-angle*57.29)
		screen.blit(zombierot, zombie)
		index += 1

    # 5.4 - Draw Score
	font = pygame.font.Font(None, 24)
	survivedtext = font.render("Zombies Killed: " + str(kills), True, (255,255,255))
	textRect = survivedtext.get_rect()
	textRect.topright=[635,5]
	screen.blit(survivedtext, textRect)

    # 5.4 - Draw Ammo
	if ammo > 0:
		font = pygame.font.Font(None, 24)
		Ammo = font.render("Ammo: " + str(ammo), True, (255,255,255))
		textRect = Ammo.get_rect()
		textRect.topright=[800,5]
		screen.blit(Ammo, textRect)
	else:
		font = pygame.font.Font(None, 24)
		Ammo = font.render("Ammo: " + str(ammo), True, (255,0,0))
		textRect = Ammo.get_rect()
		textRect.topright=[800,5]
		screen.blit(Ammo, textRect)		
	# 5.4 - Draw GrenadeAmmo
	if grenadeAmmo > 0:
		font = pygame.font.Font(None, 24)
		gAmmo = font.render("Ammo: " + str(grenadeAmmo), True, (255,255,255))
		textRect = gAmmo.get_rect()
		textRect.topright=[900,5]
		screen.blit(gAmmo, textRect)
	else:
		font = pygame.font.Font(None, 24)
		gAmmo = font.render("Ammo: " + str(grenadeAmmo), True, (255,0,0))
		textRect = gAmmo.get_rect()
		textRect.topright=[900,5]
		screen.blit(gAmmo, textRect)		
	#5.5 - Draw health
	screen.blit(healthbar, (5,5))
	for health1 in range(healthvalue):
		screen.blit(health, (health1+8,8))	
	# 6 - update screen
	pygame.display.flip()
	# 7 - loop through events
	for event in pygame.event.get():
		# check if the event is the X button
		if event.type==pygame.QUIT:
			pygame.quit()
			exit(0)
		if event.type == pygame.KEYDOWN:
			if event.key==K_w:
				walking += 1
				keys[0]=True
			elif event.key==K_a:
				keys[1]=True
			elif event.key==K_s:
				walking += 1
				keys[2]=True
			elif event.key==K_d:
				keys[3]=True
			elif event.key==K_e:
				if len(grenades) < 1 and grenadeAmmo > 0:
					grenadeAmmo -= 1
					position = pygame.mouse.get_pos()
					grenades.append([math.atan2(position[1]-(playerpos1[1]+32),
						position[0]-(playerpos1[0]+26)),
						playerpos1[0]+32,playerpos1[1]+32])
			elif event.key==K_q:
				if len(babies) < 1:
					posistion = pygame.mouse.get_pos()
					babies.append([math.atan2(position[1]-(playerpos1[1]+32),
						position[0]-(playerpos1[0]+26)),
						playerpos1[0]+32,playerpos1[1]+32])
					isBaby = True
		if event.type == pygame.KEYUP:
			if event.key==pygame.K_w:
				keys[0]=False
			elif event.key==pygame.K_a:
				keys[1]=False
			elif event.key==pygame.K_s:
				keys[2]=False
			elif event.key==pygame.K_d:
				keys[3]=False
			elif event.key==pygame.K_w and event.key.K_s:
				walking = 1
		if event.type==pygame.MOUSEBUTTONDOWN:
			if ammo > 0:
				ammo -= 1
				position=pygame.mouse.get_pos()
				acc[1]+=1
				bullets.append([math.atan2(position[1]-(playerpos1[1]+32),
							position[0]-(playerpos1[0]+26)),
							playerpos1[0]+32,playerpos1[1]+32])   	
	myWalkNum += 1

	# 8 - Move player
	if keys[0]:
		playerpos[1]-=5
	elif keys[2]:
		playerpos[1]+=5
	if keys[1]:
		playerpos[0]-=5
	elif keys[3]:
		playerpos[0]+=5
	# 9 - Check if player is dead
	if healthvalue <= 0:
		running = 0
		exitcode = 1
		if acc[1]!=0:
			accuracy=acc[0]*1.0/acc[1]*100
		else:
			accuracy = 0
	ammoTicks += 1
	grenadeTicks += 1

if exitcode:
	pygame.font.init()
	font = pygame.font.Font(None, 24)
	text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,0,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.blit(gameover, (0,0))
	screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()



