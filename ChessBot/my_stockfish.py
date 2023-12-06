from io import BytesIO
import numpy as np
from PIL import Image
from cairosvg import svg2png
import cv2
import chess
import chess.svg
from stockfish import Stockfish
from time import sleep

def show_bord_FEN(FEN='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
    svg_data = chess.svg.board(chess.Board(FEN), size=350) 
    png = svg2png(bytestring=svg_data, dpi=1)
    pil_img = Image.open(BytesIO(png)).convert('RGBA')
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
    cv2.imshow('cv_img', cv_img)

stockfish = Stockfish()
show_bord_FEN()

white_turn = True
while True:
    if white_turn:
        stockfish.make_moves_from_current_position([stockfish.get_best_move()])
        white_turn = False
    else:
        stockfish.make_moves_from_current_position([stockfish.get_best_move()])
        white_turn = True

    sleep(1)
    show_bord_FEN(stockfish.get_fen_position())    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        sleep(1)
        break
cv2.destroyAllWindows()

