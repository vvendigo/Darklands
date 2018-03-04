# coding=utf-8
import pygame

lnHeight = 25
fonts = pygame.font.get_fonts()

pygame.init()
srf = pygame.Surface((500, len(fonts)*lnHeight))

y = 0

for fname in fonts:
	print fname
	font = pygame.font.SysFont(fname, lnHeight-5)
	text = font.render(fname+": Nürnberg".decode('utf-8'), True, (255, 255, 255))
	srf.blit(text, (0, y))
	y += lnHeight


pygame.image.save(srf, "fonts.png")

