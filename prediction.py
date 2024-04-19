import cv2
import numpy as np
from ultralytics import YOLO
from help import get_coords
from sympy import Point, Polygon

def predict(cap_file, tetragons_file):
    do_cap = True

    model = YOLO('yolov8n')

    # cap = cv2.VideoCapture('test.mp4')
    # cap = cv2.VideoCapture('PXL_20231205_031521968.TS~2_new.mp4')
    # cap = cv2.VideoCapture('PXL_20231202_044440610.TS~2_CUT.mp4')
    # cap = cv2.VideoCapture('PXL_20231202_044440610.TS~2.mp4')
    cap = cv2.VideoCapture(cap_file)

    # Получение координат четырехугольника из файла
    # tetragons = get_coords('poly_vertex.txt')
    tetragons = get_coords(tetragons_file)

    # Преобразование: список(кортеж(число, число)) -> список(Polygon(Point2D, Point2D))
    drawed_tetragons = list(map(lambda x: Polygon(*x), tetragons))

    # Задаю цвета
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)

    # Перебор кадров
    while cap.isOpened():
        # Чтение кадра
        success, frame = cap.read()

        if not do_cap:
            do_cap = not do_cap
            continue

        # Если кадр есть
        if success:
            # Результат обработки кадра
            results = list(model.track(frame, persist=True, imgsz=320))
            annotated_frame = frame

            # Создание "запрещенных четырехугольников"
            for tetragon in tetragons:
                draw = np.array(tetragon, np.int32)
                cv2.polylines(annotated_frame, [draw], True, (0, 255, 255), 3, lineType=3)
                cv2.line(annotated_frame, draw[1], draw[3], (0, 255, 255), 3)
                cv2.line(annotated_frame, draw[0], draw[2], (0, 255, 255), 3)

            # Узнаю размер окна (высота, ширина)
            orig_shape = results[0].orig_shape
            # Все определенные объекты
            res = results[0].boxes.xyxyn.tolist()

            print(f'Все объекты: {res}')

            # Если на кадре обнаружены объекты
            if res:
                for i in range(len(res)):  # Для каждого объекта
                    # Координаты углов коробки
                    box_cords = res[i]
                    box = [(int(box_cords[0] * orig_shape[1]), int(box_cords[1] * orig_shape[0])),
                           (int(box_cords[2] * orig_shape[1]), int(box_cords[1] * orig_shape[0])),
                           (int(box_cords[2] * orig_shape[1]), int(box_cords[3] * orig_shape[0])),
                           (int(box_cords[0] * orig_shape[1]), int(box_cords[3] * orig_shape[0]))]

                    print(f'Коробка нынешнего объекта{box_cords}')

                    # Координата точки ног объекта
                    centre_coord = (int(((box_cords[0] + box_cords[2]) / 2) * orig_shape[1]),
                                    int((box_cords[3]) * orig_shape[0]))
                    # Отображение точки
                    cv2.circle(annotated_frame, centre_coord, 6, (255, 0, 0), -1)

                    # Отображение рамок объектов
                    for polygon in drawed_tetragons:  # Для каждой рамки
                        # Если точка внутри четырехугольника
                        if polygon.encloses_point(Point(centre_coord[0], centre_coord[1])):
                            cv2.putText(annotated_frame, "Danger!", (50, 900), cv2.FONT_HERSHEY_SIMPLEX,
                                        5, (0, 0, 255), 2)
                            cv2.rectangle(annotated_frame, box[0], box[2], RED, 4)
                print("YES")
            else:
                cv2.putText(annotated_frame, "Out of frame!", (50, 900), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 2)

            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # break

            do_cap = not do_cap

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    predict(0, 'empty.txt')
    