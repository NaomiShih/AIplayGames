# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:35:15 2021

@author: USER
"""

import pygame
from pygame.locals import*
import time
import random
from playsound import playsound






life = pygame.image.load('./assets/LIFE123.PNG')
player = pygame.image.load('./assets/playerNomal.png')

Normal = pygame.image.load('./assets/playerNomal.png')
Board = pygame.image.load('./assets/normal.png')
Nails = pygame.image.load('./assets/nails.png')


RIGHT1 = pygame.image.load('./assets/playerR1.png')
RIGHT2 = pygame.image.load('./assets/playerR2.png')

LEFT1 = pygame.image.load('./assets/playerL1.png')
LEFT2= pygame.image.load('./assets/playerL2.png')
wall =  pygame.image.load('./assets/wall.png')
ceil = pygame.image.load('./assets/ceiling.png')
TrampolineUP = pygame.image.load('./assets/trampolineUP.png')
TrampolineDown = pygame.image.load('./assets/trampolineDown.png')
conveyor_left = pygame.image.load('./assets/conveyor_left1.png')
conveyor_right = pygame.image.load('./assets/conveyor_right1.png')

ImgList = {'life'  : life, 'player' : player, 'Normal' : Normal, 'Board' : Board,
           'Nails' : Nails, 'RIGHT1' :RIGHT1, 'RIGHT2' : RIGHT2,'LEFT1' : LEFT1, 
           'LEFT2' : LEFT2, 'wall'  : wall,  'ceil' :ceil, 'TrampolineUP' : TrampolineUP, 'TrampolineDown' : TrampolineDown,
           'conveyor_left' : conveyor_left , 'conveyor_right' : conveyor_right }






pygame.init()
pygame.mixer.init()

FPS = 100#設定幀數
width, height = 480, 640 #把螢幕長寬變數丟進去
screen = pygame.display.set_mode((width, height))#設定螢幕長寬
pygame.display.set_caption('小朋友下樓梯')#設定視窗名稱




lef = 0#判斷往左兩個動作的參數
rig = 0#判斷往右兩個動作的參數
keys =  [False, False, False, False]#設定上下左右判定的list
CountF = 0#設定往下樓層的變數

Xlist  = []#紀錄每個X值
Ylist  = []#紀錄每個y值
Kindlist = []#紀錄每個板子的種類
count = 0#刷新板子亂數
count2 = 0
# 宣告 font 文字物件

# 渲染方法會回傳 surface 物件

# blit 用來把其他元素渲染到另外一個 surface 上，這邊是 window 視窗



class player:
    def __init__(self, X, Y, HP, img):
        self.X = X
        self.Y = Y
        self.HP = HP
        self.img = img
        
    


    def player_fall(player):
        player.Y += 1
        
    def player_stop_fall(player):
        player.Y -= 1.5
    def player_stop_float(player):
        player.Y += 11




class Platform:
    def __init__(self, X, Y, dmg, img):
        self.X = X
        self.Y = Y
        self.dmg = dmg
        self.img = img    
    def Platform_float(Board):
        Board.Y -= 0.5
        if Board.Y < 100:
        
            Board.X = random.randint(0, 350)
            Board.Y = 640
    def Platform_bounce(self, player):
        player.Y -= 60
    def Platform_right(self, player):
        player.X += 0.5
    def Platform_left(self, player):
        player.X -= 0.5
    def Platform_Rect(Platform, Player, PlatWidth, PlatHigth, PlayerWidth, PlayerHight):
        PlatformRect  = pygame.Rect(Platform.X, Platform.Y , PlatWidth, PlatHigth)
        PlayerRect    = pygame.Rect(Player.X, Player.Y, PlayerWidth, PlayerHight)
        if (pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1 and Platform.img == ImgList['ceil'] ):
            player.player_stop_float(Player)
        elif(pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1):
            player.player_stop_fall(Player)
            
            if (Platform.img == ImgList['TrampolineUP']):
                Platform.Platform_bounce(Player)
            if(Platform.img == ImgList['conveyor_right']):
                Platform.Platform_right(Player)
                
            if(Platform.img == ImgList['conveyor_left']):
                Platform.Platform_left(Player)
    def SetPlatform(times, platformtime, platform):#幾秒要生成 BOARDTIME 板子生成時間
        if (platformtime > times):
            screen.blit(platform.img, (platform.X, platform.Y))
            Platform.Platform_float(platform)
        
            
        
    def Platform_damage(Board, player):
        pass
        
  
for i in range(0, 100, 1):           
    X = random.randint(30, 365)
    Xlist.append(X)

player1 = player(240, 120, 12,ImgList['player'] )
RandX = random.randint(0, 99)


Board1  = Platform(Xlist[count], 600, 0, ImgList['Board'] )
count += 1
Nails1   = Platform(Xlist[count], 600, 0,ImgList['Nails'] )
count += 1
Board2  = Platform(Xlist[count], 600, 0, ImgList['Board'] )
count += 1
Trampoline  = Platform(Xlist[count], 600, 0, ImgList['TrampolineUP'] )
count += 1
ceil = Platform(20, 80, 0, ImgList['ceil'] )
count += 1
conveyor_left = Platform(Xlist[count], 600, 0, ImgList['conveyor_left'] )
count += 1
conveyor_right = Platform(Xlist[count], 600, 0, ImgList['conveyor_right'] )
count += 1


tcount =0
HPflag = 1

while 1:
    
    ##環境設定
    
    screen.fill((0, 0, 0))#把畫布塗黑
    print(player1.HP)
    
    platformtime = pygame.time.get_ticks()#設定一個計時器 單位為毫秒
    times = platformtime % 2500#計時器每2.5秒歸0
    
    
    #print(boardtime)#測試秒數到哪裡 程式有沒有預期跑
    if times < 3 and player1.Y <= 640:
        CountF += 1
    elif player1.Y >= 640:
         playsound('./assets/sounds/Fall 2.mp3', block=True)
         pygame.quit()
    head_font = pygame.font.SysFont(None, 60)#設定大小60的標題框框
    text_surface = head_font.render('B%04dF'%CountF, True, (121, 255, 121))#設定標題的字跟顏色
    screen.blit(text_surface, (300, 25))#讓標題印在畫布300,25的地方
    # 5 - clear the screen before drawing it again
    #screen.fill((0, 0, 0))
    # 6 - draw the screen elements
    for x in range (80, 700, 100):#設定牆壁 以及生命值
        screen.blit(ImgList['wall'],  (0, x))
        screen.blit(ImgList['wall'],  (460, x))
    
    screen.blit(player1.img, (player1.X, player1.Y))#設定玩家
    screen.blit(ImgList['ceil'],  (20, 80))
    screen.blit(ImgList['ceil'],  (55, 80))
    screen.blit(ImgList['life'],  (10, 0))
    
    
    
    player.player_fall(player1)
    
    playerRect  = pygame.Rect(player1.X, player1.Y, 20, 31)#畫出PLAYER1的碰撞範圍
    Platform.Platform_Rect(ceil, player1, 480, 32, 20, 31)
   
 
    WallRect  = pygame.Rect(0, 80, 18, 560)
    WallRect2  = pygame.Rect(450, 80, 15, 560)

    
    if (pygame.Rect.colliderect(playerRect, WallRect) == 1 ):
        
         player1.X  += 8
    if (pygame.Rect.colliderect(playerRect, WallRect2) == 1 ):
         
         player1.X  -= 8
    
    
  
   

    Platform.SetPlatform(0 , platformtime,Board1 )
    Platform.Platform_Rect(Board1, player1, 94, 1, 20, 31)
    
    Platform.SetPlatform(1000 , platformtime,Trampoline )#設定彈簧
    Platform.Platform_Rect(Trampoline, player1, 95, 1, 20, 31)
    #Platform.Platform_bounce(player1)
    Platform.SetPlatform(1500, platformtime, conveyor_left)
    Platform.Platform_Rect(conveyor_left, player1, 95, 1, 20, 31)
    Platform.SetPlatform(2500 , platformtime,Board2 )
    Platform.Platform_Rect(Board2, player1, 94, 1, 20, 31)

    Platform.SetPlatform(500 , platformtime,Nails1 )
    Platform.Platform_Rect(Nails1, player1, 95, 1, 20, 31)
    
    Platform.SetPlatform(3250, platformtime, conveyor_right)
    Platform.Platform_Rect(conveyor_right, player1, 95, 1, 20, 31)
    
  
    

                
            
  
    pygame.display.flip()#環境更新


    #操控角色    
    for event in pygame.event.get():
        if player1.Y > 640:
            
           
            exit(0)       

        if event.type == pygame.KEYDOWN:#左
            if event.key==K_LEFT:
                keys[2]=True
                keys[3]=False
                        
        if event.type == pygame.KEYDOWN:#右
            if event.key==K_RIGHT:
                keys[3]=True
                keys[2]=False
    
        else :
            keys[3]=False
            keys[2]=False
            player1.img = ImgList['Normal']
                           
            
        if keys[2] == True and lef % 2 == 0: #兩張跑步圖片 
            player1.img = ImgList['LEFT1']
            player1.X -= 8
            lef += 1
        elif keys[2] == True and lef % 2 == 1: 
            player1.img = ImgList['LEFT2']
            player1.X -= 8
            lef += 1
        
        elif keys[3] == True and rig % 2 == 0:
            player1.img = ImgList['RIGHT1']
            player1.X  += 8
            rig += 1 
        elif keys[3] == True and rig % 2 == 1: 
            player1.img = ImgList['RIGHT2']
            player1.X += 8
            rig += 1

       
    
    


    #playerImg = pygame.image.load('C:\\Users\\USER\\PythonGame\\LittleKids\\assets\\playerNomal.png')  

#if __name__ == '__main__':