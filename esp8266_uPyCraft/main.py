config = {}
config['ssid'] = '<SSID>'
config['key'] = '<WIFIPASSWORD>'
config['sensor_name'] = 'esp8266_home'
config['url'] = '<POST_URL>'
config['authorization'] = 'AUTH_TOKEN'
config['offset_temperature'] = -3

from generic import kpn
kpn = kpn(config)
kpn.wifi_init()
kpn.wifi_connect()
kpn.get_hostname()

import machine, onewire, ds18x20, time, ubinascii, webrepl
from umqttsimple import MQTTClient

client = None
broker = "192.168.2.21"
client_id = "esp8266_home"
topic = "home"
ds_pin = machine.Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

client = MQTTClient(client_id, broker)
client.connect
print("Connected to {}".format(broker))

roms = ds_sensor.scan()
post_data = {}
while True:
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  for rom in roms:
    #print(rom)
    data = ds_sensor.read_temp(rom)
    print(data)
    post_data['Temperature'] = ds_sensor.read_temp(rom)
    #client.publish('{}/{}'.format(topic,client_id),bytes(str(data), 'utf-8'))
    client.publish('home-assistant/home/esp8266_home','24')
    print('Sensor state: {}'.format(data))
    kpn.post_data(post_data)
  time.sleep(5)

# Main
timer1 = Timer(-1)
timer1.init(period=(10 * 1000), mode=Timer.PERIODIC, callback=lambda t:measure())


