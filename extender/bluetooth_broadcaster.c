#include "BLEDevice.h"

BLEServer *pServer = nullptr;
BLECharacteristic *pCharacteristic = nullptr;

void setup() {
  Serial.begin(115200);
  Serial.println("Setting up BLE...");

  BLEDevice::init("Quinn");

  // Create a BLE Server
  pServer = BLEDevice::createServer();

  // Create a BLE Service
  BLEService *pService = pServer->createService(BLEUUID((uint16_t)0x181C)); // Custom Service UUID

  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
                      BLEUUID((uint16_t)0x2A56), // Custom Characteristic UUID
                      BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
                    );

  //Message to be sent out                  
  pCharacteristic->setValue("Hello World!");

  pService->start();

  // Start broadcasting
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(pService->getUUID());
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x06);
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
}

void loop() {
  delay(5000);
}
