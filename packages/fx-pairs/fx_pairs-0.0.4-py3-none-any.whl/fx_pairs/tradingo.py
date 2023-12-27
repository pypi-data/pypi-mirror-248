from trading_ig import IGService
from trading_ig.config import config

ig_service = IGService(
    config.username, config.password, config.api_key, config.acc_type
)
ig_service.create_session()

open_positions = ig_service.fetch_open_positions()
print("open_positions:\n%s" % open_positions)

print("")


epic = "KB.D.DRINKS.CASH.IP"  # 'CS.D.EURGBP.MINI.IP'
resolution = "1min"
num_points = 10
response = ig_service.fetch_historical_prices_by_epic_and_num_points(
    epic, resolution, num_points
)
df_ask = response["prices"]["bid"]
print("ask prices:\n%s" % df_ask)
