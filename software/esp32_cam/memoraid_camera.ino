/*
 * MEMORAID - AI Smart Glasses
 * ESP32-CAM Camera Module
 *
 * Reference implementation for the MEMORAID prototype architecture.
 * Captures JPEG frames and exposes them through a simple HTTP endpoint
 * for the external recognition application.
 */

#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>

// ============================================================
// Wi-Fi Configuration
// ============================================================

const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// ============================================================
// AI Thinker ESP32-CAM Pin Configuration
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
// Web Server
// ============================================================

WebServer server(80);

// ============================================================
// Camera Initialization
// ============================================================

bool initializeCamera() {

    camera_config_t config;

    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer   = LEDC_TIMER_0;

    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;

    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;

    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;

    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;

    config.xclk_freq_hz = 20000000;

    config.pixel_format = PIXFORMAT_JPEG;

    // Use PSRAM when available.
    if (psramFound()) {

        config.frame_size = FRAMESIZE_VGA;
        config.jpeg_quality = 10;
        config.fb_count = 2;

    } else {

        config.frame_size = FRAMESIZE_QVGA;
        config.jpeg_quality = 12;
        config.fb_count = 1;
    }

    esp_err_t result = esp_camera_init(&config);

    if (result != ESP_OK) {

        Serial.printf(
            "Camera initialization failed: 0x%x\n",
            result
        );

        return false;
    }

    // Basic image sensor configuration.
    sensor_t* sensor = esp_camera_sensor_get();

    if (sensor != nullptr) {

        sensor->set_brightness(sensor, 0);
        sensor->set_contrast(sensor, 0);
        sensor->set_saturation(sensor, 0);
    }

    return true;
}

// ============================================================
// Capture Endpoint
//
// GET /capture
//
// Returns a single JPEG image.
// ============================================================

void handleCapture() {

    camera_fb_t* frame = esp_camera_fb_get();

    if (frame == nullptr) {

        server.send(
            500,
            "text/plain",
            "Camera capture failed"
        );

        return;
    }

    server.sendHeader(
        "Content-Disposition",
        "inline; filename=memoraid.jpg"
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
// Status Endpoint
//
// GET /status
// ============================================================

void handleStatus() {

    String response = "{";
    response += "\"device\":\"MEMORAID\",";
    response += "\"module\":\"ESP32-CAM\",";
    response += "\"camera\":\"online\"";
    response += "}";

    server.send(
        200,
        "application/json",
        response
    );
}

// ============================================================
// Root Endpoint
// ============================================================

void handleRoot() {

    String message;

    message += "MEMORAID Smart Glasses\n";
    message += "ESP32-CAM module online\n\n";
    message += "Available endpoints:\n";
    message += "/capture\n";
    message += "/status\n";

    server.send(
        200,
        "text/plain",
        message
    );
}

// ============================================================
// Setup
// ============================================================

void setup() {

    Serial.begin(115200);

    delay(1000);

    Serial.println();
    Serial.println("=================================");
    Serial.println(" MEMORAID AI SMART GLASSES");
    Serial.println(" ESP32-CAM MODULE");
    Serial.println("=================================");

    // Initialize camera.
    if (!initializeCamera()) {

        Serial.println(
            "ERROR: Camera initialization failed."
        );

        while (true) {
            delay(1000);
        }
    }

    Serial.println(
        "Camera initialized successfully."
    );

    // Connect to Wi-Fi.
    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    Serial.print(
        "Connecting to Wi-Fi"
    );

    while (WiFi.status() != WL_CONNECTED) {

        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.println(
        "Wi-Fi connected."
    );

    Serial.print(
        "MEMORAID camera IP: "
    );

    Serial.println(
        WiFi.localIP()
    );

    // Configure HTTP endpoints.
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
        "Ready to capture images."
    );
}

// ============================================================
// Main Loop
// ============================================================

void loop() {

    server.handleClient();
}
