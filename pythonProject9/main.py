import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1200, 1000))
color1 = 'Blue'
color = screen.fill(color1)
pygame.display.set_caption("Music Player")
time_array = [0]

musicList = ["Song1.ogg", "Song2.ogg", "Song3.ogg"]

timeList = []
global paused
paused = False
colorcount = 0

font = pygame.font.SysFont("Comic Sans", 32)

text = font.render("SPACE TO PAUSE, RIGHT ARROW TO PLAY, CLICK TO SKIP SONG", False, (180, 180, 180))
text_x = text.get_width()
text_y = text.get_height()

surface1 = pygame.surface.Surface((text_x, text_y))
surface1.blit(text, (0,0))

global current_rect

class Button(pygame.sprite.Sprite):
    def __init__(self, posx, posy, file1, file2):
        global current_rect
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.file1 = file1
        self.file2 = file2
        self.image = pygame.image.load(file1)
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)
        current_rect = self.rect
    def update(self, currently_paused):
        global current_rect
        if currently_paused == False:
            self.image = pygame.image.load(self.file1)
            self.rect = self.image.get_rect()
            self.rect.center = (self.posx, self.posy)
            current_rect = self.rect
            button_group.draw(screen)
            pygame.display.flip()

        else:
            self.image = pygame.image.load(self.file2)
            self.rect = self.image.get_rect()
            self.rect.center = (self.posx, self.posy)
            button_group.draw(screen)
            current_rect = self.rect
            pygame.display.flip()

last_pressed = [0]
global click
click = False

def mouse_collision(rectangle):
    mousevents = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    collisionbool = rectangle.collidepoint(mouse_pos)
    if collisionbool == True and click == True:
        ##I used to have a time elapsed bool above, checking if currenttime - lasttime click was changed > 0.2. This was
        ##dumb, as think about it: as your running the code you are checking 2 conditions side by side in original code
        #1) is mouse_collision = true(both pos of mouse and click = true), is click = False
        ## then pause
        #2) is mouse_collision = true and is paused = True
        ## then play
        ##problem being, if you check time elapsed within the mouse_collision method, you are checking the time elapsed since the function was last called
        ##thus, lets say you have already ran 1 time. Pause is now == True(because in previous iteration mouse_collision returned TRUE and paused = False)
        #so, in iteration 2, assume the time check is within mouse_collision, and that sufficient time has elapsed
        #in this situation, first 1) will be ran, and mouse_collision will return TRUE(thus adding current_time to time array), but the condition will not
        #be met, because PAUSE = TRUE. However, the method is still CALLED, and as a result, bc sufficient time has elapsed and collisionbool = TRUE and click = TRUE,
        #the method will successfully return true and append the currenttime to timelist
        #this is very bad, bc now, when we call #2 in the second iteration, this condition #2 was SUPPOSED TO RUN. But it will not longer run, because mouse_collision
        #will return FALSE. Why? Because, in the previous calling of mouse_collision within this SAME iteration, mouse collision already was TRUE
        #Thus, the time.time() appended to timearray is very very very very marginally smaller than current time because of the very small time elapsed since last calling
        #As a result, this function will return FALSE and our play method will never be run
        return True
    else:
        return False

def click_statesetter(eventlist):
    global click
    print("HERE")
    for j in eventlist:
        print("J IS", j)
        if j.type == pygame.MOUSEBUTTONDOWN:
            if j.button == 1:
                click = True
        else:
            click = False



Button1 = Button(600,500, "Pause.png", "Play.png")

button_group = pygame.sprite.GroupSingle()
button_group.add(Button1)





def colorchange():
    global colorcount
    colorlist = ['Blue', 'Red', 'Purple', 'Green']
    color = screen.fill(colorlist[colorcount])
    colorcount = colorcount + 1
    if colorcount == len(colorlist) - 1:
        colorcount = 0



def checkquit():
    global eventlist
    eventlist = pygame.event.get()
    for event in eventlist:
        if event.type == pygame.QUIT:
            raise SystemExit

def pause():
    global eventlist
    global paused
    global seconds
    global sub
    print("pausd is", paused)
    keys = pygame.key.get_pressed()
    ###in construction
    click_statesetter(eventlist)





    ###inconstruction
    if mouse_collision(Button1.rect) and paused == False and time.time() - last_pressed[-1] > 0.2:
        last_pressed.append(time.time())
        print("runnning")
        seconds = 0
        sub = 0
        paused = True
        button_group.update(paused)
        pygame.mixer.music.pause()
#### you may ask: if we end up running this once(in the scenario where space is hit and pause = false), wouldn't
#### it be futile because the next iteration paused will be true?
#### NO! because even though pause is true, when paused() is called again, all that will happen is it will check
#### if condition 1(space = true and pause = false) is true, and since pause = True it is not true so this will not be run
#### it will check the second condition, and when it checks it will not run either because the player has not hit the up button yet
#### so it works really well bc we keep the sub variable at 0 until the point where paused = False again
    elif mouse_collision(Button1.rect) == True and paused == True and time.time() - last_pressed[-1] > 0.2:
        last_pressed.append(time.time())
        print("running1")
        seconds = 1
        paused = False
        button_group.update(paused)
        pygame.mixer.music.unpause()




def timer(t):
    global seconds
    global subtractor
    global paused
    screen.blit(surface1, (0,0))
    #no flip needed, button group automatically takes what is drawn to screen and flips to user in the next line
    button_group.update(paused)
    seconds = 1
    while t > 0:
        start_time = time.time()
        mouseevent = pygame.mouse.get_pressed()
        pygame.display.update()
        checkquit()
        ##time.sleep(seconds)
        print("start time is", start_time, "time.time() is", time.time())

        if mouseevent[2] == True:
            print("running mouseevent")
           ## time_array.append(time.time())
          ##  if time_array[-1] - time_array[-2] > 1:
            if time.time() - time_array[-1] > 0.5:
                print("a second has elapsed since last pause")
                t = 0
                paused = False
                ## if we skip a song, we want pause to go back to False so we can display pause img
                time_array.append(time.time())
                print("the newest time at which we have pause has been added to the time array list")
                print("this list's purpose is to append the various times at which we skip songs so that we can")
                print("make sure that the time time a(current skip) - time x(previous skip) is greater than 1")
                print("this means one second has elapsed since the last skip, and this prevents multiple clicks in a short time")
                print("from resulting in a quick succession of skips")

        else:
            subtractor = time.time() - start_time
            pause()
            if paused == True:
                subtractor = sub

            t = t - subtractor
            print(t)

def getlistofsonglengths():
    for i in musicList:
        peek = pygame.mixer.Sound(i)
        print("length",(peek.get_length()))
        timeList.append((peek.get_length()))


songcounter = 0

def getTitle(a):
    title = ''
    for i in a:
        if i == '.':
            break
        else:
            title = title + i
    return(title)

def playMusic():
    getlistofsonglengths()
    pygame.display.update()
    global songcounter
    for i in musicList:
        colorchange()
        music = pygame.mixer.music.load(musicList[songcounter])
        pygame.mixer.music.play()
        pygame.display.set_caption(getTitle(musicList[songcounter]))
        timewaited = int(timeList[songcounter])
        timer(timewaited)
        songcounter = songcounter + 1
        print("Reach here", songcounter)

playMusic()