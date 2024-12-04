import RPi.GPIO as GPIO
import time

SWITCH_PIN = 23  # 스위치에 연결한 GPIO 핀 번호

GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 풀다운 설정

try:
    while True:
        if GPIO.input(SWITCH_PIN) == GPIO.HIGH:
            print("스위치 안 눌림")
        else:
            print("스위치 눌림")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("종료합니다.")
finally:
    GPIO.cleanup()
