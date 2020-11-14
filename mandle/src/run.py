import cv2
import time
from src.hand_tracker import HandTracker
import src.motionCheck as MotionCheck
import sys
import json
class mandle_run():
    def jsonRead(self):
        with open("data.json", "r") as data_json:
            resultset = json.load(data_json)
            return resultset
    def exit_pro(self):
        self.hasFrame = False
        cv2.destroyAllWindows()
    hasFrame = False
    def start_run(self):
        WINDOW = u"Mandle - Montion Handler"
        PALM_MODEL_PATH = "models/palm_detection_without_custom_op.tflite"
        LANDMARK_MODEL_PATH = "models/hand_landmark.tflite"
        ANCHORS_PATH = "models/anchors.csv"

        POINT_COLOR = (255, 255, 255)
        CONNECTION_COLOR = (0, 0, 0)
        THICKNESS = 2 

        #cv2.namedWindow(WINDOW)
        capture = cv2.VideoCapture(0)

        if capture.isOpened():
            self.hasFrame, frame = capture.read()
        else:
            self.hasFrame = False

        #        8   12  16  20
        #        |   |   |   |
        #        7   11  15  19
        #    4   |   |   |   |
        #    |   6   10  14  18
        #    3   |   |   |   |
        #    |   5---9---13--17
        #    2    \         /
        #     \    \       /
        #      1    \     /
        #       \    \   /
        #        ------0-
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (5, 6), (6, 7), (7, 8),
            (9, 10), (10, 11), (11, 12),
            (13, 14), (14, 15), (15, 16),
            (17, 18), (18, 19), (19, 20),
            (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)
        ]

        detector = HandTracker(
            PALM_MODEL_PATH,
            LANDMARK_MODEL_PATH,
            ANCHORS_PATH,
            box_shift=0.2,
            box_enlarge=1.3
        )
        
        #json읽어오기
        data_json = self.jsonRead()

        prevTime = 0
        prev_motion_num = 0
        prev_motion_point = (0,0)
        while self.hasFrame:
            frame = cv2.flip(frame,1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            points, _ = detector(image)
            if points is not None:
                prev_motion_num, prev_motion_point= MotionCheck.checkFinger(frame,points,prev_motion_num, prev_motion_point,data_json)
                print(prev_motion_num, prev_motion_point)
                pntcnt = 0
                for connection in connections:
                    x0, y0 = points[connection[0]]
                    x1, y1 = points[connection[1]]
                    cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), CONNECTION_COLOR, THICKNESS)
                for point in points:
                    x, y = point
                    pntstr = "%d" % pntcnt
                    cv2.circle(frame, (int(x), int(y)), THICKNESS * 2, POINT_COLOR, THICKNESS)
                    #cv2.putText(frame, pntstr, (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0+pntcnt*10,255-pntcnt*10,50+pntcnt*5))
                    pntcnt += 1
                
            else :
                cv2.putText(frame, "None", (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
            
            
            #현재 시간 가져오기 (초단위로 가져옴)
            curTime = time.time()
            #한번 돌아온 시간!!
            sec = curTime - prevTime
            #이전 시간을 현재시간으로 다시 저장시킴
            prevTime = curTime
            # 프레임 계산 한바퀴 돌아온 시간을 1초로 나누면 된다.
            fps = 1/(sec)
            str = "%0.1f FPS" % fps
            cv2.putText(frame, str, (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0))
            

            #인식 화면 출력
            #cv2.imshow(WINDOW, frame)
            
            #캡쳐정보다시 읽기
            hasFrame, frame = capture.read()
            key = cv2.waitKey(1)
            if key == 27:
                break

        capture.release()
        cv2.destroyAllWindows()
