void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  pinMode(LED_BUILTIN, OUTPUT);
  
}

int serialData;
int data[] = {0, 0, 4, 3, 5, 6, 10, 15, 20, 12, 4, 1, 0, 0};
int size = sizeof(data)/sizeof(int);
void loop() {
 for(int i = 0; i < size; i++){
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println(data[i]);
  delay(100);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  
 }
}



