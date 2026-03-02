#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Servo.h>
#include <math.h>

// ตั้งค่าหน้าจอ OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// กำหนดขา GPIO ใหม่เพื่อหลบ I2C
const int TRIG_PIN = D5;
const int ECHO_PIN = D6; 
const int SERVO_PIN = D3; 

Servo myServo;

// ฟังก์ชันแสดงผลบน OLED
void updateDisplay(String msg, float val1 = -1, String unit1 = "", float val2 = -1, String unit2 = "") {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  display.println(msg);
  display.println("---------------------");
  
  if (val1 != -1) {
    display.setTextSize(1);
    display.print("Dist: ");
    display.setTextSize(2);
    display.print(val1, 1);
    display.setTextSize(1);
    display.println(" " + unit1);
  }
  
  if (val2 != -1) {
    display.setCursor(0, 45);
    display.setTextSize(1);
    display.print("Speed: ");
    display.setTextSize(2);
    display.print(val2, 2);
    display.setTextSize(1);
    display.println(" " + unit2);
  }
  
  display.display();
}

float measure_distance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // timeout 30ms
  return (duration * 0.0343) / 2;
}

float MoveIn(float a, float b, float distance2) {
  float d = sin(64.0 * M_PI / 180.0) * distance2;
  float x = sqrt(pow(distance2, 2) - pow(d, 2));
  float z = a - x;
  return sqrt(pow(d, 2) + pow(z, 2));
}

float MoveOut(float a, float b, float c, float distance2) {
  float z = distance2 - c;
  float y = sin(26.0 * M_PI / 180.0) * z;
  float x = sqrt(pow(z, 2) - pow(y, 2));
  return sqrt(pow(y, 2) + pow(b + x, 2));
}

void setup() {
  Serial.begin(115200);
  
  // เริ่มต้นจอ OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C สำหรับจอส่วนใหญ่
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  display.clearDisplay();
  updateDisplay("System Ready...");

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  myServo.attach(SERVO_PIN);
  myServo.write(58);
}

void loop() {
  myServo.write(58);
  float distance = measure_distance();
  
  if (distance > 0 && distance <= 50) {
    updateDisplay("Target Detected!", distance, "cm");
    
    float a = distance;
    float b = tan(64.0 * M_PI / 180.0) * a;
    float c = sqrt(pow(a, 2) + pow(b, 2));
    
    unsigned long start_time = millis();
    myServo.write(122);
    delay(150);

    while (true) {
      float distance2 = measure_distance();
      
      if (distance2 > 0 && distance2 <= 100) {
        unsigned long end_time = millis();
        float t = (end_time - start_time) / 1000.0;
        
        float s;
        if (distance2 >= c - 5 && distance2 <= c + 5) s = distance2;
        else if (distance2 < c - 5) s = MoveIn(a, b, distance2);
        else s = MoveOut(a, b, c, distance2);

        s /= 100.0; // cm -> m
        float speed = s / t;

        // แสดงผลลัพธ์สุดท้ายบนจอ
        updateDisplay("Result:", s, "m", speed, "m/s");
        
        Serial.print("Speed: "); Serial.println(speed);
        delay(5000);
        break;
      }
      delay(10);
    }
  } else {
    updateDisplay("Scanning...", distance, "cm");
  }
  delay(100);
}