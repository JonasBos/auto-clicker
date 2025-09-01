import FreeSimpleGUI as sg
import time
import threading

class App:
    def __init__(self, controller):
        self.controller = controller
        self.click_frequency = 45
        self.click_position = None
        self.window = None
        self.create_window()
        self.click_worker = None
        self.clicking = False

    def create_window(self):
        # Define the layout
        layout = [
            [sg.Radio('Left Click', 'CLICK_TYPE', default=True, key='-LEFT_CLICK-'), sg.Radio('BNM', 'CLICK_TYPE', key='-BNM-')],
            [sg.Text('Auto Clicker', font=('Helvetica', 16), justification='center')],
            [sg.Text('Clicks per second:'), sg.InputText(str(self.click_frequency), key='-FREQUENCY-')],
            [sg.Button('Start Clicking', size=(15, 2), key='-START-')],
            [sg.Text('Status: Ready', key='-STATUS-')],
            [sg.Button('Exit', size=(10, 1))]
        ]

        # Create the window
        self.window = sg.Window('Auto Clicker', layout, size=(250, 200),
                               finalize=True, resizable=False)

    def start_clicking(self):
        self.clicking = True
        self.click_frequency = float(self.window['-FREQUENCY-'].get())
        self.click_interval = 1 / self.click_frequency

        try:
            if self.click_interval <= 0:
                raise ValueError("Interval must be positive")
        except ValueError:
            sg.popup_error('Please enter a valid positive number for the interval!')
            return

        self.window['-START-'].update(disabled=True)
        self.window['-STATUS-'].update(f'Status: Clicking...')

        # Start clicking in a separate thread
        self.click_worker = threading.Thread(target=self._click_worker, daemon=True)
        self.click_worker.start()

    def _click_worker(self):

        self.window.write_event_value('-UPDATE_STATUS-', 'Status: Clicking...')

        click_function = self.controller.click_left if self.window['-LEFT_CLICK-'].get() else lambda: self.controller.click_keyboard(['B', 'N', 'M'])

        self.window.write_event_value('-UPDATE_STATUS-', 'Status: Left clicking...')
        while self.clicking:
            click_function()
            time.sleep(self.click_interval)

    def stop_clicking(self):
        self.clicking = False
        self.window['-START-'].update(disabled=False)
        self.window['-STATUS-'].update('Status: Stopped')

        # Wait for thread to finish (it will exit the loop now that clicking is False)
        if self.click_worker is not None and self.click_worker.is_alive():
            self.click_worker.join(timeout=2)  # Wait max 2 seconds
            self.click_worker = None

    def handle_right_click(self):
        self.window['-STATUS-'].update('Status: Right-click detected!')
        time.sleep(0.2)  # Debounce delay

        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def run(self):
        while True:
            event, values = self.window.read(timeout=100)  # Add timeout to check for right-click

            # Check for right-click when not actively clicking
            if self.controller.detectRightclick():
                self.handle_right_click()

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == '-START-':
                self.start_clicking()
            elif event == '-UPDATE_STATUS-':
                self.window['-STATUS-'].update(values[event])

        self.window.close()

