from pynput.mouse import Listener, Button, Controller
import pyautogui, threading, keyboard, time, os

threads = 8
hold = True # Wether or not you have to hold down the click button to autoclick
toggle_key = "f3"

class Main(Controller):
    def __init__(self):
        self.down = False
        self.toggle = True
        self.on = False
        self.mouse = super()
        self.clicks = 0
        self.count = 0
        for _ in range(threads):
            threading.Thread(target=self.spam).start()
        threading.Thread(target=self.title).start()
        threading.Thread(target=self.listen).start()

        with Listener(on_click=self.on_click) as listener:
            listener.join()

    def title(self):
        while True:
            old = int(self.count)
            time.sleep(0.1)
            speed = self.count-old
            os.system(f'TITLE {speed*10}/s clicks per second')

    def click(self):
        self.clicks += 1
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def spam(self):
        while True:
            if self.down and self.toggle:
                self.count += 1
                threading.Thread(target=self.click).start()

            time.sleep(0.01)

    def listen(self):
        key = {
            True: "on",
            False: "off"
        }

        while True:
            if keyboard.read_key() == toggle_key:
                self.toggle = not self.toggle
                print(f"Toggled {key[self.toggle]}")

            time.sleep(1)

    def on_click(self, x, y, button, pressed):
        if not button == Button.left:
            return
            
        if self.clicks: 
            if not pressed: 
                self.clicks -= 1
            return

        if hold:
            self.down = pressed
        elif pressed:
            self.down = not self.down

if __name__ == "__main__":
    Main()