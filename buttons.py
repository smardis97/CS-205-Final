import pygame
from constants import *
import sys
import random

sys.path.insert(0, '..')

pygame.font.init()

class BUTTONS:

    def __init__(self):
        pygame.init()
        self.smallFont = pygame.font.Font('freesansbold.ttf', 20)
        self.width = pygameWindowWidth
        self.depth = pygameWindowDepth
        self.screen = pygame.display.set_mode((pygameWindowWidth, pygameWindowDepth))
        self.programState = 0
        self.musicState = True
        self.dice1 = random.randint(1,6)
        self.dice2 = random.randint(1,6)
        self.distance = 18
        # What do these numbers mean/refer to?
        self.circleX = 295 + 910 - 140 - 70 + 1 + 69 + self.distance
        self.circleY = 910 - 140 + 1 + self.distance
        self.circleRadius = self.distance
        self.enterYourName = "Enter your name"
        self.enterSwitch = False

    def drawButtons(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # start
        if self.width / 2 + 50 > mouse[0] > self.width / 2 - 50 and 250 > mouse[1] > 200:
            pygame.draw.rect(self.screen, lightGreen, (self.width / 2 - 50, 200, 100, 50))
        else:
            pygame.draw.rect(self.screen, green, (self.width / 2 - 50, 200, 100, 50))
        # dice button
        if self.width / 2 + 50 > mouse[0] > self.width / 2 - 50 and 325 > mouse[1] > 275:
            pygame.draw.rect(self.screen, lightBlue, (self.width/2-50, 275, 100, 50))
            if click[0] == 1:
                sumDice = self.dice1 + self.dice2
                print("sumdice is",sumDice)
                while sumDice > 0:
                    if self.circleX != 1065 + self.distance - 630 and self.circleY == 771 + self.distance and sumDice != 0:
                        self.circleX -= 70
                        sumDice -= 1
                        print(sumDice)
                    # blue one near corner
                    if self.circleX == 1065 + self.distance - 630 and self.circleY == 771+self.distance and sumDice != 0:
                        self.circleX -= 2 * self.distance
                        sumDice-=1
                        print(sumDice)
                    if self.circleX == 1065 + self.distance - 630 - 2 * self.distance and self.circleY != 771 + self.distance - 630 and sumDice != 0:
                        self.circleY -= 70
                        sumDice -= 1
                        print(sumDice)
                    # light blue near corner
                    if self.circleX == 1065 + self.distance - 630 - 2 * self.distance and self.circleY == 771 + self.distance - 630 and sumDice != 0:
                        self.circleY -= 2 * self.distance
                        sumDice -= 1
                        print(sumDice)
                    if self.circleX != 1065 + self.distance - 2 * self.distance and self.circleY == 771+self.distance - 630 - 2 * self.distance and sumDice != 0:
                        self.circleX += 70
                        sumDice -= 1
                        print(sumDice)
                    # orange near corner
                    if self.circleX == 1065 + self.distance - 2 * self.distance and self.circleY == 771 + self.distance - 630 - 2 * self.distance and sumDice != 0:
                        self.circleX += 2 * self.distance
                        sumDice -= 1
                        print(sumDice)
                    if self.circleX == 1065 + self.distance and self.circleY != 771 + self.distance - 2 * self.distance and sumDice != 0:
                        self.circleY += 70
                        sumDice -= 1
                        print(sumDice)
                    # yellow near corner
                    if self.circleX == 1065 + self.distance and self.circleY == 771 + self.distance - 2 * self.distance and sumDice != 0:
                        self.circleY += 2 * self.distance
                        sumDice -= 1
                        print(sumDice)
                self.dice1 = random.randint(1, 6)
                self.dice2 = random.randint(1, 6)
        else:
            pygame.draw.rect(self.screen, blue, (self.width / 2 - 50, 275, 100, 50))
        # reset
        if self.width / 2 + 50 > mouse[0] > self.width / 2 - 50 and 400 > mouse[1] > 350:
            pygame.draw.rect(self.screen, lightGreen, (self.width / 2 - 50, 350, 100, 50))
            if click[0] == 1:
                self.circleX = 295 + 910 - 140 - 70 + 1 + 69 + self.distance
                self.circleY = 910 - 140 + 1 + self.distance
        else:
            pygame.draw.rect(self.screen, green, (self.width / 2 - 50, 350, 100, 50))
        # quit
        if self.width / 2 + 50 > mouse[0] > self.width / 2 - 50 and 475 > mouse[1] > 425:
            pygame.draw.rect(self.screen, lightBlue, (self.width / 2 - 50, 425, 100, 50))
        else:
            pygame.draw.rect(self.screen, blue, (self.width / 2 - 50, 425, 100, 50))

        startSurf, startRect = self.textObjects("Start",self.smallFont)
        diceSurf, diceRect = self.textObjects("Dice",self.smallFont)
        resetSurf, resetRect = self.textObjects("Reset",self.smallFont)
        quitSurf, quitRect = self.textObjects("Quit",self.smallFont)


        startRect.center=(self.width / 2, 200 + 25)
        diceRect.center=(self.width / 2, 275 + 25)
        resetRect.center=(self.width / 2, 350 + 25)
        quitRect.center=(self.width / 2, 425 + 25)

        self.screen.blit(startSurf, startRect)
        self.screen.blit(diceSurf, diceRect)
        self.screen.blit(resetSurf, resetRect)
        self.screen.blit(quitSurf, quitRect)

    def homeButtons(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # start
        if self.width / 2 + 100 > mouse[0] > self.width / 2 - 100 and 570 > mouse[1] > 470:
            pygame.draw.rect(self.screen, lightGreen, (self.width / 2 - 100, 470, 200, 100))
            if click[0] == 1:
                self.programState = 1
        else:
            pygame.draw.rect(self.screen, green, (self.width / 2 - 100, 470, 200, 100))
        # music
        if self.width / 2 - 200 > mouse[0] > self.width / 2 - 400 and 570 > mouse[1] > 470:
            pygame.draw.rect(self.screen, lightBlue, (self.width / 2 - 400, 470, 200, 100))
            if click[0] == 1 and self.musicState:
                pygame.mixer.music.pause()
                self.musicState = False
            elif click[0] == 1 and not self.musicState:
                pygame.mixer.music.unpause()
                self.musicState = True

        else:
            pygame.draw.rect(self.screen, blue, (self.width / 2 - 400, 470, 200, 100))
        # quit
        if self.width / 2 + 400 > mouse[0] > self.width / 2 + 200 and 570 > mouse[1] > 470:
            pygame.draw.rect(self.screen, lightBlue, (self.width / 2 + 200, 470, 200, 100))
            if click[0] == 1:
                pygame.display.quit()
                pygame.quit()
                exit()
        else:
            pygame.draw.rect(self.screen, blue, (self.width / 2 + 200, 470, 200, 100))

        startSurf, startRect = self.textObjects("Start",self.smallFont)
        musicSurf, musicRect = self.textObjects("Music",self.smallFont)
        quitSurf, quitRect = self.textObjects("Quit",self.smallFont)


        startRect.center=(self.width / 2 - 100 + 100, 470 + 50)
        musicRect.center=(self.width / 2 - 400 + 100, 470 + 50)
        quitRect.center=(self.width / 2 + 200 + 100, 470 + 50)

        self.screen.blit(startSurf, startRect)
        self.screen.blit(musicSurf, musicRect)
        self.screen.blit(quitSurf, quitRect)

    def textObjects(self,text,font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
    def enterUserName(self,username):
        print(username)
        graph = pygame.image.load('images/enterName.jpg')
        graph = pygame.transform.scale(graph, (910, 700))
        self.screen.blit(graph, (290, 100))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # start
        if self.width / 2 + 100 > mouse[0] > self.width / 2 - 100 and 470 > mouse[1] > 370:
            pygame.draw.rect(self.screen, lightGreen, (self.width / 2 - 100, 370, 200, 100))
            if click[0] == 1:
                self.enterSwitch = True
        else:
            pygame.draw.rect(self.screen, green, (self.width / 2 - 100, 370, 200, 100))
        if self.enterSwitch:
            self.enterYourName = username

        startSurf, startRect = self.textObjects(self.enterYourName,self.smallFont)
        startRect.center=(self.width / 2 - 100 + 100, 370 + 50)
        self.screen.blit(startSurf, startRect)


    def plainBase(self,username):
        ####################################### tile_bounds list ###############################################################
        graph = pygame.image.load('images/monopoly_768*768.png')
        self.screen.blit(graph, ((1280-768)/2, 0))


        board_size = 768
        margin_x = (pygameWindowWidth-board_size)/2
        margin_y = 768
        corner_width = 104
        tile_width = 62

        first_corner_left_top = (pygameWindowWidth-margin_x-corner_width,pygameWindowDepth-corner_width)
        first_corner_right_bottom = (pygameWindowWidth-margin_x,pygameWindowDepth)
        tile_bounds = [(first_corner_left_top,first_corner_right_bottom)]
        for i in range(0,9):
            tile_bounds.append(((pygameWindowWidth-margin_x-corner_width-tile_width-tile_width*i,pygameWindowDepth-corner_width), (pygameWindowWidth-margin_x-corner_width-tile_width*i,pygameWindowDepth)))
        second_corner_left_top = (margin_x,pygameWindowDepth-corner_width)
        second_corner_right_bottom = (margin_x+corner_width,pygameWindowDepth)
        tile_bounds.append((second_corner_left_top,second_corner_right_bottom))
        for i in range(0,9):
            left_tile_left_top = (margin_x, pygameWindowDepth - corner_width-tile_width-tile_width*i)
            left_tile_right_bottom = (margin_x + corner_width, pygameWindowDepth-corner_width-tile_width*i)
            tile_bounds.append((left_tile_left_top, left_tile_right_bottom))
        third_corner_left_top = (margin_x,0)
        third_corner_right_bottom = (margin_x+corner_width,corner_width)
        tile_bounds.append((third_corner_left_top,third_corner_right_bottom))
        for i in range(0,9):
            top_tile_left_top = (margin_x+corner_width+tile_width*i, 0)
            top_tile_right_bottom = (margin_x + corner_width + tile_width + tile_width*i, corner_width)
            tile_bounds.append((top_tile_left_top, top_tile_right_bottom))
        fourth_corner_left_top = (margin_x+pygameWindowDepth-corner_width,0)
        fourth_corner_right_bottom = (margin_x+pygameWindowDepth,corner_width)
        tile_bounds.append((fourth_corner_left_top,fourth_corner_right_bottom))
        for i in range(0,9):
            right_tile_left_top = (margin_x + pygameWindowDepth - corner_width, 0+corner_width+tile_width*i)
            right_tile_right_bottom = (margin_x + pygameWindowDepth, corner_width+tile_width*(i+1))
            tile_bounds.append((right_tile_left_top, right_tile_right_bottom))
        # print(len(tile_bounds))
        # print(tile_bounds)
        # for i in range(0,40):
        #     print(tile_bounds[i])
        #     print(tile_bounds[i][0])
        #     pygame.draw.line(self.screen,red,(tile_bounds[i][0]),(tile_bounds[i][1]))

        ##########################################################################################################################
        #
        # board_size = 768
        # margin_x = (pygameWindowWidth-board_size)/2
        # margin_y = board_size
        # corner_width = 104
        # tile_width = 64
        # blank_tile_width = 59

        # ## right-bottom corner tile
        # pygame.draw.line(self.screen,red,(margin_x+board_size-corner_width,board_size-corner_width),(margin_x+board_size,board_size))
        # ## bottom 9 tiles
        # pygame.draw.line(self.screen,red,(margin_x+board_size-corner_width-tile_width,board_size-corner_width),(margin_x+board_size-corner_width,board_size))
        # pygame.draw.line(self.screen,red,(margin_x+board_size-corner_width-tile_width-blank_tile_width,board_size-corner_width),(margin_x+board_size-corner_width-tile_width,board_size))
        # pygame.draw.line(self.screen,red,(margin_x+board_size-corner_width-tile_width*2-blank_tile_width,board_size-corner_width),(margin_x+board_size-corner_width-tile_width-blank_tile_width,board_size))
        # pygame.draw.line(self.screen,red,(margin_x+board_size-corner_width-tile_width*2-blank_tile_width*2,board_size-corner_width),(margin_x+board_size-corner_width-tile_width*2-blank_tile_width,board_size))
        # pygame.draw.line(self.screen,red,(margin_x+board_size-corner_width-tile_width*3-blank_tile_width*2,board_size-corner_width),(margin_x+board_size-corner_width-tile_width*2-blank_tile_width*2,board_size))
        # pygame.draw.line(self.screen,red,(margin_x+board_size-corner_width-tile_width*4-blank_tile_width*2+2,board_size-corner_width),(margin_x+board_size-corner_width-tile_width*3-blank_tile_width*2,board_size))
        # pygame.draw.line(self.screen,red,(margin_x+board_size-corner_width-tile_width*5-blank_tile_width*2+3,board_size-corner_width),(margin_x+board_size-corner_width-tile_width*4-blank_tile_width*2,board_size))
        # pygame.draw.line(self.screen,red,(margin_x+corner_width+tile_width,board_size-corner_width),(margin_x+corner_width+tile_width*2-4,board_size))
        # pygame.draw.line(self.screen,red,(margin_x+corner_width,board_size-corner_width),(margin_x+corner_width+tile_width,board_size))



        # pygame.draw.rect(self.screen, backgroundGreen, (295, 0, 910, 910))
        # # each rectangle 70*140
        # for i in range(0,10):
        #     pygame.draw.line(self.screen, (0, 0, 0), [295+140+i*70, 0], [295+140+i*70, 140])
        #     pygame.draw.line(self.screen, (0, 0, 0), [295, 140+i*70], [295+140, 140+i*70])
        #     pygame.draw.line(self.screen, (0, 0, 0), [295+140+i*70, 910-140], [295+140+i*70, 910])
        #     pygame.draw.line(self.screen, (0, 0, 0), [295+910-140, 140+i*70], [pygameWindowWidth-295, 140+i*70])
        # pygame.draw.lines(self.screen, (0, 0, 0), True, [(295+140,140),(295+140,910-140),(295+910-140,910-140),(295+910-140,140)])
        # ## eight colors rectangles
        # ## small rectangle size 70*15
        # smallDepth = 35
        # # green
        # pygame.draw.rect(self.screen, green, (295+910-140-70+1, 910-140+1, 69, smallDepth))
        # pygame.draw.rect(self.screen, green, (295+910-140-70*2+1, 910-140+1, 69, smallDepth))
        # pygame.draw.rect(self.screen, green, (295+910-140-70*4+1, 910-140+1, 69, smallDepth))
        #
        # # blue
        # pygame.draw.rect(self.screen, blue, (295+140+1, 910-140+1, 69, smallDepth))
        # pygame.draw.rect(self.screen, blue, (295+140+70*2+1, 910-140+1, 69, smallDepth))
        #
        # # brown
        # pygame.draw.rect(self.screen, brown, (295+140-smallDepth, 910-140-70+1, smallDepth, 69))
        # pygame.draw.rect(self.screen, brown, (295+140-smallDepth, 910-140-70*3+1, smallDepth, 69))
        #
        # # lightblue
        # pygame.draw.rect(self.screen, slightBlue, (295+140-smallDepth, 140+1, smallDepth, 69))
        # pygame.draw.rect(self.screen, slightBlue, (295+140-smallDepth, 140+70+1, smallDepth, 69))
        # pygame.draw.rect(self.screen, slightBlue, (295+140-smallDepth, 140+70*3+1, smallDepth, 69))
        #
        # # purple
        # pygame.draw.rect(self.screen, purple, (295+140+1, 140-smallDepth, 69, smallDepth))
        # pygame.draw.rect(self.screen, purple, (295+140+70*2+1, 140-smallDepth, 69, smallDepth))
        # pygame.draw.rect(self.screen, purple, (295+140+70*3+1, 140-smallDepth, 69, smallDepth))
        #
        # # orange
        # pygame.draw.rect(self.screen, orange, (295+910-140-70+1, 140-smallDepth, 69, smallDepth))
        # pygame.draw.rect(self.screen, orange, (295+910-140-70*2+1, 140-smallDepth, 69, smallDepth))
        # pygame.draw.rect(self.screen, orange, (295+910-140-70*4+1, 140-smallDepth, 69, smallDepth))
        #
        # # red
        # pygame.draw.rect(self.screen, red, (295+910-140+1, 140+1, smallDepth, 69))
        # pygame.draw.rect(self.screen, red, (295+910-140+1, 140+70*2+1, smallDepth, 69))
        # pygame.draw.rect(self.screen, red, (295+910-140+1, 140+70*3+1, smallDepth, 69))
        #
        # # yellow
        # pygame.draw.rect(self.screen, yellow, (295+910-140+1, 910-140-70+1, smallDepth, 69))
        # pygame.draw.rect(self.screen, yellow, (295+910-140+1, 910-140-70*3+1, smallDepth, 69))
        # pygame.draw.rect(self.screen, yellow, (295+910-140+1, 910-140-70*4+1, smallDepth, 69))
        #
        # helloUser = "Hello "+ username
        # usernameFont = pygame.font.Font('freesansbold.ttf', 20)
        # welcome = usernameFont.render(helloUser,False,(0, 0, 0))
        # self.screen.blit(welcome,(20,20))