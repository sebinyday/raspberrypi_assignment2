from gpiozero import PWMLED
from time import sleep

# GPIO 12번 핀에 연결된 LED를 PWM 방식으로 제어
led = PWMLED(21)

try:
    while True:
        # 점점 밝아짐
        for brightness in range(0, 101):  # 0%에서 100%까지
            led.value = brightness / 100  # 0.0 ~ 1.0으로 변환
            sleep(0.02)  # 밝기 변화 속도 조절

        # 점점 어두워짐
        for brightness in range(100, -1, -1):  # 100%에서 0%까지
            led.value = brightness / 100  # 1.0 ~ 0.0으로 변환
            sleep(0.02)  # 밝기 변화 속도 조절

except KeyboardInterrupt:
    # 종료 시 LED 끄기
    led.off()
    print("Program terminated.")
