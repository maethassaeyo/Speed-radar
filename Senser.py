from machine import Pin
import utime

# Define GPIO pins for Trig and Echo
TRIG_PIN = Pin(7, Pin.OUT)  # Example: GP2
ECHO_PIN = Pin(9, Pin.IN)   # Example: GP3

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

while True:
    distance = measure_distance()
    print(f"Distance: {distance:.1f} cm")
    if distance <= 20:
        break
    utime.sleep(0.01) # Measure every 1 second