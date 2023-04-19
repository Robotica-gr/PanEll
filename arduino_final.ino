#include <Servo.h>
#include <FastLED.h>
#define S2 6
#define S3 7
#define OE 3
#define sensorOut 8
#define MAG1 2
#define SKOUPA 4
#define MAG2 5
#define KOUMPI1 10
#define KOUMPI2 12
#define SRV1 11
#define SRV2 9
//Το MAG3 είναι συνδεδεμένο συνεχώς στη γείωση

Servo SERVO1;
Servo SERVO2;

int pos1 = 20;
int pos2 = 20;
bool touch1 = false;
bool touch2 = false;
float startdown = millis();
int skoupaon = 0;
int mag1on = 0;
int mag2on = 0;
int command = 0;


int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;

CRGB leds0[48];
CRGB to_use;
int led_sort[48] = {0, 1, 2, 3, 4, 5,
                    6, 7, 8, 9, 10, 11,
                    12, 13, 14, 15, 45, 46,
                    47, 32, 33, 34, 35, 36,
                    37, 38, 39, 40, 41, 42,
                    43, 44, 18, 19, 20, 21,
                    22, 23, 24, 25, 26, 27,
                    28, 29, 30, 31, 16, 17
                   };
int led_colors[5][3] = {
  {1, 1, 1},
  {0, 0, 1},
  {1, 0, 0},
  {1, 1, 0},
  {0, 1, 0}
};
int poio_led;
int intense = 255;
int tp = 0;
int prevtp = 0;
int ledson = 0;

void setup() {
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(OE, OUTPUT);
  pinMode(MAG1, OUTPUT);
  pinMode(MAG2, OUTPUT);
  pinMode(SKOUPA, OUTPUT);

  digitalWrite(MAG1, LOW);
  digitalWrite(MAG2, LOW);
  digitalWrite(SKOUPA, LOW);
  digitalWrite(OE, LOW);

  pinMode(sensorOut, INPUT);
  pinMode(KOUMPI1, INPUT);
  pinMode(KOUMPI2, INPUT);

  SERVO1.attach(SRV1);
  SERVO2.attach(SRV2);
  SERVO1.write(20);
  SERVO2.write(20);
  delay(1000);
  SERVO1.detach();
  SERVO2.detach();

  FastLED.addLeds<WS2811, 13>(leds0, 48);

  Serial.begin(9600);
}

void loop() {
  //Εντολές:
  //1  Επιστρέφει RGB χωρισμένα με ';'
  //10 Led άσπρα
  //11 Led μπλε
  //12 Led πράσινα
  //13 Led κίτρινα
  //14 Led κόκκινα
  //21 Ενεργοποίηση σκούπας
  //22 Απενεργοποίηση σκούπας
  //23 Επιστρέφει αν η σκούπα είναι ενεργή (1 ή 0)
  //31 Κατεβαίνει το πάνω servo μέχρι τις 110 μοίρες
  //   ή μέχρι να πατηθεί το κουμπί
  //   ή μέχρι να περάσουν 5 δευτερόλεπτα
  //32 Κατεβαίνει το κάτω servo μέχρι τις 110 μοίρες
  //   ή μέχρι να πατηθεί το κουμπί
  //   ή μέχρι να περάσουν 5 δευτερόλεπτα
  //33 Κατεβαίνουν και τα δύο servo μέχρι τις 110 μοίρες
  //   ή μέχρι να πατηθεί το κουμπί
  //   ή μέχρι να περάσουν 5 δευτερόλεπτα
  //34 Ανεβαίνουν τα Servo στις 20 μοίρες
  //100-199 Πηγαίνει το πάνω servo σε μοίρες 20-119
  //200-299 Πηγαίνει το κάτω servo σε μοίρες 20-119
  //300-399 Πηγαίνουν και τα δύο servo servo σε μοίρες 20-119
  //Τα 3XΧΧ απαντάνε 1 όταν τελειώσει η κίνηση
  //41 Ενεργοποίηση του πάνω ηλεκτρομαγνήτη
  //42 Ενεργοποίηση του κάτω ηλεκτρομαγνήτη
  //43 Ενεργοποίηση και των δύο ηλεκτρομαγνητών
  //44 Απενεργοποίηση του πάνω ηλεκτρομαγνήτη
  //45 Απενεργοποίηση του κάτω ηλεκτρομαγνήτη
  //46 Απενεργοποίηση και των δύο ηλεκτρομαγνητών
  //47 Επιστρέφει αν ο πάνω μαγνήτης είναι ενεργός (1 ή 0)
  //48 Επιστρέφει αν ο κάτω μαγνήτης είναι ενεργός (1 ή 0)
  //51 Επιστρέφει 1 για πατημένο πάνω κουμπί και 0 για όχι πατημένο
  //52 Επιστρέφει 1 για πατημένο κάτω κουμπί και 0 για όχι πατημένο
  //55 Επιστρέφει 1 για πατημένα και τα δύο κουμπιά και 0 για όχι πατημένα
  if (Serial.available() > 0) {
    command = Serial.parseInt();
  } else {
    ledscreen();
  }
  if (command > 0) {
    if (command == 1) {
      digitalWrite(S2, LOW);
      digitalWrite(S3, LOW);
      delay(1);
      digitalWrite(OE, LOW);
      redFrequency = pulseIn(sensorOut, LOW);
      delay(1);
      digitalWrite(OE, HIGH);
      delay(1);
      digitalWrite(S2, HIGH);
      digitalWrite(S3, HIGH);
      delay(1);
      digitalWrite(OE, LOW);
      greenFrequency = pulseIn(sensorOut, LOW);
      delay(1);
      digitalWrite(OE, HIGH);
      delay(1);
      digitalWrite(S2, LOW);
      digitalWrite(S3, HIGH);
      delay(1);
      digitalWrite(OE, LOW);
      blueFrequency = pulseIn(sensorOut, LOW);
      delay(1);
      digitalWrite(OE, HIGH);
      delay(1);
      Serial.print(redFrequency);
      Serial.print(';');
      Serial.print(greenFrequency);
      Serial.print(';');
      Serial.println(blueFrequency);
    } else if (command > 9 && command < 15) {
      tp = command - 10;
    } else if (command == 21) {
      digitalWrite(SKOUPA, HIGH);
      skoupaon = 1;
    } else if (command == 22) {
      digitalWrite(SKOUPA, LOW);
      skoupaon = 0;
    } else if (command == 23) {
      Serial.println(skoupaon);
    } else if (command == 41) {
      digitalWrite(MAG1, HIGH);
      mag1on = 1;
    } else if (command == 44) {
      digitalWrite(MAG1, LOW);
      mag1on = 0;
    } else if (command == 42) {
      digitalWrite(MAG2, HIGH);
      mag2on = 1;
    } else if (command == 45) {
      digitalWrite(MAG2, LOW);
      mag2on = 0;
    } else if (command == 43) {
      digitalWrite(MAG1, HIGH);
      digitalWrite(MAG2, HIGH);
      mag1on = 1;
      mag2on = 1;
    } else if (command == 46) {
      digitalWrite(MAG1, LOW);
      digitalWrite(MAG2, LOW);
      mag1on = 0;
      mag2on = 0;
    } else if (command == 47) {
      Serial.println(mag1on);
    } else if (command == 48) {
      Serial.println(mag2on);
    } else if (command == 51) {
      Serial.println(digitalRead(KOUMPI1));
    } else if (command == 52) {
      Serial.println(digitalRead(KOUMPI2));
    } else if (command == 55) {
      Serial.println(int((digitalRead(KOUMPI1) + digitalRead(KOUMPI2)) / 2));
    } else if (command == 31) {
      SERVO1.attach(SRV1);
      touch1 = false;
      startdown = millis();
      while (touch1 == false && millis() - startdown < 5000) {
        pos1 = pos1 + 1;
        SERVO1.write(pos1);
        if (pos1 > 110 || digitalRead(KOUMPI1) == 1) {
          touch1 = true;
        }
        delay(50);
      }
      delay(10);
      SERVO1.detach();
      Serial.println(1);
    } else if (command == 32) {
      SERVO2.attach(SRV2);
      touch2 = false;
      startdown = millis();
      while (touch2 == false && millis() - startdown < 5000) {
        pos2 = pos2 + 1;
        SERVO2.write(pos2);
        if (pos2 > 110 || digitalRead(KOUMPI2) == 1) {
          touch2 = true;
        }
        delay(50);
      }
      delay(10);
      SERVO2.detach();
      Serial.println(1);
    } else if (command == 33) {
      SERVO1.attach(SRV1);
      SERVO2.attach(SRV2);
      touch1 = false;
      touch2 = false;
      startdown = millis();
      while ((touch1 == false || touch2 == false) && millis() - startdown < 5000) {
        if (touch1 == false) {
          pos1 = pos1 + 1;
          SERVO1.write(pos1);
        }
        if (pos1 > 110 || digitalRead(KOUMPI1) == 1) {
          touch1 = true;
        }
        if (touch2 == false) {
          pos2 = pos2 + 1;
          SERVO2.write(pos2);
        }
        if (pos2 > 110 || digitalRead(KOUMPI2) == 1) {
          touch2 = true;
        }
        delay(50);
      }
      delay(10);
      SERVO1.detach();
      SERVO2.detach();
      Serial.println(1);
    } else if (command == 34) {
      SERVO1.attach(SRV1);
      SERVO2.attach(SRV2);
      while (pos1 > 20 || pos2 > 20) {
        if (pos1 > 20) {
          pos1 = pos1 - 1;
          SERVO1.write(pos1);
        }
        if (pos2 > 20) {
          pos2 = pos2 - 1;
          SERVO2.write(pos2);
        }
        delay(25);
      }
      delay(10);
      SERVO1.detach();
      SERVO2.detach();
      Serial.println(1);
    } else if (command >= 100 && command <= 199) {
      SERVO1.attach(SRV1);
      int target = command - 80;
      int bima1 = -1;
      if (target > pos1) {
        bima1 = 1;
      }
      while (pos1 != target) {
        pos1 = pos1 + bima1;
        SERVO1.write(pos1);
        delay(25);
      }
      delay(10);
      SERVO1.detach();
      Serial.println(1);
    } else if (command >= 200 && command <= 299) {
      SERVO2.attach(SRV2);
      int target = command - 180;
      int bima2 = -1;
      if (target > pos2) {
        bima2 = 1;
      }
      while (pos2 != target) {
        pos2 = pos2 + bima2;
        SERVO2.write(pos2);
        delay(25);
      }
      delay(10);
      SERVO2.detach();
      Serial.println(1);
    } else if (command >= 300 && command <= 399) {
      SERVO1.attach(SRV1);
      SERVO2.attach(SRV2);
      int target = command - 280;
      int bima1 = -1;
      if (target > pos1) {
        bima1 = 1;
      }
      int bima2 = -1;
      if (target > pos2) {
        bima2 = 1;
      }
      while (pos1 != target || pos2 != target) {
        if (pos2 != target) {
          pos2 = pos2 + bima2;
          SERVO2.write(pos2);
        }
        if (pos1 != target) {
          pos1 = pos1 + bima1;
          SERVO1.write(pos1);
        }
        delay(25);
      }
      delay(10);
      SERVO1.detach();
      SERVO2.detach();
      Serial.println(1);
    } else {
      Serial.println(-1);
    }
    command = 0;
  }
}

void ledscreen() {
  if (tp == 0) {
    ledson = 0;
    poio_led = int(int(float(millis() / 60.0)) % 16);
    intense = 255;
    to_use = CRGB (led_colors[tp][0] * intense, led_colors[tp][1] * intense, led_colors[tp][2] * intense);
    leds0[led_sort[poio_led]] = to_use;
    leds0[led_sort[poio_led + 16]] = to_use;
    leds0[led_sort[poio_led + 32]] = to_use;
    for (int k = 1; k <= 15; k += 1) {
      intense = int(intense * 0.65);
      to_use = CRGB (led_colors[tp][0] * intense, led_colors[tp][1] * intense, led_colors[tp][2] * intense);
      if ((poio_led - k) < 0) {
        leds0[led_sort[poio_led - k + 16]] = to_use;
        leds0[led_sort[poio_led - k + 32]] = to_use;
        leds0[led_sort[poio_led - k + 48]] = to_use;
      } else {
        leds0[led_sort[poio_led - k]] = to_use;
        leds0[led_sort[poio_led - k + 16]] = to_use;
        leds0[led_sort[poio_led - k + 32]] = to_use;
      }
    }
    FastLED.show();
  } else {
    if (ledson == 0 || prevtp != tp) {
      ledson = 1;
      prevtp = tp;
      for (int k = 0; k <= 47; k += 1) {
        leds0[led_sort[k]] = CRGB (led_colors[tp][0] * 255, led_colors[tp][1] * 255, led_colors[tp][2] * 255);
      }
    FastLED.show();
    }
  }
}
