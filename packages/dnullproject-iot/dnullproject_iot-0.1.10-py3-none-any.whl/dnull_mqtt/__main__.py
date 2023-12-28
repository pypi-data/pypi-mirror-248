from config import Config
from apps.binance import AppBinance
from apps.budget import AppBudget

# from apps.nutrition import AppNutrition
from apps.notion import AppNotion
import time
from base_log import log


if __name__ == "__main__":
    config = Config()

    log.info("DNULL MQTT started...")
    log.debug("debug enabled")
    pairs = ["BTCUSDT", "ETHUSDT"]
    app_binance = AppBinance(config)
    # app_budget = AppBudget(config)
    # app_nutrition = AppNutrition(config)
    app_notion = AppNotion(config)

    while True:
        app_binance.run(pairs)
        # app_budget.run()
        app_notion.run()

        time.sleep(config.mqtt_interval)
