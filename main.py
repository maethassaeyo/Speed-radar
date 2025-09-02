from machine import Pin, PWM
import math
import utime
import time

# Define GPIO pins for Trig and Echo
TRIG_PIN = Pin(7, Pin.OUT)  # Example: GP2
ECHO_PIN = Pin(9, Pin.IN)   # Example: GP3

servo = PWM(Pin(20))
servo.freq(50)   # Servo ต้องการสัญญาณ PWM 50Hz

def servo_set(angle):
    # Servo ส่วนใหญ่รับ pulse 0.5 - 2.5 ms (0° - 180°)
    max_duty = 7864
    min_duty = 1802   # ประมาณ 2.5ms
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)


def measure_distance():
    # Send a 10us pulse to trigger the sensor
    TRIG_PIN.low()
    utime.sleep_us(2)
    TRIG_PIN.high()
    utime.sleep_us(10)
    TRIG_PIN.low()

    # Wait for the echo pulse to start
    while ECHO_PIN.value() == 0:
        pulse_start = utime.ticks_us()

    # Wait for the echo pulse to end
    while ECHO_PIN.value() == 1:
        pulse_end = utime.ticks_us()

    # Calculate pulse duration
    pulse_duration = utime.ticks_diff(pulse_end, pulse_start)

    # Calculate distance (speed of sound in cm/us is approx 0.0343)
    # Distance = (Time * Speed of Sound) / 2 (since sound travels to object and back)
    distance_cm = (pulse_duration * 0.0343) / 2
    return distance_cm

def MoveIn(a,b,distance2):
    d = math.sin(math.radians(64))*distance2
    x = math.sqrt((distance2**2)-(d**2))
    z = a-x
    s = math.sqrt((d**2)+(z**2))
    
    
    return s

def MoveOut(a,b,c,distance2):
    z = distance2-c
    y = math.sin(math.radians(26))*z
    x = math.sqrt((z**2)-(y**2))
    s = math.sqrt((y**2)+((b+x)**2))
    
    return s


while True:
    servo_set(58)
    distance = measure_distance()
    print(f"Distance: {distance:.1f} cm")
    if distance <= 50:
        a = distance
        b = math.tan(math.radians(64))*a
        c = math.sqrt((a**2)+(b**2))
        
        
        start = time.ticks_ms()
        
        servo_set(122)
        
        time.sleep(0.15)
        while True:
            distance2 = measure_distance()
            
            print(f"Distanc2: {distance2:.1f} cm")

            utime.sleep(0.01)

            if distance2 <= 100 :
                
                end = time.ticks_ms()
                t = (time.ticks_diff(end, start))/1000   
                if distance2 == c or (distance2 <= c+5 and distance2 >= c-5):
                    s = distance2
                elif distance2 < c-5:
                    s = MoveIn(a,b,distance2)
                elif distance2 > c+5:
                    s = MoveOut(a,b,c,distance2)
                s /= 100
                speed = s/t
                print("distance3 : ",s,"m")
                print("time :",t,"s")
                print("speed :",speed,"m/s")
                time.sleep(5)
                break
            

    utime.sleep(0.01) # Measure every 1 second
