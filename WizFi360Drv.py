import uasyncio as asyncio
import select, gc
from machine import UART
from time import sleep
from settings import *
from SSIDPASS import *

class WizFi360Drv:
    def __init__(self, uart=None):
        if uart is not None:
            self.uart = uart
            #self.init(uart)
        self.poll = select.poll()
        self.poll.register(uart, select.POLLIN)
        self.reset()
        self.version()
        print('[WizFi360Drv] Initialized')
        #self.connect(SSID, PASS)
        #self.update_firmware()
        self.host('WizFi360', '12345678')
        
    def connect(self, SSID, PASS):
        authStr = CONNECT+SSID+b','+PASS+EOL
        self.write(STATION_MODE)
        self.read(19)
        if self.readline() != ACK:
            raise OSError("[CONNECT] Can't set station mode.")
        self.write(DHCP_EN)
        self.read(21)
        if self.readline() != ACK:
            raise OSError("[CONNECT] Enabling DHCP failed.")
        self.write(authStr)
        self.read(31 + len(authStr))
        if self.readline() != ACK:
            raise OSError("[CONNECT] Estabilishing a connection failed.")
        else:
            print('[CONNECT] Connection estabilished.')
        
    def host(self, SSID, PASS, channel=5, encryption=3, maxCon=4, hidden=0):
        self.write(SOFT_AP_MODE)
        self.read(19)
        if self.readline() != ACK:
            raise OSError("[HOST] Entering soft AP mode failed.")
        else:
            print('[HOST] Soft AP mode OK.')
        self.write(DHCP_SOFT_EN)
        self.read(21)
        if self.readline() != ACK:
            raise OSError("[HOST] Enabling DHCP failed.")
        else:
            print('[HOST] DHCP OK.')
        startStr = START_SOFT_AP+('"'+SSID+'","'+PASS+'",{0},{1},{2},{3}'.format(channel, encryption, maxCon, hidden)).encode() + EOL
        self.write(startStr)
        ans = self.read(len(startStr)+2)
        if self.readline() != ACK:
            raise OSError("[HOST] Starting SoftAP failed.")
        else:
            print('[HOST] SoftAP OK.')
    
    def update_firmware(self):
        self.write(UPDATE)
        self.read(len(UPDATE))
        ans = None
        for i, res in enumerate(UPDATE_OK):
            ans = self.readline()
            if ans != res:
                raise OSError('[UPDATE] Update failed')
            if i < 4:
                print('[UPDATE] Update {0}'.format(i+1))
        print('[UPDATE] Finished')
            
    def clear_buffer(self):
        while uart.any():
            uart.read(1)
            
    def version(self):
        self.write(VERSION)
        self.read(8)
        a1 = self.readline()
        a2 = self.readline()
        a3 = self.readline()
        a4 = self.readline()
        a5 = self.readline()
        print((a1+a2+a3+a4+a5).decode())
        if a5 != ACK:
            raise OSError('[WizFi360Drv] Version check error')
            
    def reset(self):
        self.clear_buffer()
        self.write(RESET)
        self.read(len(RESET)+9)
        rec = self.readline()
        if rec != b'ready\r\n':
            raise OSError('[WizFi360Drv] Reset failed')
        else:
            print('[RESET] OK')
        self.clear_buffer()
        
    def write(self, msg):
        self.uart.write(msg)
        
    def readline(self):
        return self.uart.readline()
    
    def read(self, length):
        return self.uart.read(length)
        
    async def sender(self):
        swriter = asyncio.StreamWriter(self.uart, {})
        while True:
            swriter.write('AT\r\n')
            await swriter.drain()
            await asyncio.sleep(2)

    async def receiver(self):
        sreader = asyncio.StreamReader(self.uart)
        while True:
            res = await sreader.readline()
            print('Recieved', res)

    async def _init(self):
        asyncio.create_task(self.sender())
        asyncio.create_task(self.receiver())
        while True:
            await asyncio.sleep(1)

    def init(self, uart=None):
        try:
            if uart is not None:
                self.uart = uart
            asyncio.run(self._init())
        except KeyboardInterrupt:
            print('Interrupted')
        finally:
            asyncio.new_event_loop()
            print('as_demos.auart.test() to run again.')

gc.collect()

if __name__ == '__main__':
    uart = UART(1)
    drv = WizFi360Drv(uart)
