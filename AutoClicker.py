from pynput.mouse import Listener
import pyautogui, threading, keyboard, time, os

threads = 15
hold = True # Wether or not you have to hold down the click button to autoclick
toggle_key = "f3"

class Main(Listener):
    def __init__(self):
        self.down = False
        self.toggle = True
        self.on = False
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
        pyautogui.click()

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

    def on_click(self, *args):
        if self.clicks: 
            if not args[-1]: 
                self.clicks -= 1
            return

        if hold:
            self.down = args[-1]
        elif args[-1]:
            self.down = not self.down

if __name__ == "__main__":
    Main()