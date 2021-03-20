import uasyncio as asyncio
import gc
from machine import UART
from time import sleep
from settings import *



class WizFi360Drv:
    def __init__(self, uart=None):
        print(uart)
        if uart is not None:
            self.uart = uart
        self.reset()
        self.version()
        print('[WizFi360Drv] Initialized')
        
    def connect(self, SSID, PASS):
        print('[WIFI] Connectiog...')
        authStr = CONNECT+'"{0}","{1}"'.format(SSID, PASS).encode()+EOL#CONNECT+SSID+b','+PASS+EOL
        self.write(STATION_MODE)
        self.read(19)
        if self.readline() != ACK:
            raise OSError("[WIFI] Can't set station mode.")
        self.write(DHCP_EN)
        self.read(21)
        if self.readline() != ACK:
            raise OSError("[WIFI] Enabling DHCP failed.")
        self.write(authStr)
        self.read(31 + len(authStr))
        if self.readline() != ACK:
            raise OSError("[WIFI] Estabilishing a connection failed.")
        else:
            print('[WIFI] Connection estabilished.')
        
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
        while self.uart.any():
            self.uart.read(1)
            
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
        
class WLAN(WizFi360Drv):
    AP = 0
    STA = 1
        
    def init(self, mode, auth, channel=5, encryption=3, maxCon=4, hidden=0):
        if mode == self.STA:
            self.connect(auth[0], auth[1])
        elif mode == self.AP:
            self.host(auth[0], auth[1], channel, encryption, maxCon, hidden)
        else:
            raise OSError('[WLAN] Unknown mode.')
        
    def socket_client
        
    async def sender(self, queue):
        swriter = asyncio.StreamWriter(self.uart, {})
        while True:
            swriter.write(await queue.get())
            await swriter.drain()

    async def reciver(self, queue):
        sreader = asyncio.StreamReader(self.uart)
        while True:
            await queue.put(await sreader.readline())

gc.collect()

if __name__ == '__main__':
    uart = UART(1)
    drv = WizFi360Drv(uart)
