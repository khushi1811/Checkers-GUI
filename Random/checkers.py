import pygame                   
from copy import deepcopy

pygame.font.init()

#constants needed
INF = 1000000000

width = height = 600

beige = (222, 184, 134)#beige

height1=height-50

king = pygame.transform.scale(pygame.image.load('crown1.png'), (45, 45))#for image in the king token

ROWS = COLS = 8

cyan = (255, 255, 255)

edge_len = height1 // ROWS

black = (0,0,0)#black

brown = (90, 56, 40)#brown



'''
class Checkers_Game runs the whole code, including whose chance it is , which token it is and above all the board
'''
class Checkers_Game:
    def __init__(self):
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('MiniMax Algorithm')
        self.selected = None
        self.board = Checkers_Board()
        self.turn = black        # first  is user's move
        self.all_moves = {}      # valid moves list for the ai or user, whoever's turn it is 

    # updates the display
    def game_state_update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.all_moves)
        pygame.display.update()
    
    def draw_valid_moves(self, moves):
        for move in moves:
          row, col = move
          pygame.draw.circle(self.window, cyan, (col * edge_len + edge_len//2, row * edge_len + edge_len//2), 15)

    
    def move_ai(self, board):#ai turn selection
        self.board = board
        self.all_moves = {}
        if (self.turn == beige):
            self.turn = black
        else:
            self.turn = beige
    
    def move_selection(self, row, col):
        piece = self.board.token_var(row, col)
        if (self.selected):
            self.token_move(piece, row, col)
         #this function helps in finding and moving the desired move
        if (piece != 0 and piece.color == self.turn):
            self.selected = piece
            self.all_moves = self.board.move_list(piece)
            return True

        return False

    def token_move(self, piece, row, col):
        if (piece == 0 and (row, col) in self.all_moves):
            self.board.move(self.selected, row, col)#selected token  is moved
            self.board.remove(self.all_moves[(row, col)])
            self.all_moves = {}
            if (self.turn == beige):
                self.turn = black
            else:
                self.turn = beige
  

    def declare_winner(self):
        #different conditions of wnning are mentioned below
        if (self.board.black > 0):
            f = pygame.font.SysFont('Cambria', 20)
            ori_beige=self.board.beige
            ori_black=self.board.black
            num1=str(ori_black)
            num2=str(ori_beige)
            ori_beige_kings=self.board.king_beige
            ori_black_kings=self.board.king_black
            num3=str(ori_black_kings)
            num4=str(ori_beige_kings)
            string_print="YOUR TOKENS: "+num1+"  "+"YOUR KINGS: "+num3+"  "+"AI TOKENS: "+num2+"  "+"AI KINGS: "+num4
            self.window.blit(f.render(string_print, False, beige), (0,height-50))
            pygame.display.update()
            return None    

        if (self.board.beige <= 0 ):
            self.window.fill(black)
            f = pygame.font.SysFont('Lucida Handwriting', 32)
            self.window.blit(f.render("You Won. Congratulations!", False, beige), (0,height//2))
            pygame.display.update()
            pygame.time.delay(5000)
            return "Black won!!"

        elif (self.board.black <= 0):
            self.window.fill(beige)
            f = pygame.font.SysFont('Lucida Handwriting', 32)
            self.window.blit(f.render("Computer Won. Better Luck Next Time!", False, black), (0,height//2))
            pygame.display.update()
            pygame.time.delay(5000)
            return "Beige won!!"

        else:
            return None

    def get_board(self):
        return self.board


'''
This class works for drawing and moving the tokens
'''
class Checkers_Token:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.x = edge_len * self.col + (edge_len // 2)  # x-coordinate of center of the token on the board
        self.y = edge_len * self.row + (edge_len // 2)  # y-coordinate of center of the token on the board
        self.color = color
        self.is_king = False
    
    def move(self, row, col):
        self.row = row
        self.col = col
        self.x = edge_len * self.col + (edge_len // 2)
        self.y = edge_len * self.row + (edge_len // 2)
    
    # drawing the circles for the tokens
    def draw(self, window):
        rad = edge_len // 2 - 10
        pygame.draw.circle(window, self.color, (self.x, self.y), rad)
        
        if (self.is_king):#setting the king crown image on the token
            window.blit(king, (self.x - king.get_width() // 2, self.y - king.get_height() // 2))



'''
Checkers board class is used for drawing board, tokens and handles the moves for specific tokens and deleting the captured ones
   
'''
class Checkers_Board:
    def __init__(self):
        self.board = []               #checker board display
        self.beige = self.black = 12       
        self.king_beige = self.king_black = 0    
         
        # initialise the self.board with correct tokens at correct positions
        for i in range(ROWS):
            temp = []
            for j in range(COLS):
                if (j % 2 == (i + 1) % 2):
                    # top three rows for beige pieces which is ai
                    if (i <= 2):
                        temp.append(Checkers_Token(i, j, beige))
                    # bottom three rows for black pieces which is user
                    elif (i >= 5):
                        temp.append(Checkers_Token(i, j, black))
                    # empty rows
                    else:
                        temp.append(0)
                #all other positions are empty
                else:
                    temp.append(0)
            self.board.append(temp)

    # drawing and filling the checkers boxes
    def box_checkers(self, window):
        window.fill(black)
        for i in range(ROWS):
            for j in range((i + 1) % 2, COLS, 2):
                pygame.draw.rect(window, brown, (i * edge_len, j * edge_len, edge_len, edge_len))

    # to draw all the tokens on the board
    def draw(self, window):
        self.box_checkers(window)
        for i in range(ROWS):
            for j in range(COLS):
                if (self.board[i][j] != 0):
                    self.board[i][j].draw(window)
 # removes list of tokens from the board
    def remove(self, pieces):
        for i in range(len(pieces)):
            self.board[pieces[i].row][pieces[i].col] = 0
            if (pieces[i] != 0):
                if (pieces[i].color == beige):
                    self.beige -= 1
                else:
                    self.black -= 1

    # calculate utility cutoff value
    def utility_mark(self):
        return (self.beige - self.black) + ((self.king_beige - self.king_black) / 2)
    # moves a piece on the new position on the board and updates board and piece accordingly
    def move(self, piece, new_row, new_col):
        # swapping the initial and final position values
        self.board[new_row][new_col] = self.board[piece.row][piece.col]
        self.board[piece.row][piece.col] = 0
        piece.move(new_row, new_col)

        if (new_row == 0 or new_row == ROWS - 1):
            piece.is_king = True
            if (piece.color == beige):
                self.king_beige += 1
            else:
                self.king_black += 1

   #brown_kings
    # return all the pieces of a given color
    def token_list(self, color):
        pieces = []
        for i in range(ROWS):
            for j in range(COLS):
                if(self.board[i][j] != 0 and self.board[i][j].color == color):
                    pieces.append(self.board[i][j])
        return pieces


    # returns all the moves possible as a dictionary get_all_moves
    # key = final position, values = list of pieces that can reach there
    def move_list(self, piece):
        all_moves = {}

        # checking the feasible moves in downward direction
        if (piece.color == beige or piece.is_king):
            all_moves.update(self.leftwards(piece.row + 1, min(piece.row + 3, ROWS), 1, piece.color, piece.col - 1))
            all_moves.update(self.rightwards(piece.row + 1, min(piece.row + 3, ROWS), 1, piece.color, piece.col + 1))

        # checking the feasible moves in upward direction
        if (piece.color == black or piece.is_king):
            all_moves.update(self.leftwards(piece.row - 1, max(piece.row - 3, -1), -1, piece.color, piece.col - 1))
            all_moves.update(self.rightwards(piece.row - 1, max(piece.row - 3, -1), -1, piece.color, piece.col + 1))

        return all_moves

    # move in left diagonal direction
    def leftwards(self, beg, end, inc, color, l, removed = []):
        moves = {}
        last_piece = []
        for i in range(beg, end, inc):
            if (l < 0):
                break

            if (self.board[i][l] == 0):
                if (len(removed) > 0 and len(last_piece) == 0):
                    break
                else:
                    moves[(i, l)] = last_piece + removed

                # next recursive call
                if (len(last_piece) > 0):
                    if (inc == -1):
                        row = max(i - 3, -1)
                    else:
                        row = min(i + 3, ROWS)
                    moves.update(self.leftwards(i + inc, row, inc, color, l - 1, last_piece))
                    moves.update(self.rightwards(i + inc, row, inc, color, l + 1, last_piece))
                break
            elif (self.board[i][l].color != color):
                last_piece.append(self.board[i][l])
            else:
                break
            l -= 1
        return moves

    # move in right diagonal direction
    def rightwards(self, beg, end, inc, color, r, removed = []):
        moves = {}
        last_piece = []
        for i in range(beg, end, inc):
            if (r >= COLS):
                break

            if (self.board[i][r] == 0):
                if (len(removed) > 0 and len(last_piece) == 0):
                    break
                else:
                    moves[(i, r)] = last_piece + removed

                # next recursive call
                if (len(last_piece) > 0):
                    if (inc == -1):
                        row = max(i - 3, -1)
                    else:
                        row = min(i + 3, ROWS)
                    moves.update(self.leftwards(i + inc, row, inc, color, r - 1, last_piece))
                    moves.update(self.rightwards(i + inc, row, inc, color, r + 1, last_piece))
                break
            elif (self.board[i][r].color != color):
                last_piece.append(self.board[i][r])
            else:
                break
            r += 1
        return moves
    
    def token_var(self, row, col):
        return self.board[row][col]
  #print_board
    def check_print(self):
        for i in range(ROWS):
            for j in range(COLS):
                if (self.board[i][j] != 0):
                    if(self.board[i][j].color == black):
                        print("W ", end = "")
                    else:
                        print("B ", end = "")
                else:
                    print("0 ", end = "")
            print("")

# minimax algorithm
def random(current_board, depth,turn, game_work):
    # 3 = cut-off limit for the mini-max
    if (depth == 3 or game_work.declare_winner() != None):
        return current_board.utility_mark(), current_board

    if (turn == 1):
        moved_boards = get_moved_boards(current_board, beige, game_work)
        best_moved_board = None
        for i in range(len(moved_boards)):
            best_moved_board = moved_boards[i]
            break    
        return  best_moved_board

    else:
        moved_boards = get_moved_boards(current_board, beige, game_work)
        best_moved_board = None
        for i in range(len(moved_boards)):
            best_moved_board = moved_boards[i]
            break   
        return  best_moved_board

# function to find all the next state boards
def get_moved_boards(board, color, game_work):
    new_boards = []
    all_pieces = board.token_list(color)
    for i in range(len(all_pieces)):
        all_moves = board.move_list(all_pieces[i])
        #print(all_moves)

        for move, remove in all_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.token_var(all_pieces[i].row, all_pieces[i].col)

            # applying changes
            temp_board.move(temp_piece, move[0], move[1])
            if (len(remove) > 0):
                temp_board.remove(remove)
            new_boards.append(temp_board)

    return new_boards

def main():
    run = True
    # pygame gui setup
    game_work = Checkers_Game()

    while run:
         #now according to the token color, chances are taken by computer and human
        if (game_work.turn == beige):
            new_board = random(game_work.get_board(), 0, 1, game_work)
            game_work.move_ai(new_board)

        # checking if winner conditions are satisfied
        if (game_work.declare_winner() != None):
            run = False

        # checking the current events, if anyone's type indicates exit, game is terminated
        for eve_queue in pygame.event.get():
            if (eve_queue.type == pygame.QUIT):
                print("ENDED THE GAME!!")
                run = False
            
            if (eve_queue.type == pygame.MOUSEBUTTONDOWN):
                position = pygame.mouse.get_pos()
                row = position[1] // edge_len 
                col = position[0] // edge_len
                game_work.move_selection(row, col)
        game_work.game_state_update()
    pygame.quit()

main()