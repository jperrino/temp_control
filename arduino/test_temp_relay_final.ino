// Include Wifi libraries
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>

// Network credentials
const char* ssid = "<insert_SSID>";
const char* password = "<insert_password>";

// Temp API server url
String serverName = "<insert_server_url>";

String deviceName = "test8";

// Connection config
unsigned long lastTime = 0;
unsigned long timerDelay = 5000;

// Include Sensor libraries
#include "DHTesp.h"
DHTesp dht;

// Assign relay pin
int relay = D7;

// Assign temperature sensor pin
int temp_sensor = D2;

// Initialize temperature variables
float t_total,temp = 0;
float T_FINAL = 0;
float T_MAX = 24;
float T_MIN = 20;
int count = 0;

// Define methods to handle API requests
StaticJsonDocument<192> parseResponseToJson(String input);
StaticJsonDocument<192> sendGetTemperature(float temp_measure, String device);
StaticJsonDocument<192> sendHTTPRequest(String path);
/////

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  dht.setup(temp_sensor, DHTesp::DHT22);

  pinMode(relay, OUTPUT);

  // Connect to local network
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
  delay(1000);
  Serial.println("Connecting..");
  }
  Serial.print("Connected to local network. IP: ");
  Serial.println(WiFi.localIP());

  sendGetRegisterDevice(deviceName);
}

void loop() {
  String eol = "////////////////////////";
  float t = dht.getTemperature();

  t_total = t_total + t;
  count++;

  if(count == 60){
  T_FINAL = t_total/count;

  String temp_string = "Temperature: ";
  String temp_string_w_value = temp_string + String(T_FINAL, 2);
  Serial.println(temp_string_w_value);

  // Start Print T_MAX and T_MIN temperature interval values
  String temp_max_string = "T_MAX: ";
  String temp_max_string_w_value = temp_max_string + String(T_MAX, 2);
  Serial.println(temp_max_string_w_value);

  String temp_min_string = "T_MIN: ";
  String temp_min_string_w_value = temp_min_string + String(T_MIN, 2);
  Serial.println(temp_min_string_w_value);
  // End Print T_MAX and T_MIN temperature interval values

  // Send temperature GET request
  StaticJsonDocument<192> temp_response = sendGetTemperature(T_FINAL, deviceName);

  float temp_range_max = temp_response["temp_range_max"];
  float temp_range_min = temp_response["temp_range_min"];

  if(temp_range_max != NULL && temp_range_max != T_MAX){
    T_MAX = temp_range_max;
    String temp_max_update_string = "Updating T_MAX with value: ";
    String temp_max_update_string_w_value = temp_max_update_string + String(temp_range_max, 2);
    Serial.println(temp_max_update_string_w_value);
  }

  if(temp_range_max != NULL && temp_range_min != T_MIN){
    T_MIN = temp_range_min;
    String temp_min_update_string = "Updating T_MIN with value: ";
    String temp_min_update_string_w_value = temp_min_update_string + String(temp_range_min, 2);
    Serial.println(temp_min_update_string_w_value);
  }

  //checkTempMax(T_FINAL);
  //checkTempMin(T_FINAL);

  if(T_FINAL >= T_MAX){
    String temp_max_string_w_value = "Temperature is above MAX: " + String(T_MAX, 2);
    Serial.println(temp_max_string_w_value +"\n"+eol);
    digitalWrite(relay, LOW);
    delay(20000);
  }
  else if(T_FINAL <= T_MIN){
    String temp_min_string_w_value = "Temperature is below MIN: " + String(T_MIN, 2);
    Serial.println(temp_min_string_w_value +"\n"+eol);
    digitalWrite(relay, HIGH);
    delay(20000);
  }
  else{
    Serial.println("Temperature is inside interval\n" + eol);
    delay(20000);
  }

  delay(20000);

  temp = 0;
  t_total = 0;
  T_FINAL = 0;
  count = 0;
  }
}

StaticJsonDocument<192> sendGetTemperature(float temp_measure , String device){
  StaticJsonDocument<192> jsonResponse;
  String path = "/measure/?temp=" + String(temp_measure, 2) + "&device=" + device;
  jsonResponse = sendHTTPRequest(path);
  return jsonResponse;
}

StaticJsonDocument<192> parseResponseToJson(String input){
  StaticJsonDocument<192> doc;
  DeserializationError error = deserializeJson(doc, input);

  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.f_str());
  }
  return doc;
}

StaticJsonDocument<192> sendHTTPRequest(String path){
  StaticJsonDocument<192> jsonResponse;

  if(WiFi.status()== WL_CONNECTED){
    WiFiClient client;
    HTTPClient http;
    String serverPath = serverName + path;
  
    // Your Domain name with URL path or IP address with path
    http.begin(client, serverPath.c_str());

    // If you need Node-RED/server authentication, insert user and password below
    //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
    
    // Send HTTP GET request
    int httpResponseCode = http.GET();
    String payload = "";
  
    if(httpResponseCode>0){
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      payload = http.getString();
      Serial.println(payload);
      jsonResponse = parseResponseToJson(payload);
    }
    else{
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Free resources
    http.end();
  }
  else{
    Serial.println("WiFi Disconnected");
  }
  return jsonResponse;
}

void sendGetRegisterDevice(String device){
  StaticJsonDocument<192> jsonResponse;
  String path = "/device/?name=" + device;
  jsonResponse = sendHTTPRequest(path);
}

void checkTempMax(float temp){
  String eol = "";
  // Verify if above max
  if(temp >= T_MAX){
    String temp_max_string_w_value = "Temperature is above MAX: " + String(T_MAX, 2);
    Serial.println(temp_max_string_w_value +"\n"+eol);
    digitalWrite(relay, LOW);
  }
  else{
  Serial.println("Temperature is below MAX\n" + eol);
  }
}

void checkTempMin(float temp){
  String eol = "////////////////////////";
    // Verify if below min
  if(temp <= T_MIN){
    String temp_min_string_w_value = "Temperature is below MIN: " + String(T_MIN, 2);
    Serial.println(temp_min_string_w_value +"\n"+eol);
    digitalWrite(relay, HIGH);
  }else{
    Serial.println("Temperature is above MIN\n" + eol);
  }
}

