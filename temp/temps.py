from  threading  import Thread,Lock
import time
from queue import Queue
from pynput.keyboard import Key, KeyCode, Listener
lock=Lock()

def on_press(key:Key|KeyCode|None)->None:
    if not key:
        return None
    # try:
    if isinstance(key,KeyCode):
        # print(f'Key {key.char} pressed')
        inputs=input()
        print(inputs)
    else:
        print(f'Key {key} pressed')

def on_release(key:Key|KeyCode|None)->None:
    print(f'Key {key} released')
    if key == Key.esc:  # If the 'esc' key is released, stop listening
        return None
# Collect events until released
def thread_1():
    lock.acquire()
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join() # listener.join is a blocking call that waits for the listener to stop listening
    # it stops listening when the listener returns False, which is done when the esc key is released
def thread_2():
    sd:list=["sat","jat","LMSDKFSDJLKFJ"] 
    while True:

        time.sleep(3)
        print(sd)
thread_list=[]
targets=[thread_1,thread_2]
for i in targets:
    x=Thread(target=i)
    thread_list.append(x) 
    x.start()

for ths in thread_list:
    ths.join()