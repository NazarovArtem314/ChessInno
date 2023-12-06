from ultralytics import YOLO
import cv2
from CV.Vision import draw_bbox, pieces_number_BGR
from ultralytics.utils.plotting import Annotator

model = YOLO('YOLOv8/runs/detect/train/weights/best.pt')
imgs_path = ['DataSet/ChessReD/resize_images/test/G000_IMG001.jpg',
             'DataSet/ChessReD/resize_images/test/G000_IMG013.jpg',
             'DataSet/ChessReD/resize_images/test/G006_IMG009.jpg',
             'DataSet/ChessReD/resize_images/test/G006_IMG024.jpg',
             'DataSet/ChessReD/resize_images/test/G006_IMG112.jpg',
             'DataSet/ChessReD/resize_images/test/G019_IMG020.jpg',]
for path in imgs_path:
    img = cv2.imread(path)
    result = model.predict(img)

    for r in result:
        boxes = r.boxes
        for box in boxes:
            
            b = box.xywh[0].cpu().numpy()
            c = box.cls.cpu().numpy()
            img = cv2.circle(img, (int(b[0]), int(b[1]+b[3]*3/8)), 6, pieces_number_BGR[int(c)], -1)

    cv2.imshow(path, img)
    cv2.waitKey(0)

cv2.destroyAllWindows()