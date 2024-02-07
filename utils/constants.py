WIFI_SSID="swaym-mobile-wifi"
WIFI_PASSWORD="Piaggio!2"

AWS_IOT_CLIENT_ID = "RaPi-Pico-2040-Client"
AWS_IOT_THING_NAME = "RaPi-Pico-2040"
AWS_IOT_CORE_HOST = b'ah9frbb7pxug4-ats.iot.eu-west-1.amazonaws.com'
AWS_IOT_CORE_PORT = 8883
AWS_IOT_DEVICE_KEY = "cert/private.key.der"
AWS_IOT_DEVICE_CERT = "cert/certificate.crt.der"
AWS_IOT_SHADOW_UPDATE_TOPIC = "$aws/things/" + AWS_IOT_THING_NAME + "/shadow/update"
AWS_IOT_SHADOW_DELTA_TOPIC = "$aws/things/" + AWS_IOT_THING_NAME + "/shadow/update/delta"

GAME_STATE_UPDATE_TOPIC = 'GAME_STATE_UPDATE'
CAR_CONTROL_UPDATE_TOPIC = 'CAR_CONTROL_UPDATE'
LAP_TIME_TOPIC = "RACE_LAP_TIME"
RACE_ANALYTICS_TOPIC = "RACE_ANALYTICS"