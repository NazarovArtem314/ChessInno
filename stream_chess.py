import cv2
import numpy as np
from ultralytics import YOLO
from CV.Vision import detect_corner, get_matrix_transform, detect_pieces, pieces_number_RGB

vid = cv2.VideoCapture(2)
# vid.set(cv2.CAP_PROP_FPS, 10) 

HumanOrNone = YOLO('YOLOv8/best/HumanOrNone/best.pt')
Pieces = YOLO('YOLOv8/best/ChessPieces/weights/best.pt')


while False:
    ret, frame = vid.read()

    frame = frame[:,80:-80,:]
    frame = frame[:,::-1,:]
    frame = cv2.resize(frame, (640,640))

    result_for_corner = Pieces.predict(frame, device='cpu')
    src = detect_corner(result_for_corner)
    M = get_matrix_transform(src, (640, 640))

    frame_transform = cv2.warpPerspective(frame, M, (640, 640))

    cv2.imshow('Stream', frame)
    cv2.imshow('Transform', frame_transform)

    if cv2.waitKey(1) & 0xFF == ord('n'): 
        break


while True:
    ret, frame = vid.read()

    # frame = frame[:,80:-80,:]
    # frame = frame[:,::-1,:]
    # frame = cv2.resize(frame, (640,640))

    # result_classification = HumanOrNone.predict(frame)
    result_chess_pieces = Pieces.predict(frame)
    coord_pieces = detect_pieces(result_chess_pieces)

    if coord_pieces.shape[0] != 0:
        for x_coord, y_coord, pieces in coord_pieces:
            frame = cv2.circle(frame, (x_coord, y_coord), 6, pieces_number_RGB[pieces], -1)


    # for r in result_classification:
    #     if r.probs.top1 == 1:
    #         HumanOrNone_color = (0, 0, 255)
    #     else:
    #         HumanOrNone_color = (0, 255, 0)

    # frame = cv2.rectangle(frame, (0, 0), frame.shape[:2], HumanOrNone_color, 10)
    cv2.imshow('Stream', frame)
      
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

vid.release()
cv2.destroyAllWindows()