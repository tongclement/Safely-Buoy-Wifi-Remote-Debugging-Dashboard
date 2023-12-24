from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button
import datetime
import json

class Dashboard(GridLayout):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.cols = 2
        self.telemetry_data = {}
        self.fetch_telemetry_data()

    def estop(self, instance):
        # Action for the estop button
        UrlRequest('http://192.168.4.1/estop')

    def on(self, instance):
        # Action for the on button
        UrlRequest('http://192.168.4.1/on')

    def update_kpis(self, *args):
        # Update the UI elements with the latest KPI values
        self.ids.current_hdg.text = f"Current Heading: {self.telemetry_data.get('Current Hdg', 'N/A')}"
        self.ids.target_hdg.text = f"Target Heading: {self.telemetry_data.get('Target Hdg', 'N/A')}"
        self.ids.current_vel.text = f"Current Velocity: {self.telemetry_data.get('Current vel', 'N/A')} m/s"
        self.ids.target_vel.text = f"Target Velocity: {self.telemetry_data.get('Target vel', 'N/A')} m/s"
        self.ids.motor_power.text = f"Motor Power Setting: {self.telemetry_data.get('Current Motor Setting', 'N/A')}%"
        self.ids.rudder_deflection.text = f"Rudder Deflection: {self.telemetry_data.get('Rudder Config Var', 'N/A')}"
        self.ids.distance_to_home.text = f"Distance To Home: {self.telemetry_data.get('Distance To Home', 'N/A')} m"

    def fetch_telemetry_data(self):
        # Make a network request to fetch telemetry data
        UrlRequest('http://192.168.4.1', on_success=self.on_request_success, on_failure=self.on_request_fail, on_error=self.on_request_fail)

    def on_request_success(self, request, result):
        # Called when the network request succeeds
        try:
            #self.telemetry_data = json.loads(result)
            self.telemetry_data = result
            self.telemetry_data.update({"time": datetime.datetime.utcnow().isoformat()})
            self.update_kpis()
        except ValueError as e:
            print("Decoding JSON has failed", e)

    def on_request_fail(self, request, result):
        print("Network request failed", result)

    def start_fetching_data(self):
        # Start the clock to periodically fetch data
        Clock.schedule_interval(lambda dt: self.fetch_telemetry_data(), 1)  # Query every second

class DebugPortalApp(App):
    def build(self):
        dashboard = Dashboard()
        dashboard.start_fetching_data()
        return dashboard

if __name__ == '__main__':
    DebugPortalApp().run()