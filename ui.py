import FreeSimpleGUI as sg
import time
import threading

class App:
    def __init__(self, mouse_controller):
        self.mouse_controller = mouse_controller
        self.click_interval = 0.04
        self.click_position = None
        self.window = None
        self.create_window()

    def create_window(self):
        # Define the layout
        layout = [
            [sg.Text('Auto Clicker', font=('Helvetica', 16), justification='center')],
            [sg.Text('Click Interval (seconds):'), sg.InputText(str(self.click_interval), key='-INTERVAL-')],
            [sg.Button('Start Clicking', size=(15, 2), key='-START-')],
            [sg.Text('Status: Ready', key='-STATUS-')],
            [sg.Button('Exit', size=(10, 1))]
        ]

        # Create the window
        self.window = sg.Window('Auto Clicker', layout, size=(250, 150),
                               finalize=True, resizable=False)

    def start_clicking(self):

        try:
            if self.click_interval <= 0:
                raise ValueError("Interval must be positive")
        except ValueError:
            sg.popup_error('Please enter a valid positive number for the interval!')
            return

        self.window['-START-'].update(disabled=True)
        self.window['-STATUS-'].update('Status: Clicking will start in 5 seconds...')

        # Start clicking in a separate thread
        threading.Thread(target=self._click_worker, daemon=True).start()

    def _click_worker(self):
        time.sleep(5)  # Time to switch to the target window

        self.window.write_event_value('-UPDATE_STATUS-', 'Status: Clicking...')

        while True:
            self.mouse_controller.click()

            # Check for interrupt (right mouse button)
            if self.mouse_controller.detectInterrupt():
                self.window.write_event_value('-CLICKING_STOPPED-', 'Interrupted by right click')
                break

            time.sleep(self.click_interval)

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == '-START-':
                self.start_clicking()
            elif event == '-UPDATE_STATUS-':
                self.window['-STATUS-'].update(values[event])
            elif event == '-CLICKING_STOPPED-':
                self.window['-START-'].update(disabled=False)
                self.window['-STATUS-'].update(f'Status: {values[event]}')

        self.window.close()


