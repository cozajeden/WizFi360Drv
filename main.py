import _thread as thread, uasyncio as asyncio
from uasyncio import Event, Lock
from WizFi360 import WLAN
from machine import UART
from queue import Queue
from SSIDPASS import *



async def schedule(callback, time, *args, **kwargs):
    await asyncio.sleep_ms(time)
    callback(*args, **kwargs)
    
def print_response(msg):
    print(msg.decode())

def core1(sndQueue, recQueue):
    uart = UART(1)
    wifi = WLAN(uart)
    wifi.init(WLAN.STA, (SSID, PASS))
    wifi.socket_connect('www.wp.pl', 443, recQueue, sndQueue)

async def foo(x, queue):
    while True:
        await asyncio.sleep(x)
        await queue.put('AT\r\n')
        
async def bar(queue):
    while True:
        msg = await queue.get()
        asyncio.create_task(schedule(print_response, 0, msg))
    
    
async def main0():
    recQueue = Queue()
    sndQueue = Queue()
    asyncio.create_task(foo(15, sndQueue))
    asyncio.create_task(bar(recQueue))
    thread.start_new_thread(core1, (sndQueue, recQueue))
    await asyncio.sleep(60)
    
asyncio.run(main0())
