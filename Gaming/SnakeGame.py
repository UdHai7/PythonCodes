#Importing modules to build snake game
import pygame
import sys
import random
import time

#Checking intialization errors (6,0)
check_errors=pygame.init()
if check_errors[1]>0:
	print ("(!) Had {0} initializing errors,exiting...".format(check_errors[1]))
	sys.exit(-1)
else:
	print("Pygame successfully initialized")

#Playing Surface
PlaySurface=pygame.display.set_mode((720,460))
pygame.display.set_caption('Snake Game!')
time.sleep(10)

#Colors
red=pygame.Color(255,0,0) #Game Over
green=pygame.Color(0,255,0) #Body of Snake
black=pygame.Color(0,0,0) #Score
white=pygame.Color(255,255,255) #Background
blue=pygame.Color(0,0,255) #Food

#FPS(Frames Per Second) Controller
fpsController=pygame.time.Clock()

#Imp Variables
snakePos=[200,50]
snakeBody=[[200,50],[190,50],[180,50]]

foodPos=[random.randrange(1,72)*10,random.randrange(1,46)*10]
foodSpawn=True

direction='RIGHT'
changeto=direction
score=0

#Game Over func()
def gameOver():
	GOFont=pygame.font.SysFont('Arial',72)
	GOsurf=GOFont.render('Game Over',True,red)
	GOrect=GOsurf.get_rect()
	GOrect.midtop=(360,15)
	PlaySurface.blit(GOsurf,GOrect)
	ShowScore(0)
	pygame.display.flip()
	time.sleep(4)
	pygame.quit() #Pygame exit
	sys.exit() #Console exit


#Show Score func()
def ShowScore(choice=1):
	SSFont=pygame.font.SysFont('Arial',25)
	SSsurf=SSFont.render('Score : {0}'.format(score),True,black)
	SSrect=SSsurf.get_rect()
	if choice==1:
		SSrect.midtop=(80,10)
	else:
		SSrect.midtop=(360,120)
	PlaySurface.blit(SSsurf,SSrect)


while True:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			if event.key==pygame.K_LEFT or event.key==ord('a'):
				changeto='LEFT'
			if event.key==pygame.K_RIGHT or event.key==ord('d'):
				changeto='RIGHT'
			if event.key==pygame.K_UP or event.key==ord('w'):
				changeto='UP'				
			if event.key==pygame.K_DOWN or event.key==ord('s'):
				changeto='DOWN'
			if event.key==pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))

	#Validating direction
	if changeto=='RIGHT' and not direction =='LEFT':
		direction='RIGHT'
	if changeto=='LEFT' and not direction =='RIGHT':
		direction='LEFT'
	if changeto=='UP' and not direction =='DOWN':
		direction='UP'
	if changeto=='DOWN' and not direction =='UP':
		direction='DOWN'


	#Updating snake positions[x,y]
	if direction == 'RIGHT':
		snakePos[0] +=10
	if direction == 'LEFT':
		snakePos[0] -=10
	if direction == 'UP':
		snakePos[1] -=10
	if direction == 'DOWN':
		snakePos[1] +=10


	#Snake Body Mechanism
	snakeBody.insert(0,list(snakePos))
	if snakePos[0]==foodPos[0] and snakePos[1]==foodPos[1]:
		score +=1
		foodSpawn=False
	else:
		snakeBody.pop()
	if foodSpawn==False:
		foodPos=[random.randrange(1,72)*10,random.randrange(1,46)*10]
	foodSpawn=True

	#Playing surface background
	PlaySurface.fill(white)

	#Snake
	for pos in snakeBody:
		pygame.draw.rect(PlaySurface,green,pygame.Rect(pos[0],pos[1],10,10))

	#Food
	pygame.draw.rect(PlaySurface,blue,pygame.Rect(foodPos[0],foodPos[1],10,10))

	# #Hitting the boundary
	if snakePos[0] > 710 or snakePos[0] < 0:
	 	gameOver()
	if snakePos[1] > 450 or snakePos[1] < 0:
		gameOver()

	#Hitting body itself
	for block in snakeBody[1:]:
		if snakePos[0] == block[0] and snakePos[1] == block[1]:
			gameOver()

	ShowScore()
	pygame.display.flip()
	fpsController.tick(15)