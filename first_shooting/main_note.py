import pygame
#隨機值
import random
#路徑模組
import os

#遊戲視窗由迴圈組成 game loop
#1.取得玩家輸入
#2.更新遊戲
#3.渲染顯示至畫面上
#4.經過一段時間後再次進入下一次迴圈


#設定後不在改動的變數名稱設置全大寫字母
#遊戲更新偵數
FPS = 60
#視窗寬度
WIDTH = 500
#視窗高度
HEIGHT = 600
#RGB顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#遊戲初始化
pygame.init()
#創建視窗(寬度,高度)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
#更改視窗標題名稱
pygame.display.set_caption("第一個射擊小遊戲")
#是否執行遊戲
running = True
#因應不同電腦或環境的執行速度不同
#設定一個固定速度以維持相同的遊戲體驗
clock = pygame.time.Clock()


#載入圖片
#避免在不同作業系統下，圖片路徑錯誤
#os(模組).path(main當前資料夾).join(加入) ”img“(資料夾), 的”background.jpg“檔案(可以再往下找).convert()(轉為pygame容易讀取格式,減少載入時間) 
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()


#創建一個類別Player繼承內建的sprite類別
class Player(pygame.sprite.Sprite):
    #設定初始函式
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #設定顯示圖片
        #self.image = pygame.Surface((50, 40))
        #載入圖片
        self.image = pygame.transform.scale(player_img, (50, 80))
        #將指定顏色變為透明
        self.image.set_colorkey(BLACK)
        #顏色填滿
        #self.image.fill((GREEN))

        #設定圖片位置
        #將照片get_rect誆選並設定屬性
        #(x,y), top, topright
        #left, center, right
        #bottomleft, bottom, bottomright
        self.rect = self.image.get_rect()
        #設定飛船碰撞判定半徑
        self.radius = 25
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # #設定(x,y)
        # self.rect.x = 400
        # self.rect.y = 400
        # #以方塊中心設定位置
        # self.rect.center = (WIDTH/2, HEIGHT/2)
        #以方塊屬性設定位置
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        #初始移動速度
        self.speedx = 8


    def update(self):
        #判斷鍵盤上的案件是否有被觸發
        #並回傳布林值True, False
        key_pressed = pygame.key.get_pressed()

        #判斷右鍵是否有被觸發, 如果有就向右移動
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        #判斷左鍵是否有被觸發, 如果有就向左移動
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        # #判斷d鍵是否有被觸發, 如果有就向右移動
        # if key_pressed[pygame.K_d]:
        #     self.rect.x += 2
        # #判斷a鍵是否有被觸發, 如果有就向左移動
        # if key_pressed[pygame.K_a]:
        #     self.rect.y -= 1

        # #移動方塊位置
        # self.rect.x += 2
        # #如果移動出方塊則跳回最右邊
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0

        #限制方塊布會超出視窗
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    #飛船射擊
    def shoot(self):
        #子彈位置
        bullet = Bullet(self.rect.centerx, self.rect.top)
        #全部物件群組
        all_sprites.add(bullet)
        #子彈群組(判斷碰撞)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    #設定初始函式
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #設定顯示圖片
        # self.image = pygame.Surface((30, 40))
        #沒有失真的圖片
        self.image_ori = pygame.transform.scale(rock_img, (50, 70))
        self.image_ori.set_colorkey(BLACK)
        #轉動後的圖片
        self.image = self.image_ori.copy()
        #載入圖片
        #self.image = pygame.transform.scale(rock_img, (50, 70))
        #顏色填滿
        # self.image.fill((RED))
        
        #設定圖片位置
        #將照片get_rect誆選並設定屬性
        #(x,y), top, topright
        #left, center, right
        #bottomleft, bottom, bottomright
        self.rect = self.image.get_rect()
        #設定飛船碰撞判定半徑
        self.radius = self.rect.width/2
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        # #設定(x,y)
        # self.rect.x = 400
        # self.rect.y = 400
        # #以方塊中心設定位置
        # self.rect.center = (WIDTH/2, HEIGHT/2)

        #隕石位置
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        
        #初始掉落速度
        self.speedy = random.randrange(1, 3) 
        self.speedx = random.randrange(-2, 2)
        #轉動總角度
        self.total_degree = 0
        #轉動角度
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        #轉動
        self.total_degree += self.rot_degree
        #避免轉動角度超過360度
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
        self.rotate()
        #掉落隕石
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #超出視窗邊界判斷
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            #隕石位置
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            #初始掉落速度
            self.speedy = random.randrange(2, 10) 
            self.speedx = random.randrange(-3, 3) 
            
class Bullet(pygame.sprite.Sprite):
    #設定初始函式
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #設定顯示圖片
        self.image = pygame.transform.scale(bullet_img, (30, 60))
        self.image.set_colorkey(BLACK)
        
        #設定圖片位置
        #將照片get_rect誆選並設定屬性
        #(x,y), top, topright
        #left, center, right
        #bottomleft, bottom, bottomright
        self.rect = self.image.get_rect()

        #子彈位置
        self.rect.centerx = x
        self.rect.bottom = y
        
        #初始子彈速度
        self.speedy = -6


    def update(self):
        #子彈速度
        self.rect.y += self.speedy

        #判斷每個子彈是否超出視窗
        if self.rect.bottom < 0:
            #移除當前判斷成立的子彈
            self.kill()


#創建一個叫all_sprites群組(可以放很多object)
all_sprites = pygame.sprite.Group()
#創建石頭群組
rocks = pygame.sprite.Group()
#創建子彈群組
bullets = pygame.sprite.Group()
#將Player class(類別)用一個object去接
player = Player()
#將player object add in all_sprites 的srpute.Group()
all_sprites.add(player)
#掉落石頭數量
for i in range(8):
    r = Rock()
    #全部物件群組
    all_sprites.add(r)
    #子彈群組(判斷碰撞)
    rocks.add(r)



#遊戲迴圈
while running:
    #clock下的tick函式,在一秒內最多被執行的次數
    #又稱fps
    clock.tick(FPS)

    ###取得輸入###
    #event.get = 發生的所有事件
    #回傳一個列表,同時發生的事件有很多(滑鼠,多個鍵盤...等)
    #用for迴圈將列表遍歷提出
    for event in pygame.event.get():
        #事件類型是否把遊戲關閉
        if event.type  == pygame.QUIT:
            #如果是就關閉(跳出迴圈)
            running = False
        
        #事件是否觸發飛船射擊
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    ###更新遊戲###
    all_sprites.update()
    #判斷兩個群組內物件是否碰撞，各物件碰撞後是否移除
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    #當刪除石頭(True)就進入for並補一個新石頭
    for hit in hits:
        r = Rock()
        #石頭加入全部物件群組(才能update與渲染至畫面)
        all_sprites.add(r)
        #石頭加入石頭群組(才能判斷新石頭是否與子彈碰撞)
        rocks.add(r)
    
    #判斷石頭與飛船是否碰撞，碰撞後是否移除，判斷方法將默認矩形改為圓形
    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
    #碰撞是否成立
    if hits:
        #關閉遊戲
        running = False


    ###畫面顯示###
    #視窗填滿顏色, fill(R, G, B)
    #0~255的數字(調色盤的概念)
    screen.fill((BLACK))
    #設定渲染背景
    
    screen.blit(pygame.transform.scale(background_img, (500, 600)), (0,0))
    #群組內object畫至screen上
    all_sprites.draw(screen)
    #將畫面更新
    pygame.display.update()



#關閉遊戲視窗
pygame.quit()

