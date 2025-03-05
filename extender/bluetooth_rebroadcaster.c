#include "BLEDevice.h"

BLEAdvertisedDevice* myDevice;
BLEClient*  pClient = nullptr;
BLECharacteristic* pCharacteristic = nullptr;

bool deviceConnected = false;
bool doConnect = false;
bool didDisconnect = false;

void setup() {
  Serial.begin(115200);

  // Initialize BLE
  BLEDevice::init("Device 2");

  // Start scanning for devices
  BLEScan* pScan = BLEDevice::getScan();
  pScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pScan->setActiveScan(true);
  pScan->start(15); //Scan for 15 seconds
}

void loop() {
  if (deviceConnected) {
    if (pCharacteristic != nullptr) {
      String receivedMessage = pCharacteristic->getValue().c_str();
      Serial.print("Received Message: ");
      Serial.println(receivedMessage);

      // Now re-broadcast the message with an additional one
      rebroadcastMessage(receivedMessage + " and this is the additional message!");
    }
  }

  delay(1000); // Just chill for a bit
}

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
        Serial.print("Advertised Device found: ");
        Serial.println(advertisedDevice.toString().c_str());

        // Look for the name 'Quinn' (from the first ESP32)
        if (advertisedDevice.haveName() && advertisedDevice.getName() == "Quinn") {
            myDevice = new BLEAdvertisedDevice(advertisedDevice);
            doConnect = true;
        }
    }
};

bool connectToServer() {
  if (myDevice == nullptr) {
    return false;
  }

  pClient = BLEDevice::createClient();
  Serial.println("Connecting to device...");

  // Connect to the BLE server
  pClient->connect(myDevice);

  Serial.println("Connected to server!");

  // Get the service and characteristic
  BLERemoteService* pRemoteService = pClient->getService(BLEUUID((uint16_t)0x181C));
  if (pRemoteService == nullptr) {
    Serial.println("Failed to find our service UUID.");
    return false;
  }

  pCharacteristic = pRemoteService->getCharacteristic(BLEUUID((uint16_t)0x2A56)); // The characteristic UUID
  if (pCharacteristic == nullptr) {
    Serial.println("Failed to find our characteristic.");
    return false;
  }

  return true;
}

void rebroadcastMessage(String message) {
  BLEServer *pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService(BLEUUID((uint16_t)0x181C)); // Custom Service UUID

  BLECharacteristic *pNewCharacteristic = pService->createCharacteristic(
                                                BLEUUID((uint16_t)0x2A56), // Custom Characteristic UUID
                                                BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
                                              );

  pNewCharacteristic->setValue(message.c_str());
  pService->start();

  // Start advertising the rebroadcasted message
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(pService->getUUID());
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x06);
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();

  Serial.print("Rebroadcasting message: ");
  Serial.println(message);
}
