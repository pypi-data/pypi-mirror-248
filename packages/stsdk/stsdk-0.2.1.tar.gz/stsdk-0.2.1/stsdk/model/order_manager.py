from stsdk.api.http.oms import OMSApi
from stsdk.common.key import (
    CONTRACT_TYPE_LINEAR,
    ORDER_DIRECTION_BUY,
    ORDER_DIRECTION_SELL,
    ORDER_TYPE_LIMIT,
    POSITION_SIDE_NOTBOTH,
    TIME_IN_FORCE_GTC,
)


class OrderManager:
    def __init__(self, strategy_id, account_id):
        self.omsApi = OMSApi()
        self.openOrders = dict()
        self.strategy_id = strategy_id
        self.account_id = account_id

    def place_order(self, instrument_id, price, size, side):
        data = {
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
            "quantity": size,
            "price": price,
            "instrument_id": instrument_id,
            "position_side": POSITION_SIDE_NOTBOTH,
            "contract_type": CONTRACT_TYPE_LINEAR,
            "order_type": ORDER_TYPE_LIMIT,
            "order_direction": ORDER_DIRECTION_BUY
            if side == "buy"
            else ORDER_DIRECTION_SELL,
            "time_in_force": TIME_IN_FORCE_GTC,
        }
        resp = self.omsApi.place_order(data)
        self.append_order(instrument_id, resp)
        return resp

    def cancel_order(self, instrument_id, orderId):
        data = {
            "order_id": orderId,
        }
        resp = self.omsApi.cancel_order(data)
        self.remove_order(instrument_id, orderId)
        return resp

    def cancel_best_price_order(self, instrument_id, side):
        orders = {
            order_id: order_details["price"]
            for order_id, order_details in self.openOrders[instrument_id].items()
            if order_details["side"] == side
        }
        return self.cancel_order(instrument_id, max(orders, key=orders.get))

    def cancel_worst_price_order(self, instrument_id, side):
        orders = {
            order_id: order_details["price"]
            for order_id, order_details in self.openOrders[instrument_id].items()
            if order_details["side"] == side
        }
        return self.cancel_order(instrument_id, min(orders, key=orders.get))

    def cancel_instrument_orders(self, instrument_id):
        resp = []
        instrument_orders = self.openOrders[instrument_id]
        for order_id in instrument_orders:
            resp.append(self.cancel_order(instrument_id, order_id))
        return resp

    def cancel_all_orders(self):
        # await self.omsApi.cancel_all_orders()
        resp = []
        for instrument_id, orders in self.openOrders.items():
            for order_id in orders.keys():
                resp.append(self.cancel_order(instrument_id, order_id))
        return resp

    def append_order(self, instrument_id, data):
        if instrument_id not in self.openOrders:
            self.openOrders[instrument_id] = {}
        if "order_id" in data:
            self.openOrders[instrument_id][data["order_id"]] = data

    def remove_order(self, instrument_id, orderId):
        if (
            instrument_id in self.openOrders
            and orderId in self.openOrders[instrument_id]
        ):
            del self.openOrders[instrument_id][orderId]
            if len(self.openOrders[instrument_id]) == 0:
                del self.openOrders[instrument_id]
            return True

    def remove_instrument_id(self, instrument_id):
        if instrument_id in self.openOrders:
            del self.openOrders[instrument_id]

    def get_open_orders(self, instrument_id):
        return self.openOrders.get(instrument_id, {})

    def get_all_open_orders(self):
        return self.openOrders

    def get_order_by_id(self, instrument_id, orderId):
        return self.openOrders.get(instrument_id, {}).get(orderId, None)

    def get_all_outstanding_orders(self, instrument_id):
        """
        获取所有outstanding订单
        :param instrument_id:
        :return: order list
        """
        data = {
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
            "instrument_id": instrument_id,
        }
        return self.omsApi.get_all_outstanding_orders(data)

    def cancel_all_outstanding_orders(self):
        """
        取消所有outstanding订单
        :return: order list
        """
        data = {
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
        }
        orders = self.omsApi.cancel_all_outstanding_orders(data)
        del self.openOrders
        return orders

    def change_leverage(self, position_id, leverage):
        """
        更改仓位杠杆倍率
        :param position_id: 仓位id
        :param leverage: 杠杆倍率
        :return position_id: 仓位id
        :return leverage: 杠杆倍率
        """
        data = {"position_id": position_id, "leverage": leverage}
        return self.omsApi.change_leverage(data)
