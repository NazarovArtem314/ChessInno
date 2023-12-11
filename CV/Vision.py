from io import BytesIO
import numpy as np
from PIL import Image
from cairosvg import svg2png
import cv2
import chess
import chess.svg
from numpy.linalg import norm

pieces_name_RGB = {
    'white-pawn':   ( 77, 255,  77), #(  0, 179,   0)
    'white-rook':   (255, 255,  77),
    'white-knight': (255,  77, 255),
    'white-bishop': ( 77,  77, 255), #(  0,   0, 179)
    'white-queen':  (179,   0,   0),
    'white-king':   (255, 195,  77),
    'black-pawn':   (  0, 179,   0), #( 77, 255,  77)
    'black-rook':   (178, 179,   0),
    'black-knight': (179,   0, 178),
    'black-bishop': (  0,   0, 179), #( 77,  77, 255)
    'black-queen':  (255,  77,  77),
    'black-king':   (179, 119,   0),
}

pieces_name_BGR = {
    'white-pawn':   ( 77, 255,  77), #(  0, 179,   0)
    'white-rook':   ( 77, 255, 255),
    'white-knight': (255,  77, 255),
    'white-bishop': (255,  77,  77), #(179,   0,   0)
    'white-queen':  (  0,   0, 179),
    'white-king':   ( 77, 195, 255),
    'black-pawn':   (  0, 179,   0), #( 77, 255,  77)
    'black-rook':   (  0, 179, 178),
    'black-knight': (178,   0, 179),
    'black-bishop': (179,   0,   0), #(255,  77,  77)
    'black-queen':  ( 77,  77, 255),
    'black-king':   (  0, 119, 179),
}

pieces_number_RGB = {
    0:  ( 77, 255,  77), #(  0, 179,   0)
    1:  (255, 255,  77),
    2:  (255,  77, 255),
    3:  ( 77,  77, 255), #(  0,   0, 179)
    4:  (179,   0,   0),
    5:  (255, 195,  77),
    6:  (  0, 179,   0), #( 77, 255,  77)
    7:  (178, 179,   0),
    8:  (179,   0, 178),
    9:  (  0,   0, 179), #( 77,  77, 255)
    10: (255,  77,  77),
    11: (179, 119,   0),
}

pieces_number_BGR = {
    0:  ( 77, 255,  77), #(  0, 179,   0)
    1:  ( 77, 255, 255),
    2:  (255,  77, 255),
    3:  (255,  77,  77), #(179,   0,   0)
    4:  (  0,   0, 179),
    5:  ( 77, 195, 255),
    6:  (  0, 179,   0), #( 77, 255,  77)
    7:  (  0, 179, 178),
    8:  (178,   0, 179),
    9:  (179,   0,   0), #(255,  77,  77)
    10: ( 77,  77, 255),
    11: (  0, 119, 179),
}

def show_bord_FEN(FEN='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
    svg_data = chess.svg.board(chess.Board(FEN), size=350) 
    png = svg2png(bytestring=svg_data, dpi=1)
    pil_img = Image.open(BytesIO(png)).convert('RGBA')
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
    cv2.imshow('board', cv_img)


def draw_bbox(img, bbox, color=(0, 255, 0), thickness=10):
    img = cv2.rectangle(img, color=color, thickness=thickness,
                    pt1=(int((bbox[0]-bbox[2]/2)*img.shape[0]), int((bbox[1]-bbox[3]/2)*img.shape[1])),
                    pt2=(int((bbox[0]+bbox[2]/2)*img.shape[0]), int((bbox[1]+bbox[3]/2)*img.shape[1])))
    return img


def detect_pieces(result):
    x, y, c = [], [], []
    for r in result:
        boxes = r.boxes
        for box in boxes:
            c.append(int(box.cls.cpu().numpy()))

            b = box.xywh[0].cpu().numpy()
            x.append(int(b[0]))
            y.append(int(b[1]+b[3]*5/16))

    return np.array([x, y, c]).T


def detect_corner(result_of_prediction):

    dict_pieces_position = {1:  [],
                            5:  [],
                            7:  [],
                            11: [],}


    dict_corner = {}




    for r in result_of_prediction:
        boxes = r.boxes
        for box in boxes:
            
            b = box.xywh[0].cpu().numpy()
            c = int(box.cls.cpu().numpy())

            x, y = int(b[0]), int(b[1]+b[3]*2.75/8)

            if c in dict_pieces_position:
                dict_pieces_position[c].append(np.array([x, y]))

    l1 = norm(dict_pieces_position[1][0] - dict_pieces_position[5][0])
    l2 = norm(dict_pieces_position[1][1] - dict_pieces_position[5][0])

    if l1 > l2:
        dict_corner['BL'] = dict_pieces_position[1][0]
        dict_corner['BR'] = dict_pieces_position[1][1]
    else:
        dict_corner['BL'] = dict_pieces_position[1][1]
        dict_corner['BR'] = dict_pieces_position[1][0]    


    l1 = norm(dict_pieces_position[7][0] - dict_pieces_position[11][0])
    l2 = norm(dict_pieces_position[7][1] - dict_pieces_position[11][0])

    if l1 > l2:
        dict_corner['TL'] = dict_pieces_position[7][0]
        dict_corner['TR'] = dict_pieces_position[7][1]
    else:
        dict_corner['TL'] = dict_pieces_position[7][1]
        dict_corner['TR'] = dict_pieces_position[7][0]   


    ans = np.array(
    [dict_corner['BR'],
     dict_corner['TR'], 
     dict_corner['TL'], 
     dict_corner['BL']],
    dtype=np.float32)
    return ans


def get_matrix_transform(src, image_size):
    w, h = image_shape
    dst =  np.array([[15/16*w, 15/16*h],
                     [15/16*w, 1/16*h], 
                     [ 1/16*w, 1/16*h], 
                     [ 1/16*w, 15/16*h]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(src, dst)
    return M


def coord_transform(x, y, c, M):
    new_xy = M @ np.array([x, y, 1])
    new_xy = new_xy / new_xy[2]
    new_xy[2] = c
    return new_xy

