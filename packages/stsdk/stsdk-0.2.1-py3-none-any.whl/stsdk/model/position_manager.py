from stsdk.api.http.oms import OMSApi
from stsdk.common.key import ORDER_DIRECTION_BUY_STR


class PositionModule(object):
    def __init__(
        self,
        long_opening=0.0,
        long_filled=0.0,
        long_outstanding=0.0,
        short_opening=0.0,
        short_filled=0.0,
        short_outstanding=0.0,
    ):
        self.long_opening = long_opening
        self.long_filled = long_filled
        self.long_outstanding = long_outstanding
        self.short_opening = short_opening
        self.short_filled = short_filled
        self.short_outstanding = short_outstanding

    def __str__(self):
        return (
            f"long_opening: {self.long_opening}, long_filled: {self.long_filled}, "
            f"long_outstanding: {self.long_outstanding}, "
            f"short_opening: {self.short_opening}, short_filled: {self.short_filled}, "
            f"short_outstanding: {self.short_outstanding}"
        )

    @property
    def net_position(self):
        return self.long_filled - self.short_filled

    @property
    def net_outstanding_qty(self):
        return self.long_outstanding - self.short_outstanding

    def clear(self):
        self.long_opening = 0.0
        self.long_filled = 0.0
        self.long_outstanding = 0.0
        self.short_opening = 0.0
        self.short_filled = 0.0
        self.short_outstanding = 0.0

    def record_position(self, position_info):
        """
        position management in PositionModule
        :param position_info, a dictionary with keys as position_record_header
        :return:
        """
        pass


class PositionManager(object):
    def __init__(self, strategy_id, account_id):
        self.positions = dict()
        self.omsApi = OMSApi()
        self.strategy_id = strategy_id
        self.account_id = account_id

    def update_new_position(self, data):
        if "order_direction" in data:
            origin_quantity = float(data["origin_quantity"])
            if data["order_direction"] == ORDER_DIRECTION_BUY_STR:
                return PositionModule(long_opening=origin_quantity)
            else:
                return PositionModule(short_opening=origin_quantity)

    def update_canceled_position(self, data):
        if "order_direction" in data:
            origin_quantity = float(data["origin_quantity"])
            filled_quantity = float(data["filled_quantity"])
            if data["order_direction"] == ORDER_DIRECTION_BUY_STR:
                return PositionModule(
                    long_opening=-(origin_quantity - filled_quantity),
                    long_filled=filled_quantity,
                )
            else:
                return PositionModule(
                    short_opening=-(origin_quantity - filled_quantity),
                    short_filled=filled_quantity,
                )

    def update_filled_position(self, data):
        if "order_direction" in data:
            filled_quantity = float(data["filled_quantity"])
            if data["order_direction"] == ORDER_DIRECTION_BUY_STR:
                return PositionModule(
                    long_opening=-filled_quantity,
                    long_filled=filled_quantity,
                )
            else:
                return PositionModule(
                    short_opening=-filled_quantity,
                    short_filled=filled_quantity,
                )

    def update_position(self, instrument_id, position):
        if instrument_id not in self.positions:
            self.positions[instrument_id] = PositionModule()
        self.positions[instrument_id].long_opening += position.long_opening
        self.positions[instrument_id].long_filled += position.long_filled
        self.positions[instrument_id].long_outstanding += position.long_outstanding
        self.positions[instrument_id].short_opening += position.short_opening
        self.positions[instrument_id].short_filled += position.short_filled
        self.positions[instrument_id].short_outstanding += position.short_outstanding

    def clear_position(self, instrument_id):
        self.positions[instrument_id].clear()

    def get_position(self, instrument_id):
        return self.positions.get(instrument_id, PositionModule())

    def get_all_positions(self):
        return self.positions

    def close_all_positions(self):
        """
        一键平仓
        :return: order list
        """
        data = {
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
        }
        orders = self.omsApi.close_all_positions(data)
        del self.positions
        return orders
