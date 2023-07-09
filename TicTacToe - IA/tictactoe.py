import copy
import sys
import random
import pygame
import numpy as np

from constantes import *

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE GAME')
screen.fill( BG_COLOR )


class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) ) 
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False):

        #Condition Winners

        #Vertical
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    if self.squares[0][col] == 2:
                        color = CIRC_COLOR
                    else:
                        color = CROSS_COLOR
                    iPos = (col * SIZE + SIZE // 2, 20)
                    fPos = (col * SIZE + SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
                return self.squares[0][col]
            
        #Horizontal
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    if self.squares[row][0] == 2:
                        color = CIRC_COLOR
                    else:
                        color = CROSS_COLOR
                    iPos = (20, row * SIZE + SIZE // 2)
                    fPos = (WIDTH - 20, row * SIZE + SIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
                return self.squares[row][0]
            
        #Diagonal Desc
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                if self.squares[1][1] == 2:
                    color = CIRC_COLOR
                else:
                    color = CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        
        #Diagonal Asc
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                if self.squares[1][1] == 2:
                    color = CIRC_COLOR
                else:
                    color = CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        
        #No hay ganador aun
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        return empty_sqrs
    
    def isFull(self):
        return self.marked_sqrs == 9
    
    def isEmpty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd_choice(self, board):
        empty_sqrs = board.get_empty_sqrs()
        index = random.randrange(0 ,len(empty_sqrs))
        return empty_sqrs[index]
    
    def minimax(self, board, maximizing):

        #caso terminal
        case = board.final_state()

        #Gana 1
        if case == 1:
            return 1, None

        #Gana 2
        if case == 2:
            return -1, None
        
        #Empate
        elif board.isFull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval =  self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row,col)
            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval =  self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)
            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd_choice(main_board)
        else:
            eval, move = self.minimax(main_board, False)
        return move

class Game:
    def __init__(self):
        self .board = Board()
        self.ai = AI()
        self.player = 1 #1-Cruz 2-Circulo
        self.gamemode = 'ai' #Jugador vs Jugador o IA
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row,col,self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        screen.fill( BG_COLOR )
        #Vertical
        pygame.draw.line(screen, LINE_COLOR, (SIZE, 0), (SIZE,HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SIZE, 0), (WIDTH - SIZE,HEIGHT), LINE_WIDTH)

        #Horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SIZE), (WIDTH,SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SIZE), (WIDTH, HEIGHT - SIZE), LINE_WIDTH)

    def draw_fig(self,row,col):
        if self.player == 1:
            #Construido con lineas ascendentes y descendentes

            #Descendentes
            start_desc = (col * SIZE + OFFSET, row * SIZE + OFFSET)
            end_desc = (col * SIZE + SIZE - OFFSET, row * SIZE + SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            #Ascendentes
            start_asc = (col * SIZE + OFFSET, row * SIZE + SIZE - OFFSET)
            end_asc = (col * SIZE + SIZE - OFFSET, row * SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            center = (col * SIZE + SIZE // 2, row * SIZE + SIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        if self.gamemode == 'pvp':
            self.gamemode = 'ai'
            print('Mode -> ai')
        else:
            self.gamemode = 'pvp'
            print('Mode -> pvp')

    def isOver(self):
        return self.board.final_state(show=True) != 0 or self.board.isFull()

    def reset(self):
        self.__init__()

def main():

    #objects
    game = Game()
    board = game.board
    ai = game.ai

    #Explicaciones
    print('------------------------------------------------------------------')
    print('Press g to change the mode ia-pvp or pvp-ia')
    print('Press r to restart')
    print('Press 0 to change level to random, press 1 to change level to AI')
    print('------------------------------------------------------------------')

    #Bucle del main
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                #g-gamemode 
                if event.key == pygame.K_g:
                    game.change_gamemode()

                #r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                    print('Game restarted')

                #0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                    print('Random level')
                
                #1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1    
                    print('IA level')

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SIZE
                col = pos[0] // SIZE

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row,col)

                    if game.isOver():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            
            row, col = ai.eval(board)
            game.make_move(row,col)

            if game.isOver():
                game.running = False

        pygame.display.update()

main()