from machine import Pin, PWM
import utime
import time

# สร้าง PWM object ที่ขา GP15
servo = PWM(Pin(20))
servo.freq(50)   # Servo ต้องการสัญญาณ PWM 50Hz

def set_angle(angle):
    # Servo ส่วนใหญ่รับ pulse 0.5 - 2.5 ms (0° - 180°)
    max_duty = 7864
    min_duty = 1802   # ประมาณ 2.5ms
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)

# ทดสอบหมุน
while True:
    set_angle(30)
    time.sleep(1)
    start = time.ticks_ms()
    set_angle(150)
    end = time.ticks_ms()
    
    elapsed = time.ticks_diff(end, start)   # คำนวณเวลาที่ผ่านไป
    print("ใช้เวลาไป:", elapsed, "ms")
    
    time.sleep(2)
    """for ang in range(0, 151, 1):  # หมุนทีละ 30 องศา
        set_angle(ang)
        print("Angle:", ang)
        utime.sleep_us(1)"""
    


