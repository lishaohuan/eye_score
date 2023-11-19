from face_landmark_module import Face_Landmark_Module
from hand_landmark_module import Hand_Landmark_Module
import mediapipe as mp
import cv2
import pygame
from threading import Thread
import time
import tkinter as tk
from PIL import Image, ImageTk
import check_eye


def play_sound_warning():
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('warning.mp3'))
    time.sleep(1)

def play_music():
    global part, ending_part
    time_stamp = [48, 92, 134, 176] # 各节开始的时刻，以秒计数
    time_length_per_part = 30 # 每节时长
    pygame.mixer.music.load('eye_score_bgm.mp3')
    pygame.mixer.music.play() # 开始播放音乐
    time_start = time.perf_counter()
    if __debug__:
        print(time.strftime("开始做操时间: %Y-%m-%d %H:%M:%S",time.localtime()))
    while pygame.mixer.music.get_busy():
        time.sleep(1)
        time_now = time.perf_counter()
        if __debug__:
            print("做操持续时间: %.0f 秒 " %(time_now - time_start))
        # 判断当前是第几节
        if (time_now - time_start > time_stamp[0] and time_now - time_start < time_stamp[0] + time_length_per_part):
            part = 0  # 第一节
        elif (time_now - time_start > time_stamp[1] and time_now - time_start < time_stamp[1] + time_length_per_part):
            part = 1  # 第二节
        elif (time_now - time_start > time_stamp[2] and time_now - time_start < time_stamp[2] + time_length_per_part):
            part = 2  # 第三节
        elif (time_now - time_start > time_stamp[3] and time_now - time_start < time_stamp[3] + time_length_per_part):
            part = 3  # 第四节
        else:
            part = -1 # 其他：未开始、已结束或各节之间的时间
        # 判断是否进入收尾阶段
        if (time_now - time_start > time_stamp[3] + time_length_per_part):
            ending_part = 1

def show_frame():
    global frame_count, frame_interval
    global current_part, part
    global score_frame, failed_frame_num
    global part_frames, part_frames_success
    global save_flag

    # 读取一帧
    ret, frame = cap.read()

    if ret:
        if (current_part != part and part != -1):
            current_part = part
            new_text = "第" + str(current_part+1) + "节"
            label_top.configure(text=new_text)

        frame_count += 1
        if (frame_count % frame_interval > 0):
            pass

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        face_module.landmarker.detect_async(mp_image, frame_count)
        hand_module.landmarker.detect_async(mp_image, frame_count)
 
        # 等待10ms后取检测结果
        time.sleep(0.01)
        annotated_image = face_module.draw_landmarks_on_image(frame, face_module.results)
        annotated_image = hand_module.draw_landmarks_on_image(annotated_image, hand_module.results)

        if (part == 0):
            score_frame = check_eye.check_part_1_results(face_module.results.face_landmarks, hand_module.results.hand_landmarks)
            part_frames[0] += 1
            if (score_frame >= 3):
                part_frames_success[0] += 1
                failed_frame_num = 0
            else:
                failed_frame_num += 1
        elif (part == 1):
            score_frame = check_eye.check_part_2_results(face_module.results.face_landmarks, hand_module.results.hand_landmarks)
            part_frames[1] += 1
            if (score_frame >= 3):
                part_frames_success[1] += 1
                failed_frame_num = 0
            else:
                failed_frame_num += 1
        elif (part == 2):
            score_frame = check_eye.check_part_3_results(face_module.results.face_landmarks, hand_module.results.hand_landmarks)
            part_frames[2] += 1
            if (score_frame >= 3):
                part_frames_success[2] += 1
                failed_frame_num = 0
            else:
                failed_frame_num += 1
        elif (part == 3):
            score_frame = check_eye.check_part_4_results(face_module.results.face_landmarks, hand_module.results.hand_landmarks)
            part_frames[3] += 1
            if (score_frame >= 3):
                part_frames_success[3] += 1
                failed_frame_num = 0
            else:
                failed_frame_num += 1
        else:
            if (current_part != -1):
                text_between_parts = "第" + str(current_part+1) + "节得分: " + str(round(100.0*float(part_frames_success[current_part])/float(part_frames[current_part])))
                label_top.configure(text=text_between_parts)
                if __debug__:
                    print(text_between_parts)
                failed_frame_num = 0

        if (failed_frame_num >= 50):  # 连续50帧不成功，文字+声音报警，保存错误图片
            text_warning = "检测到不标准动作，为保护眼睛，请纠正！"
            label_mid.configure(fg="red")
            label_mid.configure(text=text_warning)
            if __debug__:
                print(text_warning)
            if (failed_frame_num == 50):
                start_sound_warning()
                cv2.imwrite("frame_" + str(frame_count) + "_warning.jpg", annotated_image)
        else:
            label_mid.configure(text="")
        
        if (ending_part == 1):
            failed_frame_num = 0
            # 计算各节的得分
            eye_score = [0, 0, 0, 0]
            eye_score_str = ""
            for i in range(4):
                eye_score[i] = round(100.0*float(part_frames_success[i])/float(part_frames[i]))
                eye_score_str += str(eye_score[i]) + " "
            text_ending = "各节得分: [ " + eye_score_str + "] 眼保健操结束, 谢谢使用AI眼天使!"
            label_mid.configure(fg="blue")
            label_mid.configure(text=text_ending)
            if __debug__:
                print(text_ending)
        
        if (save_flag == 1):
            cv2.imwrite("frame_" + str(frame_count) + ".jpg", annotated_image)
            save_flag = 0

        # 显示当前帧图像
        gui_frame = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(gui_frame)
        photo = ImageTk.PhotoImage(image=img)
        label_frame.photo = photo
        label_frame.configure(image=photo)  

    # 20ms后运行下一帧
    window.after(20, show_frame)


def start_music():
    print("开始播放音乐")
    t1 = Thread(target=play_music)
    t1.setDaemon(True)
    t1.start()

def start_sound_warning():
    print("开始播放警告声音")
    t2 = Thread(target=play_sound_warning)
    t2.setDaemon(True)
    t2.start()

def save_image():
    global save_flag
    save_flag = 1

# --- main ---

part = -1                            # 各节的编号，-1表示未开始或已结束
ending_part = 0                      # 是否进入收尾阶段
frame_count = 0                      # 帧计数
frame_interval = 2                   # 帧间隔，即几帧处理一帧
score_frame = 0                      # 当前帧的得分
current_part = -1                    # 当前节的编号，-1表示未开始或已结束
part_frames = [0, 0, 0, 0]           # 各节的总帧数
part_frames_success = [0, 0, 0, 0]   # 各节的成功帧数
failed_frame_num = 0                 # 连续不成功的帧数
save_flag = 0                        # 是否保存当前帧

# 加载模型
face_module = Face_Landmark_Module()
face_module.load_model('face_landmarker.task')
hand_module = Hand_Landmark_Module()
hand_module.load_model('hand_landmarker.task')

# 初始化视频和音频
cap = cv2.VideoCapture(0)
pygame.mixer.init()

# 初始化图形界面
window = tk.Tk()
window.title("欢迎使用AI眼天使")
width=(int)(window.winfo_screenwidth()*0.7)
height=(int)(window.winfo_screenheight()*0.7)
window.geometry(f"{width}x{height}")
window.resizable(1, 1)

# 创建标题区域
label_top = tk.Label(window, text="点击 [开始] 按钮或按空格键盘播放眼保健操音乐")
label_top.grid(column=0, row=0)
# 创建提示区域
label_mid = tk.Label(window, text="")
label_mid.grid(column=0, row=1)
label_mid.configure(font=("Arial", 20))
# 创建显示视频的区域
label_frame = tk.Label(window, width=width, height=(height-100))
label_frame.grid(column=0, row=2)
# 创建开始按钮
button = tk.Button(window, text="开始", command=start_music)
button.grid(column=0, row=3)
# 绑定快捷键
window.bind('<Escape>', lambda e: window.quit())
window.bind('<space>', lambda e: start_music())
window.bind('<Return>', lambda e: save_image())

# 开始显示视频
show_frame()

# 开始运行窗口
window.mainloop()
