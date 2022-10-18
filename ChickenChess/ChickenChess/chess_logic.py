from turtle import update
from types import NoneType
from stockfish import Stockfish
import os
from sys import platform
from .settings import BASE_DIR
import chess
if platform == "linux":
    stockpath = os.path.join(BASE_DIR,'engine/stockfish_15_linux_x64/stockfish_15_linux_x64/stockfish_15_x64')
elif platform == "darwin":
    system = 'osx'
elif platform == "win32":
    stockpath = os.path.join(BASE_DIR,'engine/stockfish_15_win_x64/stockfish_15_win_x64/stockfish_15_x64.exe')

ROWS = 8

class board():
    def __init__(self):
        try:
            self.stockfish = Stockfish(path=stockpath,parameters={"Skill Level": 8})
            self.stockfish.set_position([])
        except Exception as e:
            print("Errore nel caricamento di stockfish: ",e)
        self.board = chess.Board()
    
    def stringify_board(self,board):
        b = ''
        for piece in str(board):
            if piece != '\n' and piece != ' ':
                b += piece
        b = b[::-1]
        print(b)
        return b

    def update(self,allmovesmade):
        if allmovesmade == '':
            return
        uci_moves = allmovesmade.split()
        
        try:
            self.stockfish.set_position(uci_moves)
        except Exception as e:
            print("Stockfish not loaded")

        for move in uci_moves:
            self.board.push(chess.Move.from_uci(move))
    
    def dictify_legal_moves(self,movefrom):
        str_moves = [str(x) for x in self.board.legal_moves if movefrom in str(x)]
        #non mi importa delle chiavi, fa comodo struttura dizionario per json ajax
        return {hash(x):x for x in str_moves }
    
    def return_updated_position_after_move(self,position,move):
        self.update(position)
        self.board.push(chess.Move.from_uci(move))
        gameover = self.board.outcome()
        self.stockfish.make_moves_from_current_position([move])
        opponent_move = self.stockfish.get_best_move_time(1000)
        self.stockfish.make_moves_from_current_position([opponent_move])
        self.board.push(chess.Move.from_uci(opponent_move))
        gameover = self.board.outcome()
        if gameover != None:
            gameover = gameover.result()
        else:
            gameover = None
        return self.stringify_board(str(self.board)),opponent_move, gameover

    def object_move(self,uci):
        return chess.Move.from_uci(uci)

    def is_legal(self,move):
        if self.object_move(move) in self.board.legal_moves:
            return True
        else:
            return False

    def move_online(self,allmoves,last_move):
        self.update(allmoves)
        self.board.push(chess.Move.from_uci(last_move))
        gameover = self.board.outcome()
        if gameover != None:
            gameover = gameover.result()
        else:
            gameover = ''
        return self.stringify_board(str(self.board)), gameover
    

#dict_ex[new_key] = dict_ex[old_key]
#del dict_ex[old_key]

if __name__ == '__main__':
    b = board()
    print(str(b.board))
    b.board.push_san('e4')
    print(b.board.legal_moves)
    mossa = chess.Move.from_uci("g1f3")
    b.board.push(mossa)  # Make the move