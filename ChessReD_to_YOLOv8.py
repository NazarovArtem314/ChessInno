import json
import cv2
import numpy as np
import os



# read original annotations
with open('DataSet/ChessReD/original/annotations.json', 'r') as f:
    CRD_json = json.load(f)
    
CRD_pieces = CRD_json['annotations']['pieces']
CRD_corners = CRD_json['annotations']['corners']
CRD_images = CRD_json['images']



# checking annotation for a chess piece
exist_pieces_annotation = set()
empty_pieces_annotation = set()
for pieces_on_image in CRD_pieces:
    if ('bbox' in pieces_on_image):
        exist_pieces_annotation.add(pieces_on_image['image_id'])
    else:
        empty_pieces_annotation.add(pieces_on_image['image_id'])



# checking annotation for a chess piece
exist_corners_annotation = set()
empty_corners_annotation = set()
for corners_on_image in CRD_corners:
    if ('corners' in corners_on_image):
        exist_corners_annotation.add(corners_on_image['image_id'])
    else:
        empty_corners_annotation.add(corners_on_image['image_id'])



# exsist/empty annotations proportion
if exist_corners_annotation == exist_pieces_annotation:
    print(f'''exsist/empty annotations proportion: {len(exist_pieces_annotation)/(len(exist_pieces_annotation)+len(empty_pieces_annotation)):.3f}''')
else:
    print(f'''exsist/empty annotations proportion (for pieces): {len(exist_pieces_annotation)/(len(exist_pieces_annotation)+len(empty_pieces_annotation)):.3f}''')
    print(f'''exsist/empty annotations proportion (for corners): {len(exist_corners_annotation)/(len(exist_corners_annotation)+len(empty_corners_annotation)):.3f}''')



# save non annotations images
os.makedirs('DataSet/ChessReD/non_annotations_images/images')
for id in list(empty_pieces_annotation):
    img = cv2.imread('DataSet/ChessReD/original/chessred/' + CRD_images[id]['path'])
    img = cv2.resize(img, (640, 640))
    if not os.path.exists('DataSet/ChessReD/non_annotations_images/'+CRD_images[id]['path'][:-len(CRD_images[id]['file_name'])-1]):
        os.makedirs('DataSet/ChessReD/non_annotations_images/'+CRD_images[id]['path'][:-len(CRD_images[id]['file_name'])-1])
    cv2.imwrite('DataSet/ChessReD/non_annotations_images/' + CRD_images[id]['path'], img)



# train, val, test split
train = set()
val = set()
test = set()

np.random.seed(42)
shufle_exist_image = list(exist_pieces_annotation)
np.random.shuffle(shufle_exist_image)

c = 1
for i in shufle_exist_image:
    if c <= len(exist_pieces_annotation) * 0.7:
        train.add(i)
    elif len(exist_pieces_annotation) * 0.7 < c <= len(exist_pieces_annotation) * 0.85:
        val.add(i)
    else:
        test.add(i)
    c += 1



# create learn directory
learn_directory = 'pieces'
os.makedirs(f'DataSet/ChessReD/{learn_directory}/test')
os.makedirs(f'DataSet/ChessReD/{learn_directory}/train')
os.makedirs(f'DataSet/ChessReD/{learn_directory}/val')



# save annotations (image_name.txt)
for pieces_on_image in CRD_pieces:
    image_id = pieces_on_image['image_id']
    
    if image_id in exist_pieces_annotation:
        file_name = CRD_images[image_id]['file_name'].strip('jpg')+'txt'
        width = CRD_images[image_id]['width']
        height = CRD_images[image_id]['height']
        
        resize_x = (pieces_on_image['bbox'][0] + pieces_on_image['bbox'][2]/2)/width
        resize_y = (pieces_on_image['bbox'][1] + pieces_on_image['bbox'][3]/2)/height
        resize_width  = pieces_on_image['bbox'][2]/width
        resize_height = pieces_on_image['bbox'][3]/height

        bbox = [resize_x, resize_y, resize_width, resize_height]
        category = pieces_on_image['category_id']

        if image_id in train:
            with open('DataSet/ChessReD/'+learn_directory+'/train/'+file_name,'a') as annotations:
                annotations.write(' '.join(list(map(str,([category] + bbox))))+'\n')

        if image_id in val:
            with open('DataSet/ChessReD/'+learn_directory+'/val/'+file_name,'a') as annotations:
                annotations.write(' '.join(list(map(str,([category] + bbox))))+'\n')

        if image_id in test:
            with open('DataSet/ChessReD/'+learn_directory+'/test/'+file_name,'a') as annotations:
                annotations.write(' '.join(list(map(str,([category] + bbox))))+'\n')



# save image (image_name.jpg)
for image_id in list(exist_pieces_annotation):
    if image_id in train:
        img = cv2.imread('DataSet/ChessReD/original/chessred/' + CRD_images[image_id]['path'])
        img = cv2.resize(img, (640, 640))
        cv2.imwrite('DataSet/ChessReD/'+learn_directory+'/train/' + CRD_images[image_id]['file_name'], img)

    if image_id in val:
        img = cv2.imread('DataSet/ChessReD/original/chessred/' + CRD_images[image_id]['path'])
        img = cv2.resize(img, (640, 640))
        cv2.imwrite('DataSet/ChessReD/'+learn_directory+'/val/' + CRD_images[image_id]['file_name'], img)

    if image_id in test:
        img = cv2.imread('DataSet/ChessReD/original/chessred/' + CRD_images[image_id]['path'])
        img = cv2.resize(img, (640, 640))
        cv2.imwrite('DataSet/ChessReD/'+learn_directory+'/test/' + CRD_images[image_id]['file_name'], img)