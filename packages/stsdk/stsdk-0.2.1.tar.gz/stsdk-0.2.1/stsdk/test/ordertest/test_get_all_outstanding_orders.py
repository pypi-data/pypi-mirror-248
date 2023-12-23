import pytest

from stsdk.test.ordertest.initialization import initialization
from stsdk.test.ordertest.logs import logger


# @pytest.fixture
def init_ST(strategy_id, account_id):
    st = initialization(strategy_id, account_id)
    # st = initialization("1", "aris_test")
    logger.info(st)
    return st


# 无订单情况
def test_get_all_outstanding_orders_return():
    st=init_ST("1", "aris_test")
    # instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    instrument_id="EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_SPOT.UNSPECIFIED.UNSPECIFIED.UNSPECIFIED"
    result = st.get_all_outstanding_orders(instrument_id)
    logger.info("正常执行: %s" % result)
    assert result=={}

# 验证accountid不正确
def test_get_all_outstanding_orders_accountid():
    st=init_ST("1", "aris_test111")
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    result = st.get_all_outstanding_orders(instrument_id)
    logger.info("accountid不正确: %s" % result)
    assert result=={}

# 验证strategy_id不正确
def test_get_all_outstanding_orders_strategy_id():
    st=init_ST("112", "aris_test")
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    result = st.get_all_outstanding_orders(instrument_id)
    logger.info("accountid不正确: %s" % result)
    assert result=={}

