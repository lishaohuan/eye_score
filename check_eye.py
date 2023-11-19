# 检查第一节的正确性，揉耳垂
def check_part_1_results(face_landmarks, hand_landmarks):
    score = 0
    if face_landmarks and hand_landmarks:
        if len(hand_landmarks) < 2:
            if __debug__:
                print("第一节: 未能识别出两只手")
            return score

        face_mark = face_landmarks[0]
        # 脸部关键点
        #   139          368   # 上眼角持平,耳朵中上部
        #   34            264  # 中眼角持平,耳朵中上部 
        #  227            447
        #      50    280       # 脸部边缘
        #  147            376 
        #  177            401  # 耳朵下部
        right_face_x    = max(face_mark[139].x, face_mark[34].x,
                              face_mark[227].x, face_mark[50].x,
                              face_mark[147].x, face_mark[177].x)
        right_face_y_up = min(face_mark[139].y, face_mark[34].y)
        left_face_x     = min(face_mark[368].x, face_mark[264].x,
                              face_mark[447].x, face_mark[280].x,
                              face_mark[376].x, face_mark[401].x)
        left_face_y_up  = min(face_mark[368].y, face_mark[264].y)

        # 左右手定位
        if hand_landmarks[0][20].x > hand_landmarks[1][20].x:
            left_hand_mark = hand_landmarks[0]
            right_hand_mark = hand_landmarks[1]
        else:
            left_hand_mark = hand_landmarks[1]
            right_hand_mark = hand_landmarks[0]

        # 左手关键点位置
        left_hand_x = max(left_hand_mark[6].x, left_hand_mark[10].x)
        left_hand_y = min(left_hand_mark[6].y, left_hand_mark[10].y)
        # 右手关键点位置
        right_hand_x = min(right_hand_mark[6].x, right_hand_mark[10].x)
        right_hand_y = min(right_hand_mark[6].y, right_hand_mark[10].y)
        
        # 检查位置的规则
        if left_hand_x >= left_face_x and left_hand_y >= left_face_y_up:
            score = score + 1
        if right_hand_x <= right_face_x and right_hand_y >= right_face_y_up: 
            score = score + 2
        if score == 3:
            if __debug__:
                print(f"第一节: 动作规范, 得{score} 分")
        else:
            if __debug__:
                print(f"第一节: 动作不规范, 得{score} 分")
    else:
        if __debug__:
            print("第一节: 无效图片,识别脸部和手失败")

    return score

# 检查第二节的正确性，揉太阳穴刮上眼眶
def check_part_2_results(face_landmarks, hand_landmarks):
    score = 0
    if face_landmarks and hand_landmarks:
        if len(hand_landmarks) < 2:
            if __debug__:
                print("第二节: 未能识别出两只手")
            return score

        face_mark = face_landmarks[0]
        # 脸部关键点
        #          109  338             # 脸最上面，额头
        #
        # 162                     389   # 脸左右边缘
        #     229 230     449 450         
        face_left_x  = face_mark[389].x
        face_right_x = face_mark[162].x
        face_up_y    = min(face_mark[109].y, face_mark[338].y)
        face_low_y   = max(face_mark[229].y, face_mark[230].y,
                           face_mark[449].y, face_mark[450].y)

        # 左右手定位
        if hand_landmarks[0][20].x > hand_landmarks[1][20].x:
            left_hand_mark = hand_landmarks[0]
            right_hand_mark = hand_landmarks[1]
        else:
            left_hand_mark = hand_landmarks[1]
            right_hand_mark = hand_landmarks[0]
        
        # 左手关键点位置
        left_index_x = left_hand_mark[6].x
        left_index_y = left_hand_mark[6].y 
        # 右手关键点位置
        right_index_x = right_hand_mark[6].x
        right_index_y = right_hand_mark[6].y 

        # 检查位置的规则
        if  left_index_x <= face_left_x and \
            left_index_x >= face_right_x and \
            left_index_y >= face_up_y and \
            left_index_y <= face_low_y:
            score += 1
        if  right_index_x <= face_left_x and \
            right_index_x >= face_right_x and \
            right_index_y >= face_up_y and \
            right_index_y <= face_low_y:
            score += 2
        if score == 3:
            if __debug__:
                print(f"第二节: 动作规范, 得{score} 分")
        else:
            if __debug__:
                print(f"第二节: 动作不规范, 得{score} 分")
    else:
        if __debug__:
            print("第二节: 无效图片,识别脸部和手失败")

    return score

# 检查第三节的正确性,摁四白穴
def check_part_3_results(face_landmarks, hand_landmarks):
    score = 0
    if face_landmarks and hand_landmarks:
        if len(hand_landmarks) < 2:
            if __debug__:
                print("第三节: 未能识别出两只手")
            return score

        face_mark = face_landmarks[0]
        # 脸部关键点
        #  117                128         357                  346
        #   50                   188  412                      280
        #      36 142 126 217                 437 355 371 266
        right_face_left_x  = min(face_mark[50].x, face_mark[117].x)
        right_face_right_x = max(face_mark[128].x, face_mark[188].x) 
        right_face_up_y    = min(face_mark[117].y, face_mark[128].y)
        right_face_low_y   = max(face_mark[36].y, face_mark[142].y,
                                 face_mark[126].y, face_mark[217].y)

        left_face_left_x   = min(face_mark[357].x, face_mark[412].x)
        left_face_right_x  = max(face_mark[280].x, face_mark[346].x)
        left_face_up_y     = min(face_mark[357].y, face_mark[346].y)
        left_face_low_y    = max(face_mark[266].y, face_mark[371].y,
                                 face_mark[355].y, face_mark[437].y)

        # 左右手定位
        if hand_landmarks[0][20].x > hand_landmarks[1][20].x:
            left_hand_mark = hand_landmarks[0]
            right_hand_mark = hand_landmarks[1]
        else:
            left_hand_mark = hand_landmarks[1]
            right_hand_mark = hand_landmarks[0]
            
        # 左手关键点位置
        left_hand_x = left_hand_mark[8].x
        left_hand_y = left_hand_mark[8].y 
        # 右手关键点位置
        right_hand_x = right_hand_mark[8].x
        right_hand_y = right_hand_mark[8].y  
        
        # 检查位置的规则
        if  left_hand_x >= left_face_left_x and \
            left_hand_x <= left_face_right_x and \
            left_hand_y >= left_face_up_y and \
            left_hand_y <= left_face_low_y:
            score += 1
        if  right_hand_x >= right_face_left_x and \
            right_hand_x <= right_face_right_x and \
            right_hand_y >= right_face_up_y and \
            right_hand_y <= right_face_low_y:
            score += 2
        if score == 3:
            if __debug__:
                print(f"第三节: 动作规范, 得{score} 分")
        else:
            if __debug__:
                print(f"第三节: 动作不规范, 得{score} 分")
    else:
        if __debug__:
            print("第三节: 无效图片,识别脸部和手失败")

    return score

# 检查第四节的正确性：揉按晴明穴
def check_part_4_results(face_landmarks, hand_landmarks):
    score = 0
    if face_landmarks and hand_landmarks:
        face_mark = face_landmarks[0]
        # 脸部关键点
        # 65            295
        #    221   441 
        #    114   343 
        # 142           371 
        face_left_x = min(face_mark[221].x,face_mark[114].x) 
        face_right_x = max(face_mark[441].x,face_mark[343].x) 
        face_up_y = min(face_mark[65].y, face_mark[295].y)
        face_low_y = max(face_mark[142].y, face_mark[371].y)

        hand_mark = hand_landmarks[0]
        # 选择合适位置的手
        if len(hand_landmarks) > 1:
            if hand_landmarks[0][4].y > hand_landmarks[1][4].y:
                hand_mark = hand_landmarks[1]
        
        # 拇指和食指的关键点
        thumb_x = hand_mark[4].x
        thumb_y = hand_mark[4].y 
        index_x = hand_mark[8].x
        index_y = hand_mark[8].y 

        # 检查位置的规则
        if  thumb_x >= face_left_x and \
            thumb_x <= face_right_x and \
            thumb_y >= face_up_y and \
            thumb_y <= face_low_y:
            score += 1
        if  index_x >= face_left_x and \
            index_x <= face_right_x and \
            index_y >= face_up_y and \
            index_y <= face_low_y:
            score += 2 
        if score == 3:
            if __debug__:
                print(f"第四节: 动作规范, 得{score} 分")
        else:
            if __debug__:
                print(f"第四节: 动作不规范, 得{score} 分")
    else:
        if __debug__:
            print("第四节: 无效图片,识别脸部和手失败")

    return score
