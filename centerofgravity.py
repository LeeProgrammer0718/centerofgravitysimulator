import pygame,sys
import math
import random
pygame.init()
pygame.display.set_caption("Center of Gravity")
width,height = 1000,700
surface = pygame.display.set_mode((width,height))

class rect:
    def __init__(self,size): #m=질량 size = (width,height) //2의 배수 
        self.width = size[0]
        self.height = size[1]
        self.pos = [0,0] #초기 사각형 중심 
        self.mouseoneclick = 0 #마우스를 한 번 눌렀을 때 1 두번 
        self.mousepointlist = [(0,0),(0,0)] #index 0--start pos index1--end pos
        self.firstmousetracking = False #마우스 트래킹이 끝나면 True
        self.moveangle = math.radians(0) #각도 변화량
        self.detectmoveangle = False #각도 변화량 한번만 측정하게 함 
        self.detectgravity = False #무게중심이 바닥면 가까이 있으면 False
        self.centerofgravity = [0,0] #무게중심 계산
        self.velocity = 0
    
    def rectpos(self,pos): #사각형의 각 꼭짓점 좌표 계산 
        self.pos = pos
        lineangle2 = math.radians(90)-self.moveangle
        lineangle4 = math.radians(180)-(lineangle2+math.radians(90))
        #print("angle",lineangle2,lineangle4)
        self.pointlist= [(self.pos[0]+self.width//2+self.width*math.sqrt(2)*math.cos(math.radians(45)+lineangle2),self.pos[1]+self.height//2-self.width*math.sqrt(2)*math.sin(math.radians(45)+lineangle2)),\
                         (self.pos[0]+self.width//2+self.width*math.cos(lineangle2),self.pos[1]+self.height//2-self.width*math.sin(lineangle2)),\
                         (self.pos[0]+self.width//2,self.pos[1]+self.height//2),\
                         (self.pos[0]+self.width//2-self.width*math.cos(lineangle4),self.pos[1]+self.height//2-self.width*math.sin(lineangle4))]
        
    def drawrect(self,surface,linesize):
        pos = self.pos
        '''
        pygame.draw.lines(surface,(255,255,255),False,[((pos[0]-self.width//2,pos[1]-self.height//2),(pos[0]+self.width//2,pos[1]-self.height//2)),\
                                                       ((pos[0]+self.width//2,pos[1]-self.height//2),(pos[0]+self.width//2,pos[1]+self.height//2)),\
                                                       ((pos[0]+self.width//2,pos[1]+self.height//2),(pos[0]-self.width//2,pos[1]+self.height//2)),\
                                                       ((pos[0]-self.width//2,pos[1]+self.height//2),(pos[0]-self.width//2,pos[1]-self.height//2))\
                                                       ],5)'''
        pygame.draw.line(surface,(255,255,255),self.pointlist[0],self.pointlist[1],linesize)
        pygame.draw.line(surface,(255,255,255),self.pointlist[1],self.pointlist[2],linesize)
        pygame.draw.line(surface,(255,255,255),self.pointlist[2],self.pointlist[3],linesize)
        pygame.draw.line(surface,(255,255,255),self.pointlist[3],self.pointlist[0],linesize)

    def rectafterimage(self,surface,linesize):
        pygame.draw.line(surface,(116,116,116),(self.pos[0]-self.width//2,self.pos[1]-self.height//2),(self.pos[0]+self.width//2,self.pos[1]-self.height//2),linesize)
        pygame.draw.line(surface,(116,116,116),(self.pos[0]+self.width//2,self.pos[1]-self.height//2),(self.pos[0]+self.width//2,self.pos[1]+self.height//2),linesize)
        pygame.draw.line(surface,(116,116,116),(self.pos[0]+self.width//2,self.pos[1]+self.height//2),(self.pos[0]-self.width//2,self.pos[1]+self.height//2),linesize)
        pygame.draw.line(surface,(116,116,116),(self.pos[0]-self.width//2,self.pos[1]+self.height//2),(self.pos[0]-self.width//2,self.pos[1]-self.height//2),linesize)
        
    def drawdot(self,surface):
        pygame.draw.circle(surface,(255,255,255),(int(self.pointlist[0][0]),int(self.pointlist[0][1])),7,0)
        pygame.draw.circle(surface,(255,0,0),(int(self.pointlist[1][0]),int(self.pointlist[1][1])),7,0)
        pygame.draw.circle(surface,(0,255,0),(int(self.pointlist[2][0]),int(self.pointlist[2][1])),7,0)
        pygame.draw.circle(surface,(0,0,255),(int(self.pointlist[3][0]),int(self.pointlist[3][1])),7,0)
        
    def mousetracking(self,mousepoint,mouseclick):
        if self.pointlist[0][0]<mousepoint[0]<self.pointlist[1][0] and self.pointlist[0][1]<mousepoint[1]<self.pointlist[2][1]:
            #print("inner")
            if mouseclick[0] == 1:
                #마우스 클릭시
                if self.mouseoneclick == 0:
                    self.mousepointlist[0]=mousepoint
                    self.mouseoneclick = 1
        if mouseclick[0] != 1:
            if self.mouseoneclick==1:
                self.mousepointlist[1] = mousepoint
                self.mouseoneclick = 0
                self.firstmousetracking = True
        #print(self.mousepointlist)
        #할 때 무조건 안쪽에서 바깥쪽으로 이동할 것
        
    def drawmouseline(self,surface):
        if self.firstmousetracking:
            pygame.draw.line(surface,(255,0,0),self.mousepointlist[0],self.mousepointlist[1],3)
            pygame.draw.line(surface,(0,255,0),self.mousepointlist[0],self.pointlist[2],3)
            pygame.draw.line(surface,(0,255,0),self.mousepointlist[1],self.pointlist[2],3)
        
    def drawgravityline(self,surface):
        self.centerofgravity = [(self.pointlist[1][0]+self.pointlist[3][0])//2,(self.pointlist[0][1]+self.pointlist[2][1])//2]
        pygame.draw.line(surface,(255,187,0),((self.pointlist[1][0]+self.pointlist[3][0])//2,(self.pointlist[0][1]+self.pointlist[2][1])//2),((self.pointlist[1][0]+self.pointlist[3][0])//2,700),3)
        
    def deltaangle(self): #잡아당긴 각도계산
        if self.firstmousetracking: #마우스 트래킹이후 실행 
            if not self.detectmoveangle: #처음만 실행
                angle1 = math.atan2(self.pointlist[2][1]-self.mousepointlist[0][1],self.pointlist[2][0]-self.mousepointlist[0][0])
                angle2 = math.atan2(self.pointlist[2][1]-self.mousepointlist[1][1],self.mousepointlist[1][0]-self.pointlist[2][0])
                self.moveangle = math.radians(180)-(angle1+angle2) #radian
                #print(self.moveangle)
                self.detectmoveangle = True
                
    def returnangle(self):
        return self.moveangle
    
    def DetectCenterOfGravity(self):
        if self.pointlist[2][0]< self.centerofgravity[0]<self.pointlist[1][0]:
            self.detectgravity = True
        else:
            self.detectgravity = False
        #print(self.detectgravity)
            
    def returngravitypos(self): #무게중심 좌표 반환 
        return self.centerofgravity
    
    def move(self): #회전운동 적용 
        if self.detectgravity:
            if self.pointlist[1][1]<self.pointlist[2][1]:
                self.moveangle -= math.radians(-1-self.velocity)
                self.velocity += math.radians(4)
                print(self.moveangle)
                print("move")
        else:
            if self.pointlist[3][1]<self.pointlist[2][1]:
                self.moveangle -= math.radians(1+self.velocity)
                self.velocity += math.radians(4)
    
def text(surface,TEXT,COLOR,SIZE,POS):
    pygame.font.init()
    font = pygame.font.Font(None,SIZE)
    text = font.render(TEXT,False,COLOR)
    surface.blit(text,POS)   

def LoadingBar(surface,num,pos,size):
    #파일 검사용 로딩바
    if num<101:
        pass
    else:
        return True
    pygame.draw.rect(surface,(255,255,255),(pos,size),2)
    pygame.draw.rect(surface,(255,255,255),(pos,(0+size[0]//100*num,size[1])),0)

def START(): #시작 화면 , 파일 검사
    global surface,width,height
    num = 0
    while True:
        pygame.time.delay(60)
        width = surface.get_width()
        height = surface.get_height()
        text(surface,"Center   Of   Gravity   Simulation",(92,209,229),90,(0,80))
        text(surface,"made by jaeho and shyuk",(250,237,125),30,(0,150))
        num += random.random()*10
        if LoadingBar(surface,num,((width-width//5*3)//2,height-height//10),(width//5*3,20)):
            print("finish")
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    return True

                
def main():
    global surfaces,width,height
    rectangle = rect((250,250))
    KEY = [False] #재시작 버튼 눌림 감지 
    while True:
        pygame.time.delay(10)
        surface.fill((0,0,0))
        text(surface,"To restart, Press R key ",(92,209,229),35,(0,0))
        pygame.draw.line(surface,(255,255,255),(0,height-70),(width,height-70),5)
        rectangle.rectpos((500,500))
        rectangle.rectafterimage(surface,5)
        rectangle.drawrect(surface,5)
        rectangle.mousetracking(pygame.mouse.get_pos(),pygame.mouse.get_pressed())
        rectangle.drawmouseline(surface)
        rectangle.deltaangle()
        text(surface,"Angle: {} (radian)".format(rectangle.returnangle()),(140,140,140),35,(0,80))
        rectangle.drawgravityline(surface)
        rectangle.drawdot(surface)
        rectangle.DetectCenterOfGravity()
        rectangle.move()
        text(surface,"Center Of Gravity",(255,0,0),20,rectangle.returngravitypos())
        if KEY[0]:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    KEY[0] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    KEY[0] = False
        pygame.display.update()
        
    main()

if __name__ == "__main__":
    #main()
    if START():
        main()
