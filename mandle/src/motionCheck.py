import cv2
import numpy as np
import math
import pyautogui as pg
import time
def checkFinger(frame,points,prev_motion_num, prev_motion_point,data_json):

    #다섯 손가락 각도
    fingerAngle = [0,0,0,0,0]
    #펴진 손가락 갯수
    fcnt = 0
    #모션포인트
    motionNum = 0
    for i in range(5): # 손가락 당
        for j in range(i*4+1,i*4+3): #첫번째 관절과 두번째 관절 반복
                # 벡터의 차이를 구하고
                ba = points[j] - points[j+1]
                bc = points[j+2] - points[j+1]
                # numpy를 통한 각도 계산을 합니다.
                cosine_angle = np.dot(ba,bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
                angle = np.arccos(cosine_angle) 
                pAngle = np.degrees(angle)
                # 해당 손가락이 얼만큼 굽혀졌는지의 정도를 모두 합합니다.
                fingerAngle[i] = fingerAngle[i] + abs(pAngle-180)

    # 각 손가락들의 굽혀진 각도를 리스트로 출력
    thumDegree = "/".join(["%d" % (_) for _ in fingerAngle])
    cv2.putText(frame, " Angle Degree : "+thumDegree, (130, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,100,0))
    
    # 굽혀졌다 판단한 손가락의 갯수를 구함
    for i in range(5):
        if i != 0:    
                if fingerAngle[i]<70: # 50미만인 경우 펴졌다고 판단
                        fcnt += 1
                        motionNum += (2 ** i)
        elif fingerAngle[i]<35: # 엄지의경우 35미만인 경우 펴졌다고 판단
                fcnt += 1
                motionNum += (2 ** i)
    
    fCntStr = "Finger Count : "+str(fcnt)

    cv2.putText(frame, fCntStr, (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
    
    # 이전 모션 포인트와 비교한 움직인 거리
    x1,y1 = points[0]
    x2,y2 = prev_motion_point
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

     
    keyset = [" ", "right", "left", "up","down","f"]
    # 엄지 1 검지 2 중지 4 약지 8 소지 16 비트합연산
    
    # 로큰롤
    if(bool(data_json["1"]["bool"])):
        if motionNum == 18 and dist > 50 and prev_motion_point[1] - points[0][1] > 50  :
                cv2.putText(frame, "rock & roll !!", (10, 140), cv2.FONT_HERSHEY_TRIPLEX, 2, (125,125,255))
                pg.press(keyset[int(data_json["1"]["action"])])

    # 총
    if motionNum == 3 and dist > 50:
            x1,y1 = points[5]
            x2,y2 = points[8]
            if x1 < x2 :
                if(bool(data_json["2"]["bool"])):
                        if points[0][0] - prev_motion_point[0] > 50: 
                                cv2.putText(frame, "Right Input", (10, 140), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (0,0,0))
                                pg.press(keyset[int(data_json["2"]["action"])]) 
            else : 
                if(bool(data_json["3"]["bool"])):
                        if prev_motion_point[0] - points[0][0] > 50 :
                                cv2.putText(frame, "Left Input", (10, 140), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (0,0,0))
                                pg.press(keyset[int(data_json["3"]["action"])]) 
    
    # 5손가락에서 락큰롤 3손가락
    if(bool(data_json["4"]["bool"])):
        if motionNum == 1+2+16 and dist < 10:
                if prev_motion_num ==  1+2+4+8+16:
                        cv2.putText(frame, "5->3", (10, 140), cv2.FONT_ITALIC, 2, (125,0,0))
                        pg.press(keyset[int(data_json["4"]["action"])])




#     # 오꼐이
#     if motionNum == 1+4+8+16 and abs(points[4][0]-points[8][0])+abs(points[4][1]-points[8][1]) < 20 and dist < 10:
#         cv2.putText(frame, "Ok!", (10, 140), cv2.FONT_ITALIC, 2, (125,0,0))
#         pg.press('right')

#     # 엄지척
#     if motionNum == 1  and dist > 50:
#             x1,y1 = points[4]
#             x2,y2 = points[17]
#             if y1 < y2 :
#                         if prev_motion_point[1] -points[0][1]> 50:
#                                 cv2.putText(frame, "Good!", (10, 140), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (0,125,0))
#                                 pg.press('up')
#             else :
#                 if points[0][1] - prev_motion_point[1] > 50:
#                         cv2.putText(frame, "Ooh..", (10, 140), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (0,0,255))
#                         pg.press('down') 
#     # 브이
#     if motionNum == 6 and dist > 100:
#             cv2.putText(frame, "V~", (10, 140), cv2.FONT_ITALIC, 2, (125,0,0))

            
    return motionNum,points[0]