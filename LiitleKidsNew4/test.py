# -*- coding: utf-8 -*-

class GameState():
    
    
    def __init__(self):
        super().__init__()
        super(player,self).__init__(self, X, Y, HP, img, vel)
        super(Platform,self).__init__(self, X, Y, dmg, img)
        self.playerx = int(SCREENWIDTH / 2)#agent initial position
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) *0.2)#agent initial 
        self.keys =  [False, False, False]
        self.score=0
        
    def frame_step(self, input_actions):
        pygame.event.pump()
        terminal = False
        reward=0.1
        if input_actions[0] == 1 or input_actions[1]== 1 or input_actions[2]== 1:  # 检查输入正常
            if input_actions[0] == 1 and input_actions[1] == 0 and input_actions[2] == 0  and self.pos != (0,1):
            # 不動
                pass
            elif input_actions[0] == 0 and input_actions[1] == 1 and input_actions[2] == 0  == 0 and self.pos != (0,-1):
            #向左
                keys[2]=True
            elif input_actions[0] == 0 and input_actions[1] == 0 and input_actions[2] == 1  and self.pos != (1,0):
            #向右
                keys[3]=True
       
            else:
                pass
        else:
            raise ValueError('Multiple input actions!')
        
        #判斷碰撞
        if (pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1 and Platform.img == ImgList['ceil'] ): 
            self.score-=1
            reward = -1
        
        if(pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1) and (Player.Y+PlayerHight)>Platform.Y:
            if (Platform.img == ImgList['Normal']):
                self.score+=1
                reward = 1
                
        if(pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1) and (Player.Y+PlayerHight)>Platform.Y:
            if (Platform.img == ImgList['Nails']):
                self.score-=1
                reward = -1
        
        if(pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1) and (Player.Y+PlayerHight)>Platform.Y:
            if (Platform.img == ImgList['TrampolineUP']):
                self.score+=0.1
                reward = 0.1
        
        if(pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1) and (Player.Y+PlayerHight)>Platform.Y:
            if(Platform.img == ImgList['conveyor_right']):
                self.score+=0.1
                reward = 0.1
        
        if(pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1) and (Player.Y+PlayerHight)>Platform.Y:
            if(Platform.img == ImgList['conveyor_left']):   
                self.score+=0.1
                reward = 0.1
        #判斷死亡
        isdead=isDead(player)
        
        
        if isdead:
            terminal = True
            self.__init__()
            reward = -10
        #draw
        self.screen.fill(0,0,0)
        for x in range (80, 700, 100):#設定牆壁 以及生命值
            screen.blit( KidImg.wall,  (0, x))
            screen.blit( KidImg.wall,  (460, x))
        
            screen.blit(player1.img, (player1.X, player1.Y))#設定玩家
            screen.blit( KidImg.ceil,  (20, 80))
            screen.blit( KidImg.ceil,  (55, 80))
            
            if player1.HP == 10:
                screen.blit( KidImg.life,  (10, 0))
            elif player1.HP == 9:
                screen.blit( KidImg.life1,  (10, 0))
            elif player1.HP == 8:
                screen.blit( KidImg.life2,  (10, 0))
            elif player1.HP == 7:
                screen.blit( KidImg.life3,  (10, 0))
            elif player1.HP == 6:
                screen.blit( KidImg.life4,  (10, 0))
            elif player1.HP == 5:
                screen.blit( KidImg.life5,  (10, 0))
            elif player1.HP == 4:
                screen.blit( KidImg.life6,  (10, 0))
            elif player1.HP == 3:
                screen.blit( KidImg.life7,  (10, 0))
            elif player1.HP == 2:
                screen.blit( KidImg.life8,  (10, 0))
            elif player1.HP == 1:
                screen.blit( KidImg.life9,  (10, 0))
            elif player1.HP <= 0:
                screen.blit( KidImg.life10,  (10, 0))
                
            
            
            
            
            image_data = pygame.surfarray.array3d(pygame.display.get_surface())
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            
            return image_data, reward, terminal