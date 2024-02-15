import cv2

cap = cv2.VideoCapture("PXL_20231205_031521968.TS~2_new.mp4")

while cap.isOpened():
    success, frame = cap.read()
    if success:
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
