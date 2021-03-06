#!/usr/bin/env python
import pygame
from pygame.locals import *

pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)

windowSurface = pygame.display.set_mode((600,400), FULLSCREEN,32)
windowInfo = pygame.display.Info()
FONTSIZE = 48
LINEHEIGHT = 28
basicFont = pygame.font.SysFont(None, FONTSIZE)

def render(windowSurface):
  
  #Draw amount Poured
  text = basicFont.render("Current", True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text,(40,20))
  text = basicFont.render("HIYO!", True, WHITE, BLACK)
  textRect = text.get_rect()
  windowSurface.blit(text,(40,20+LINEHEIGHT))
  
  pygame.display.flip()
  
while True:
  for event in pygame.event.get():
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
      GPIO.cleanup()
      pygame.quit()
      sys.exit()
      
  render(windowSurface)