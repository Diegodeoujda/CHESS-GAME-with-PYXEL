import pyxel
import os
os.chdir(os.path.dirname(__file__))

pawn = 1
rook = 2
bishop = 3
king = 4
knight = 5
queen = 6

import pyxel


class Menu:
    def __init__(self):

        self.isPlaying = False
        self.quit = False

        self.play_button_x = 40
        self.play_button_y = 40
        self.quit_button_x = 40
        self.quit_button_y = 70
        self.button_width = 50
        self.button_height = 20

    def update(self):
        pyxel.mouse(True)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            if (self.play_button_x <= mouse_x <= self.play_button_x + self.button_width and
                    self.play_button_y <= mouse_y <= self.play_button_y + self.button_height):
                self.isPlaying = True
            elif (self.quit_button_x <= mouse_x <= self.quit_button_x + self.button_width and
                  self.quit_button_y <= mouse_y <= self.quit_button_y + self.button_height):
                self.quit = True

    def draw(self):
        pyxel.cls(0)
        if not self.isPlaying:
            pyxel.text(55, 20, "Chess", pyxel.COLOR_WHITE)

            pyxel.rect(self.play_button_x, self.play_button_y, self.button_width, self.button_height, pyxel.COLOR_GREEN)
            pyxel.text(self.play_button_x + 10, self.play_button_y + 5, "Play", pyxel.COLOR_WHITE)

            pyxel.rect(self.quit_button_x, self.quit_button_y, self.button_width, self.button_height, pyxel.COLOR_RED)
            pyxel.text(self.quit_button_x + 10, self.quit_button_y + 5, "Quit", pyxel.COLOR_WHITE)

        if self.quit:
            pyxel.quit()



class Pieces:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getColor(self):
        if self.color == "black":
            return 0
        else:
            return 7

    def __str__(self):
        return f"{self.__class__.__name__}({self.color})({self.x},{self.y})"

    def __repr__(self):
        return self.__str__()


class Pawn(Pieces):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def getValidMove(self, board):
        valid_moves = []
        if self.color == 'white':
            direction = -1
        else:
            direction = 1
        # avancer une case
        if 0 <= self.y + direction < 8 and board.get_piece(self.x, self.y + direction) == 0:
            valid_moves.append((self.x, self.y + direction))

            # avancer 2 case
            if 0 <= self.y + direction * 2 < 8 and board.get_piece(self.x, self.y + direction * 2) == 0:
                valid_moves.append((self.x, self.y + direction * 2))

        # diag
        for dx in [-1, 1]:
            nx, ny = self.x + dx, self.y + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board.get_piece(nx, ny)
                if piece and piece.color != self.color:
                    valid_moves.append((nx, ny))

        return valid_moves


class Rook(Pieces):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def getValidMove(self, board):
        valid_moves = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece(x, y)
                if piece == 0:
                    valid_moves.append((x, y))
                elif piece.color != self.color:
                    valid_moves.append((x, y))
                    break
                else:
                    break
                x += dx
                y += dy

        return valid_moves


class Bishop(Pieces):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def getValidMove(self, board):
        valid_moves = []

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece(x, y)
                if piece == 0:
                    valid_moves.append((x, y))
                elif piece.color != self.color:
                    valid_moves.append((x, y))
                    break
                else:
                    break
                x += dx
                y += dy

        return valid_moves


class Queen(Pieces):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def getValidMove(self, board):
        valid_moves = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece(x, y)
                if piece == 0:
                    valid_moves.append((x, y))
                elif piece.color != self.color:
                    valid_moves.append((x, y))
                    break
                else:
                    break
                x += dx
                y += dy

        return valid_moves


class King(Pieces):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def getValidMove(self, board):
        valid_moves = []

        directions = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1),
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]

        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            if 0 <= x < 8 and 0 <= y < 8:  # Vérifie que la case est dans les limites de l'échiquier
                piece = board.get_piece(x, y)
                if piece == 0 or piece.color != self.color:  # Si case vide ou ennemie
                    valid_moves.append((x, y))

        return valid_moves


class Knight(Pieces):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def getValidMove(self, board):
        valid_moves = []

        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]

        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                piece = board.get_piece(x, y)
                if piece == 0 or piece.color != self.color:
                    valid_moves.append((x, y))

        return valid_moves


class ChessBoard:
    def __init__(self):
        self.width = 8
        self.length = 8
        self.board = []
        self.constructBoard()

    def constructBoard(self):
        for y in range(self.length):
            ligne = [0] * self.length
            self.board.append(ligne)
        for x in range(self.width):
            self.board[1][x] = Pawn('black', x, 1)
            self.board[6][x] = Pawn('white', x, 6)

        self.board[0][0] = Rook('black', 0, 0)
        self.board[0][7] = Rook('black', 7, 0)
        self.board[7][0] = Rook('white', 0, 7)
        self.board[7][7] = Rook('white', 7, 7)

        # knight
        self.board[0][1] = Knight('black', 1, 0)
        self.board[0][6] = Knight('black', 6, 0)
        self.board[7][1] = Knight('white', 1, 7)
        self.board[7][6] = Knight('white', 6, 7)

        # Bishop
        self.board[0][2] = Bishop('black', 2, 0)
        self.board[0][5] = Bishop('black', 5, 0)
        self.board[7][2] = Bishop('white', 2, 7)
        self.board[7][5] = Bishop('white', 5, 7)

        # queen
        self.board[0][3] = Queen('black', 3, 0)
        self.board[7][3] = Queen('white', 3, 7)

        # king
        self.board[7][4] = King('white', 4, 7)
        self.board[0][4] = King('black', 4, 0)
        print(self.board)

    def get_piece(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.length:
            return self.board[y][x]
        return 0

    def move_piece(self, from_x, from_y, to_x, to_y):
        piece = self.board[from_y][from_x]
        if piece:
            piece.move(to_x, to_y)
            self.board[to_y][to_x] = piece
            self.board[from_y][from_x] = 0
            return True
        return False
 
class ChessGame:
    def __init__(self):
        pyxel.init(128, 128, title="Chess")
        pyxel.load("chess.pyxres")
        self.board = ChessBoard()
        self.menu = Menu()
        self.selected_piece = None
        self.current_player = 'white'
        pyxel.run(self.update, self.renderGame)
        


    def update(self):
        
        if not self.menu.isPlaying:
            self.menu.update()
        else:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                tile_x = pyxel.mouse_x // 16
                tile_y = pyxel.mouse_y // 16
                if 0 <= tile_x < 8 and 0 <= tile_y < 8:
                    if self.selected_piece is None:
                        # sel une pièce
                        piece = self.board.get_piece(tile_x, tile_y)
                        if piece and piece.color == self.current_player:
                            print(piece)
                            self.selected_piece = (tile_x, tile_y)
                            self.validmove = piece.getValidMove(self.board)
                            print(self.validmove)
                    else:
                        # dep piece
                        from_x, from_y = self.selected_piece
                        if (tile_x, tile_y) in self.validmove:
                            self.board.move_piece(from_x, from_y, tile_x, tile_y)
                            if self.current_player == 'white':
                                self.current_player = 'black' 
                            else:
                                self.current_player = 'white'
                        
                        self.selected_piece = None
                        self.valid_moves = []

       
                    

    def renderGame(self):
        if not self.menu.isPlaying:
            self.menu.draw()


        else:
            tile_size = 16
            for y in range(self.board.length):
                for x in range(self.board.width):
                    if ((x+y)%2) == 0:
                        color = 4
                    else:
                        color = 15
                    pyxel.rect(x * tile_size, y * tile_size, tile_size, tile_size, color)

            for y in range(8):
                for x in range(8):
                    piece = self.board.get_piece(x, y)
                    if piece:
                        X,Y = 0,0
                        if isinstance(piece, Pawn):
                            Xpiece, Ypiece = piece.getX(), piece.getY()
                            if piece.getColor() == 0:
                                X,Y = 0,32
                            else:
                                X,Y =0,16

                        elif isinstance(piece, Rook):
                            
                            Xpiece, Ypiece = piece.getX(), piece.getY()
                            if piece.getColor() == 0:
                                X,Y =16,32
                            else:
                                X,Y =16,16
                        elif isinstance(piece, Knight):
                            Xpiece, Ypiece = piece.getX(), piece.getY()
                            if piece.getColor() == 0:
                                X,Y =32,32
                            else:
                                X,Y =32,16

                        elif isinstance(piece, Bishop):
                            Xpiece, Ypiece = piece.getX(), piece.getY()
                            if piece.getColor() == 0:
                                X,Y =80,32
                            else:
                                X,Y =80,16

                        elif isinstance(piece, Queen):
                            Xpiece, Ypiece = piece.getX(), piece.getY()
                            if piece.getColor() == 0:
                                X,Y =48,32
                            else:
                                X,Y =48,16

                        elif isinstance(piece, King):
                            X,Y = 64,16
                            Xpiece, Ypiece = piece.getX(), piece.getY()
                            if piece.getColor() == 0:
                                X,Y =64,32
                            else:
                                X,Y =64,16
                            
                        pyxel.blt(Xpiece * tile_size, Ypiece * tile_size,0,X, Y,tile_size,tile_size,11)

            if self.selected_piece:
                x, y = self.selected_piece
                pyxel.rectb(x * tile_size, y * tile_size, tile_size, tile_size, 8)
                for move_x, move_y in self.validmove:
                    pyxel.rectb(move_x * tile_size, move_y * tile_size, tile_size, tile_size, 11)


ChessGame()