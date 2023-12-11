import json
import copy
import cv2
from ultralytics import YOLO

with open('DataSet/ChessReD/original/annotations.json', 'r') as f:
    CRD_json = json.load(f)
    
my_json = copy.copy(CRD_json)

CRD_pieces = CRD_json['annotations']['pieces']
CRD_images = CRD_json['images']

exist_pieces_annotation = set()
empty_pieces_annotation = set()
for pieces_on_image in CRD_pieces:
    if ('bbox' in pieces_on_image):
        exist_pieces_annotation.add(pieces_on_image['image_id'])
    else:
        empty_pieces_annotation.add(pieces_on_image['image_id'])

predictor = YOLO('YOLOv8/best/ChessPieces/weights/best.pt')

for images_id in list(empty_pieces_annotation):
    json_image = CRD_images[images_id]

    img = cv2.imread('DataSet/ChessReD/non_annotations_images/' + json_image['path'])
    w, h = json_image['width'], json_image['height']

    result = predictor(img)

    path_annotations = json_image['path'][:-3]+'txt'
    print(path_annotations)

    with open('DataSet/ChessReD/non_annotations_images/'+path_annotations,'w') as annotations:
        for r in result:
            boxes = r.boxes
            for box in boxes:
                c = str(int(box.cls.cpu().numpy()))
                x, y, w, h = box.xywhn[0].cpu().numpy()
                annotations.write(f'{c} {str(x)} {str(y)} {str(w)} {str(h)}\n')