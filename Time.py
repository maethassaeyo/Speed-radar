import time

start = time.ticks_ms()   # เวลาเริ่มต้น (มิลลิวินาที)
time.sleep(2.5)           # รอ 2.5 วินาที
end = time.ticks_ms()     # เวลาสิ้นสุด

elapsed = time.ticks_diff(end, start)   # คำนวณเวลาที่ผ่านไป
print("ใช้เวลาไป:", elapsed, "ms")
