import sys
import pygame

def init():
    pygame.init()
    screen = pygame.display.set_mode((400,400))

def getKey(keyName):
    ans = False
    for event in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    if keyInput [myKey]:
        ans = True
    pygame.display.update()

    return ans
def main():
    if getKey('LEFT'):
        print('Key Left was pressed')
    if getKey('RIGHT'):
        print('Key Right was pressed')

if __name__ == '__main__':
    init()
    while True:
        main()
