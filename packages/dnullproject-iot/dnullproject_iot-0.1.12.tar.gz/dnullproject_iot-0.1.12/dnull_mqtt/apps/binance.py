from dnull_mqtt.apps.app import App
from binance.spot import Spot
from dnull_mqtt.config import Config
from dnull_mqtt.base_log import log


class AppBinance(App):
    def __init__(self, Config: Config) -> None:
        self.name = "binance"
        super().__init__(self.name, Config)
        self.client = Spot()
        self.awtrix.icon(self.name)
        self.awtrix.settings["pushIcon"] = 1

    def get_price(self, pair: str):
        price = int(str(self.client.avg_price(pair)["price"]).split(".")[0])
        return f"{price:_}"

    def get_diff(self, pair: str):
        data = self.client.klines(pair, self.config.binance_candlestick_inverval)[-1]
        return round(float(data[1]) - float(data[4]), 2)

    def run(self, pairs: list):
        messages = list()
        for pair in pairs:
            self.get_diff(pair)
            price = self.get_price(pair)
            diff = self.get_diff(pair)
            if diff < 0:
                diff = f"--Red::({diff})--"
            elif diff == 0:
                diff = f"--White::({diff})--"
            else:
                diff = f"--Green::({diff})--"

            message = f"--White::{price}--{diff}"
            self.awtrix.icon(pair)
            messages.append(self.awtrix.message(message).copy())

            log.debug(f"binance: {pair} - {message}")
        log.debug(f"binance: {messages}")
        self.mqtt.publish(messages)
