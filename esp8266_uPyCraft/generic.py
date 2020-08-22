from machine import Timer, idle
import network
import urequests as requests
import utime as time
from os import uname

class kpn:
  def __init__(self, configuration):
    self.ssid = configuration['ssid'] or '<SSID>'
    self.key = configuration['key'] or '<WIFIPASSWORD>'
    self.sensor_name = configuration['sensor_name'] or ''
    self.url = configuration['url'] or '<POST_URL>'
    self.authorization = configuration['authorization'] or ''

    self.check_network = Timer(-1)
    self.check_network.init(period=(7 * 1000), mode=Timer.PERIODIC, callback=lambda t:kpn.wifi_connect(self))
  
  def __repr__(self):
    print( 'ssid(%r)' % self.ssid)

  def wifi_init(self):
    self.wifi = network.WLAN(network.STA_IF)
    
    ap = network.WLAN(network.AP_IF)
    
    if ap.active():
      ap.active(False)
  
  def wifi_scan(self):
    if self.ssid:
      networks = self.wifi.scan()
      
      found = False
      for net in networks:
        net_ssid = str(net[0], 'utf')
        
        if net_ssid == self.ssid:
          found = True
      
      if not found:
        self.ssid = None
  
  def wifi_connect(self):
    if self.ssid:
      if not self.wifi.isconnected():
        print('connecting to network (', self.ssid, ')...')
    
        self.wifi.active(True)
        self.wifi.connect(self.ssid, self.key)
    else:
      self.check_network.deinit()

  def wifi_disconnect(self):
    if self.wifi.isconnected():
      print('disconnect from (', self.ssid, ')...')
    
      self.wifi.disconnect()
    
  def get_hostname(self):
    self.sensor_name = self.wifi.config("dhcp_hostname").lower()

  def post_data(self, measure_data):
    # Fill the dictionairy
    measure_data["SensorId"] = self.sensor_name
    measure_data["Uptime"] = (time.ticks_ms() // 1000)
    
    headers = {}
    headers['Authorization'] = self.authorization
    headers['Content-Type'] = 'application/json'
    headers['User-Agent'] = uname()[4]

    # Send measure data to demo platform
    try:
      response = requests.post(self.url, json=measure_data, headers=headers)
      
      result = { 'response_code': response.status_code, 'lastupdated': (time.ticks_ms() // 1000) }
      print(result)
      response.close()

      self.lastupdated = (time.ticks_ms() // 1000)
    except:
      result = { 'code': 'failure' }
    finally:
      return result
      

    
  
