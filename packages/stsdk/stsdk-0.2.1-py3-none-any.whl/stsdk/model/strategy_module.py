import threading
from typing import Dict, List

from stsdk.common.key import (
    ORDER_STATUS_CANCELED,
    ORDER_STATUS_EXPIRED,
    ORDER_STATUS_FILLED,
    ORDER_STATUS_NEW,
    ORDER_STATUS_OMS_PLACE_ORDER_FAILED,
    ORDER_STATUS_PARTIALLY_FILLED,
    ORDER_STATUS_REJECTED,
)
from stsdk.common.signal_key import CANCEL_ORDER_SIGNAL, PLACE_ORDER_SIGNAL
from stsdk.model.order_manager import OrderManager
from stsdk.model.position_manager import PositionManager
from stsdk.model.strategy_base import StrategyBaseModule
from stsdk.utils.log import log


class StrategyModule(StrategyBaseModule):
    def __init__(self, strategy_id, account_id):
        super().__init__(strategy_id, account_id)
        self.orderManager = OrderManager(strategy_id, account_id)
        self.positionManager = PositionManager(strategy_id, account_id)
        self.init_order_thread()
        log.info("StrategyModule init")

    def init_order_thread(self):
        threading.Thread(target=self.consumer_with_signal).start()

    # 使用信号下单，本质上是通过blinker发送一个信号，然后通过信号处理函数来下单，这样无需等待接口返回，可以提高下单速度
    def place_order_signal(self, instrument_id, price, size, side, **kwargs):
        message = {
            "instrument_id": instrument_id,
            "price": price,
            "size": size,
            "side": side,
            **kwargs,
        }
        PLACE_ORDER_SIGNAL.send(message)

    # 使用信号撤单，本质上是通过blinker发送一个信号，然后通过信号处理函数来撤单，这样无需等待接口返回，可以提高撤单速度
    def cancel_order_signal(self, instrument_id, order_id):
        message = {
            "instrument_id": instrument_id,
            "order_id": order_id,
        }
        CANCEL_ORDER_SIGNAL.send(message)

    def place_order_handle(self, message):
        instrument_id, price, size, side = message.values()
        self.place_order(instrument_id, price, size, side)

    def cancel_order_handle(self, message):
        instrument_id, order_id = message.values()
        self.cancel_order(instrument_id, order_id)

    def consumer_with_signal(self):
        PLACE_ORDER_SIGNAL.connect(self.place_order_handle)
        CANCEL_ORDER_SIGNAL.connect(self.cancel_order_handle)

    # 下单基础函数，封装了对应下单接口的调用，以及下单后的持仓更新
    def place_order(self, instrument_id, price, size, side, **kwargs):
        resp = self.orderManager.place_order(instrument_id, price, size, side, **kwargs)
        log.info("place_order resp: %s" % resp)
        if "order_id" in resp:
            self.positionManager.update_position(
                resp["instrument_id"], self.positionManager.update_new_position(resp)
            )
        else:
            log.error("place_order error: %s" % resp)
        return resp

    # 批量下单基础函数，封装了对应下单接口的调用，以及下单后的持仓更新
    def place_batch_orders(self, orders: List[Dict]):
        resp = []
        for o in orders:
            resp.append(self.place_order(**o))
        return resp

    # 撤单基础函数，封装了对应撤单接口的调用，以及撤单后的持仓更新
    def cancel_order(self, instrument_id, order_id):
        return self.orderManager.cancel_order(instrument_id, order_id)

    # 批量撤单基础函数，封装了对应撤单接口的调用，以及撤单后的持仓更新
    def cancel_batch_orders(self, orders):
        resp = []
        for o in orders:
            resp.append(self.cancel_order(o.instrument_id, o.order_id))
        return resp

    def cancel_best_price_order(self, instrument_id, side):
        return self.orderManager.cancel_best_price_order(instrument_id, side)

    def cancel_worst_price_order(self, instrument_id, side):
        return self.orderManager.cancel_worst_price_order(instrument_id, side)

    def cancel_instrument_orders(self, instrument_id):
        return self.orderManager.cancel_instrument_orders(instrument_id)

    def cancel_all_orders(self):
        return self.orderManager.cancel_all_orders()

    # 获取持仓基础函数，封装了对应持仓接口的调用
    def get_position(self, instrument_id):
        return self.positionManager.get_position(instrument_id)

    # 获取目前还在挂的订单基础函数
    def get_open_orders(self, instrument_id):
        return self.orderManager.get_open_orders(instrument_id)

    # 获取目前还在挂所有的持仓基础函数
    def get_all_open_orders(self):
        return self.orderManager.get_all_open_orders()

    # 获取目前所有的持仓基础函数
    def get_all_positions(self):
        return self.positionManager.get_all_positions()

    # 通过订单id获取某个订单基础函数
    def get_order_by_id(self, instrument_id, order_id):
        return self.orderManager.get_order_by_id(instrument_id, order_id)

    def handle_order_update(self, message):
        if "body" in message:
            order_id = message["body"]["order_id"]
            order_status = message["body"]["order_status"]
            log.info(
                "receive order update: order_id: %s, order_status: %s"
                % (order_id, order_status)
            )
            if order_status in [ORDER_STATUS_NEW, ORDER_STATUS_PARTIALLY_FILLED]:
                self.orderManager.append_order(
                    message["body"]["instrument_id"], message["body"]
                )
            if order_status == ORDER_STATUS_FILLED:
                if self.orderManager.remove_order(
                    message["body"]["instrument_id"], message["body"]["order_id"]
                ):
                    self.positionManager.update_position(
                        message["body"]["instrument_id"],
                        self.positionManager.update_filled_position(message["body"]),
                    )
            if order_status in [
                ORDER_STATUS_CANCELED,
                ORDER_STATUS_REJECTED,
                ORDER_STATUS_EXPIRED,
                ORDER_STATUS_OMS_PLACE_ORDER_FAILED,
            ]:
                if self.orderManager.remove_order(
                    message["body"]["instrument_id"], message["body"]["order_id"]
                ):
                    self.positionManager.update_position(
                        message["body"]["instrument_id"],
                        self.positionManager.update_canceled_position(message["body"]),
                    )
        else:
            log.error("message: %s" % message)
