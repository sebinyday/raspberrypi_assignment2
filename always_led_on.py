from gpiozero import LED
from time import sleep

# GPIO 12번 핀에 연결된 LED 제어
led = LED(21)

try:
    led.on()  # 프로그램 실행 시 LED 켜기
    print("LED is ON. Press Ctrl+C to exit.")

    while True:
        sleep(1)  # 프로그램이 종료되지 않도록 대기

except KeyboardInterrupt:
    led.off()  # 프로그램 종료 시 LED 끄기
    print("LED is OFF. Program terminated.")
