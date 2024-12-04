import RPi.GPIO as GPIO
import time

BUZZER_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    print("스피커 테스트: ON")
    GPIO.output(BUZZER_PIN, GPIO.HIGH)  # 스피커 켜기
    time.sleep(2)
    print("스피커 테스트: OFF")
    GPIO.output(BUZZER_PIN, GPIO.LOW)  # 스피커 끄기
finally:
    GPIO.cleanup()
