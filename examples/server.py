import _thread as thread, uasyncio as asyncio
from uasyncio import Event, Lock
from socket import Socket, Queue
from machine import UART
from SSIDPASS import *



async def schedule(callback, time, *args, **kwargs):
    await asyncio.sleep_ms(time)
    callback(*args, **kwargs)
    
def print_response(msg):
    print(msg)

def core1(sndQueue, recQueue):
    uart = UART(1)
    wifi = Socket(uart)
    wifi.init(Socket.STA, (SSID, PASS))
    wifi.listen(3000)
    asyncio.create_task(reciver(uart, recQueue))
    asyncio.create_task(sender(uart, sndQueue))

async def foo(x, queue):
    while True:
        await asyncio.sleep(x)
        await queue.put('AT\r\n')
        
async def bar(queue):
    while True:
        msg = await queue.get()
        if msg is None:
            break
        asyncio.create_task(schedule(print_response, 0, msg))
        

        
async def sender(uart, queue):
    swriter = asyncio.StreamWriter(uart, {})
    while True:
        swriter.write(await queue.get())
        await swriter.drain()

async def reciver(uart, queue):
    sreader = asyncio.StreamReader(uart)
    while True:
        await queue.put(await sreader.readline())

    
async def main0():
    recQueue = Queue()
    sndQueue = Queue()
    asyncio.create_task(foo(15, sndQueue))
    asyncio.create_task(bar(recQueue))
    thread.start_new_thread(core1, (sndQueue, recQueue))
    await asyncio.sleep(60)
    
asyncio.run(main0())
