from flask import Flask, render_template, Response
import cv2
import time
import RPi.GPIO as GPIO

app = Flask(__name__)

# OpenCV 설정
capture = cv2.VideoCapture(-1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Haar Cascade 로드 (얼굴 감지용)
face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')

# GPIO 설정
BUZZER_PIN = 18
SWITCH_PIN = 23
GREEN_LED_PIN = 7  # 초록색 LED
RED_LED_PIN = 25  # 빨간색 LED

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT) #부저
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #스위치
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)  # 초록색 LED 설정
GPIO.setup(RED_LED_PIN, GPIO.OUT)  # 빨간색 LED 설정

# 초기 상태 OFF
GPIO.output(BUZZER_PIN, GPIO.LOW)
GPIO.output(GREEN_LED_PIN, GPIO.LOW)
GPIO.output(RED_LED_PIN, GPIO.LOW)

# 상태 변수
face_missing_time = 0
alarm_triggered = False
button_press_count = 0  # 버튼 누른 횟수 저장

def turn_on_green_led():
    """초록색 LED 켜기 (Face Detected)"""
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    GPIO.output(RED_LED_PIN, GPIO.LOW)  # 빨간색 LED OFF

def turn_on_red_led():
    """빨간색 LED 켜기 (ALARM 상태)"""
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)  # 초록색 LED OFF

def sound_alarm():
    """스피커와 빨간 LED를 켜도록 설정."""
    print("ALARM: Sound ON, RED LED ON")
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    turn_on_red_led()

def stop_alarm():
    """스피커를 끄고 초록 LED를 켜도록 설정."""
    print("ALARM: Sound OFF, GREEN LED ON")
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    turn_on_green_led()

def gen_frames():
    global face_missing_time, alarm_triggered, button_press_count
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

            if len(faces) == 0:  # 얼굴이 감지되지 않음
                if not alarm_triggered:
                    if face_missing_time == 0:
                        face_missing_time = time.time()
                    elif time.time() - face_missing_time >= 2:  # 2초 이상 얼굴 감지 안됨
                        sound_alarm()
                        alarm_triggered = True
            else:  # 얼굴이 감지됨
                face_missing_time = 0
                if not alarm_triggered:
                    turn_on_green_led()  # 초록색 LED 켜기

            # 스위치로 알람 중단 (버튼 3번 누르면 알람 종료)
            if alarm_triggered and GPIO.input(SWITCH_PIN) == GPIO.LOW:  # 버튼이 눌렸을 때 LOW
                button_press_count += 1
                print(f"Button pressed {button_press_count} time(s)")
                time.sleep(0.2)  # 디바운싱 처리
                if button_press_count >= 3:
                    stop_alarm()
                    alarm_triggered = False
                    button_press_count = 0  # 버튼 카운터 초기화

            # 얼굴 박스 그리기
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # 파란색 박스

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    """알람 상태를 반환"""
    return {
        "alarm_triggered": alarm_triggered
    }

if __name__ == "__main__":
    try:
        app.run(host="10.21.37.250", port="8080")
    finally:
        GPIO.cleanup()

