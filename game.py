import pgzrun 
from platformer import * 

# our platformer constants
TILE_SIZE = 18 
ROWS = 30 
COLS = 20

# Pygame constants
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "Game Platformer"

# build world
platforms = build("platformer_platforms.csv", TILE_SIZE)
obstacles = build("platformer_obstacles.csv", TILE_SIZE)
pipes = build("platformer_pipes.csv", TILE_SIZE)
arrows = build("platformer_arrow.csv", TILE_SIZE)
coins = build("platformer_coins.csv", TILE_SIZE)
mushrooms = build("platformer_mushrooms.csv", TILE_SIZE)
hearts = build("platformer_heart.csv", TILE_SIZE)
pipe_flags = build("platformer_flag-pipe.csv", TILE_SIZE)
flags = build("platformer_flag.csv", TILE_SIZE)
enemys = build("platformer_enemy.csv", TILE_SIZE)

# hero_frames = [f"arq{i}" for i in range(1,5)]
# idle_image = "arq0"
# current_frame = 0

# define player Actor 
hero = Actor("p_01_right_stop")
hero.bottomleft = (0, HEIGHT - TILE_SIZE)

# define Actor-specific variables
hero.velocity_x = 3
hero.velocity_y = 0
hero.jumping = False
hero.alive = True
hero.scale = 1

# frame_duration = 0.1
# frame_timer = 0

# define global variables
game_started = False
gravity = 1
jump_velocity = -10
over = False 
win = False
game_music = True
game_sound = True
# is_walking = False


# Create buttons
start_button = Rect(((WIDTH / 2-50, HEIGHT / 2-11)), (100, 20))
leave_button = Rect(((495, 5)), (35, 18))
music_button = Rect(((8, 5)), (52, 15))
sound_button = Rect(((65, 5)), (52, 15))


# music
def music_game(): 
  if game_music: 
    music.play("game_music")
  else:
    music.pause()
    
# sound
def sound_game(sound_object): 
  if game_sound:
    if sound_object == "coin":
      sounds.coin.play()
    elif sound_object == "heart":
      sounds.heart.play()
    elif sound_object == "mushroom":
      sounds.mushroom.play()
    elif sound_object == "winner":
      sounds.winner.play()
    elif sound_object == "over":
      sounds.over.play()
    
  else:
    sounds.coin.stop()
    sounds.heart.stop()
    sounds.mushroom.stop()
    sounds.winner.stop()
    
    
def draw():
    screen.clear()
    screen.fill("skyblue")
    # draw all platforms
    for platform in platforms:
      platform.draw()
    # draw all obstacles
    for obstacle in obstacles:
      obstacle.draw()
    # draw all pipes
    for pipe in pipes:
      pipe.draw()
   # draw all coins
    for coin in coins:
      coin.draw()
    # draw all arrows
    for arrow in arrows:
      arrow.draw()
    # draw all mushrooms
    for mushroom in mushrooms:
      mushroom.draw()
    # draw all hearts
    for heart in hearts:
      heart.draw()  
    # draw all pipe flag
    for pipe_flag in pipe_flags:
      pipe_flag.draw()  
    # draw all flags
    for flag in flags:
      flag.draw()  
    # draw all enemys
    # for enemy in enemys:
    #   enemy.draw()  
      
    # draw the hero 
    if hero.alive: 
      hero.draw()
    
    if not game_started:
        # draw button start
        screen.draw.filled_rect(start_button, (0, 0, 0))  
        screen.draw.text("Start game", center=(WIDTH // 2, HEIGHT // 2), color="white", fontsize=20, )
    if game_started:
        screen.draw.filled_rect(leave_button, (205, 0, 0)) 
        screen.draw.text("Exit", (500, 7), color="white", fontsize=20)
        screen.draw.filled_rect(music_button, (25, 25, 205)) 
        screen.draw.filled_rect(sound_button, (25, 25, 205)) 
        
        #display button sound
        if game_sound: 
          screen.draw.text("Sound On", (67, 8), color="white", fontsize=15)
        else: 
          screen.draw.text("Sound Off", (67, 8), color="white", fontsize=15)
          
        # display button music
        if game_music: 
          screen.draw.text("Music On", (10, 8), color="white", fontsize=15) 
        else: 
          screen.draw.text("Music Off", (10, 8), color="white", fontsize=15)
        
        # display messages
        if over: 
          screen.draw.text("Game Over!", center=(WIDTH / 2, HEIGHT / 2))
          sound_game("over")
          clock.schedule(exit, 0.8)
        if win: 
          sound_game("winner")
          screen.draw.text("You Win!", center=(WIDTH / 2, HEIGHT / 2))  
          clock.schedule(exit, 4.0)
               
      
def on_mouse_down(pos):
    global game_started, game_music, game_sound
    if start_button.collidepoint(pos):  
        game_started = True
    
    if sound_button.collidepoint(pos):
        game_sound = not game_sound
           
    if music_button.collidepoint(pos):
        game_music = not game_music
        music_game()
        
    if leave_button.collidepoint(pos):
      exit()
      
def update(dt):
  global over, win, game_started, frame_timer, current_frame, is_walking
  # is_walking = False
  if game_started:
         # handle left movement
        if keyboard.LEFT and hero.midleft[0] > 0: 
          hero.x -= hero.velocity_x
          # hero.spite =  archaeologist_walk 
          hero.image =  "p_01_left_walk" if hero.image ==  "p_01_left_stop" else "p_01_left_stop"
          hero.flip_x = True
          # hero.walking = True
          # hero.image = hero_frames[current_frame]
          # is_walking = True

        # handle right movement
        elif keyboard.RIGHT and hero.midright[0] < WIDTH: 
          hero.x += hero.velocity_x
          hero.image =  "p_01_right_walk" if hero.image ==  "p_01_right_stop" else "p_01_right_stop"
          hero.flip_x = False
          # hero.image = hero_frames[current_frame]
          # is_walking = True

        
        # if is_walking: 
        #   frame_timer += dt
        #   if frame_timer >= frame_duration:
        #     frame_timer = 0
        #     current_frame = (current_frame +1) % len(hero_frames)
        #   else:
        #       hero.image = idle_image
                      
          # hero.spite =  archaeologist_walk 
        
        # handle gravity
        hero.y += hero.velocity_y 
        hero.velocity_y += gravity
        
        # if the hero collided with a platform
        if hero.collidelist(platforms) != -1: 
          # get object that hero collided with
          object = platforms[hero.collidelist(platforms)]
          # moving down - hit the ground
          if hero.velocity_y >= 0:
            hero.y = object.y - (object.height / 2 + hero.height / 2)
            hero.jumping = False
          # moving up -> hit their head
          else:
            hero.y = object.y + (object.height / 2 + hero.height / 2)
          hero.velocity_y = 0 
        
        # check collision with obstacles
        if hero.collidelist(obstacles) != -1:
            hero.alive = False
            over = True
            
        # check mushroom collision
        for mushroom in mushrooms:
          if hero.colliderect(mushroom):
              sound_game("mushroom")
              mushrooms.remove(mushroom)
              
        if len(mushrooms) == 0:
            win = True
              
        # check coin collision
        for coin in coins:
          if hero.colliderect(coin):
              sound_game("coin")
              coins.remove(coin)
              
        # check heart collision
        for heart in hearts:
          if hero.colliderect(heart):
              sound_game("heart")
              hearts.remove(heart)

        #check flag collision
        for flag in flags:
          if hero.colliderect(flag):
            win = True
            sound_game("winner")
  
def on_key_down(key):
  if key == keys.UP and not hero.jumping: 
      hero.velocity_y = jump_velocity
      hero.jumping = True

# def on_key_up(key):
  # if key == keys.LEFT or key == keys.RIGHT:
    # hero.sprite = archaeologist_stand
music_game()
pgzrun.go()