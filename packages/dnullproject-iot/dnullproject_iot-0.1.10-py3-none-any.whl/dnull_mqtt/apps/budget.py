from apps.app import App
from config import Config

class AppBudget(App):
    def __init__(self, Config: Config) -> None:
        self.name = "budget"
        super().__init__(self.name, Config)

    def run(self):
        self.mqtt.publish(self.awtrix.message(f"budget: TODO"))
