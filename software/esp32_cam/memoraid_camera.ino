/*
 * MEMORAID - ESP32-CAM Camera Module
 *

 *
 * Hardware:
 * - AI Thinker ESP32-CAM
 * - OV2640 camera
 * - Wi-Fi
 *
 * Function:
 * - Initialize the OV2640 camera
 * - Connect to Wi-Fi
 * - Capture images
 * - Provide an HTTP endpoint for image capture
 * - Provide system status
 */

#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>

// ============================================================
// Wi-Fi Configuration
// ============================================================

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// ============================================================
// AI Thinker ESP32-CAM pin configuration
// ============================================================

#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5

#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// ============================================================
// Web server
// ============================================================

WebServer server(80);

// ============================================================
// Camera initialization
// ============================================================

bool initializeCamera() {

  camera_config_t config;

  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;

  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;

  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;

  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;

  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;

  config.xclk_freq_hz = 20000000;

  config.pixel_format = PIXFORMAT_JPEG;

  // Use PSRAM when available.
  if (psramFound()) {

    config.frame_size   = FRAMESIZE_VGA;
    config.jpeg_quality = 10;
    config.fb_count     = 2;

  } else {

    config.frame_size   = FRAMESIZE_QVGA;
    config.jpeg_quality = 12;
    config.fb_count     = 1;
  }

  config.grab_mode = CAMERA_GRAB_LATEST;
  config.fb_location = CAMERA_FB_IN_PSRAM;

  esp_err_t result = esp_camera_init(&config);

  if (result != ESP_OK) {

    Serial.print("Camera initialization failed. Error: 0x");
    Serial.println(result, HEX);

    return false;
  }

  // ----------------------------------------------------------
  // Camera sensor configuration
  // ----------------------------------------------------------

  sensor_t* sensor = esp_camera_sensor_get();

  if (sensor != nullptr) {

    sensor->set_brightness(sensor, 0);
    sensor->set_contrast(sensor, 0);
    sensor->set_saturation(sensor, 0);

    Serial.println("OV2640 camera sensor initialized.");
  }

  return true;
}

// ============================================================
// Root endpoint
// ============================================================

void handleRoot() {

  String html;

  html += "<!DOCTYPE html>";
  html += "<html>";
  html += "<head>";
  html += "<title>MEMORAID ESP32-CAM</title>";
  html += "</head>";

  html += "<body>";
  html += "<h1>MEMORAID Camera Module</h1>";

  html += "<p>ESP32-CAM is online.</p>";
  html += "<p>OV2640 camera initialized.</p>";

  html += "<p>";
  html += "<a href='/capture'>Capture Image</a>";
  html += "</p>";

  html += "<p>";
  html += "<a href='/status'>System Status</a>";
  html += "</p>";

  html += "</body>";
  html += "</html>";

  server.send(200, "text/html", html);
}

// ============================================================
// Image capture endpoint
// ============================================================

void handleCapture() {

  camera_fb_t* frame = esp_camera_fb_get();

  if (frame == nullptr) {

    Serial.println("Camera capture failed.");

    server.send(
      500,
      "text/plain",
      "Camera capture failed"
    );

    return;
  }

  Serial.print("Image captured. Size: ");
  Serial.print(frame->len);
  Serial.println(" bytes");

  server.sendHeader(
    "Content-Disposition",
    "inline; filename=memoraid_capture.jpg"
  );

  server.send_P(
    200,
    "image/jpeg",
    reinterpret_cast<const char*>(frame->buf),
    frame->len
  );

  esp_camera_fb_return(frame);
}

// ============================================================
// Status endpoint
// ============================================================

void handleStatus() {

  String response = "{";

  response += "\"system\":\"MEMORAID\",";
  response += "\"camera\":\"OV2640\",";
  response += "\"controller\":\"ESP32-CAM\",";
  response += "\"wifi\":";

  if (WiFi.status() == WL_CONNECTED) {
    response += "\"connected\",";
  } else {
    response += "\"disconnected\",";
  }

  response += "\"ip\":\"";
  response += WiFi.localIP().toString();
  response += "\"";

  response += "}";

  server.send(
    200,
    "application/json",
    response
  );
}

// ============================================================
// Wi-Fi connection
// ============================================================

void connectWiFi() {

  Serial.println();
  Serial.println("Connecting to Wi-Fi...");

  WiFi.begin(
    WIFI_SSID,
    WIFI_PASSWORD
  );

  int attempts = 0;

  while (
    WiFi.status() != WL_CONNECTED &&
    attempts < 30
  ) {

    delay(500);

    Serial.print(".");

    attempts++;
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {

    Serial.println("Wi-Fi connected.");

    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

  } else {

    Serial.println(
      "Wi-Fi connection failed."
    );
  }
}

// ============================================================
// Setup
// ============================================================

void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println();
  Serial.println("==============================");
  Serial.println("       MEMORAID SYSTEM");
  Serial.println("==============================");

  // ----------------------------------------------------------
  // Initialize camera
  // ----------------------------------------------------------

  Serial.println("Initializing OV2640...");

  if (!initializeCamera()) {

    Serial.println(
      "Camera initialization failed."
    );

    while (true) {
      delay(1000);
    }
  }

  Serial.println(
    "Camera initialization successful."
  );

  // ----------------------------------------------------------
  // Connect to Wi-Fi
  // ----------------------------------------------------------

  connectWiFi();

  // ----------------------------------------------------------
  // Configure HTTP endpoints
  // ----------------------------------------------------------

  server.on(
    "/",
    HTTP_GET,
    handleRoot
  );

  server.on(
    "/capture",
    HTTP_GET,
    handleCapture
  );

  server.on(
    "/status",
    HTTP_GET,
    handleStatus
  );

  server.begin();

  Serial.println(
    "MEMORAID camera server started."
  );

  Serial.println(
    "Available endpoints:"
  );

  Serial.println(
    "  /"
  );

  Serial.println(
    "  /capture"
  );

  Serial.println(
    "  /status"
  );
}

// ============================================================
// Main loop
// ============================================================

void loop() {

  server.handleClient();

  delay(2);
}
