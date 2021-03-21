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
        print('[WLAN] Connectiog...')
        authStr = CONNECT+'"{0}","{1}"'.format(SSID, PASS).encode()+EOL
        self.write(STATION_MODE)
        self.read(len(STATION_MODE)+2)
        if self.readline() != ACK:
            raise OSError("[WLAN] Can't set station mode.")
        self.write(DHCP_EN)
        self.read(len(DHCP_EN)+2)
        if self.readline() != ACK:
            raise OSError("[WLAN] Enabling DHCP failed.")
        self.write(authStr)
        while True:
            rec = self.readline()
            if rec == ACK:
                print('[WLAN] Connection estabilished.')
                return 'OK'
            elif rec == ERROR:
                print('[WLAN] Failed to connect.')
        
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
    
    def any(self):
        return self.uart.any()
        
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
        
    def socket_connect(self, addr, port, recQueue, sndQueue):
        self.senderQue = sndQueue
        connectStr = SOC_CLIENT+'"{0}",{1}'.format(addr, port).encode()+EOL
        self.write(connectStr)
        self.read(len(connectStr))
        if self.readline() != CONNECTED:
            self.clear_buffer()
            return 'ERROR'
        self.readline()
        self.client = True
        asyncio.create_task(self.reciver(recQueue))
        asyncio.create_task(self.sender(sndQueue))
        return 'OK'
        
    async def sender(self, queue):
        swriter = asyncio.StreamWriter(self.uart, {})
        if self.client:
            while True:
                msg = await queue.get()
                if msg == CLOSED:
                    print('[SOCKET] Connection lost.')
                    self.client = False
                    break
                swriter.write(msg)
                await swriter.drain()
        else:
            while True:
                swriter.write(await queue.get())
                await swriter.drain()

    async def reciver(self, queue):
        sreader = asyncio.StreamReader(self.uart)
        if self.client:
            while True:
                msg = await sreader.readline()
                print(msg)
                if msg == CLOSED:
                    await self.senderQue.put(CLOSED)
                    break
                await queue.put(msg)
        else:
            while True:
                await queue.put(await sreader.readline())

gc.collect()

if __name__ == '__main__':
    uart = UART(1)
    drv = WizFi360Drv(uart)
