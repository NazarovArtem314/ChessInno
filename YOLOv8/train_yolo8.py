from ultralytics import YOLO

model = YOLO('YOLOv8/yolov8n.pt')
results = model.train(data='DataSet/ChessReD/corners.yaml',
                      epochs=150, imgsz=640,
                      device='cpu',
                      optimizer='AdamW', iou=0.9,
                      lr0=0.001, lrf=0.00005)