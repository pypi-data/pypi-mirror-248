import json
import os

from stsdk.common.env import ENV_PRE, ENV_PROD, ENV_TEST
from stsdk.utils.consul import ConsulClient


class Config:
    env = ENV_TEST
    config = {}

    def __init__(self):
        self._load_config()
        address, token = self.consul_addr
        self.consul_client = ConsulClient(address, token)
        self._get_config_from_consul()

    # 内部方法，加载配置文件
    def _load_config(self):
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../config/config.json")
        )
        try:
            with open(config_path, "r") as file:
                data = json.load(file)
                self.consul = data.get("consul", {})
                self.log = data.get("log", {})
                self.metric = data.get("metric", {})
            env_config_path = self.get_config_env_path()
            with open(env_config_path, "r") as file:
                data = json.load(file)
                self.api_endpoint = data.get("api_endpoint", {})
        except Exception as e:
            raise Exception(f"init config Error: {e}")

    def _get_config_from_consul(self):
        if self.env == ENV_PROD:
            self.api_endpoint = self.consul_client.get_api_endpoint()

    def __str__(self):
        return (
            f"API Endpoint: {self.api_endpoint}\n"
            f"Environment: {self.env}\n"
            f"Log Path: {self.log}\n"
            f"Strategy Module: {self.strategy_module}\n"
        )

    # 执行策略前，需要初始化一些策略本身的配置
    def init_config(self, path):
        try:
            with open(path, mode="r", encoding="utf-8") as f:
                self.config = json.load(f)
        except Exception as e:
            raise Exception(f"Error loading config file: {e}")

    # 从配置中心获取配置,仅支持读取
    def get_config(self, key):
        value = self.config.get(key, "")
        return value

    # 不同的env会带来不同的配置，需要在执行策略前设置env
    def set_env(self, env):
        self.env = env

    def get_config_env_path(self):
        default_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../config/test.config.json")
        )
        if self.env == ENV_TEST:
            return default_path
        if self.env == ENV_PRE:
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../config/pre.config.json")
            )
        if self.env == ENV_PROD:
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../config/prod.config.json")
            )
        return default_path

    @property
    def DMS_BASE_HTTP_URL(self):
        return self.api_endpoint.get("http", {}).get("dms_base_url", "")

    @property
    def DMS_BASE_WS_URL(self):
        return self.api_endpoint.get("ws", {}).get("dms_base_ws", "")

    @property
    def OMS_BASE_HTTP_URL(self):
        return self.api_endpoint.get("http", {}).get("oms_base_url", "")

    @property
    def OMS_BASE_WS_URL(self):
        return self.api_endpoint.get("ws", {}).get("oms_base_ws", "")

    @property
    def ENV(self):
        return self.env

    @property
    def LOG_PATH(self):
        return self.log.get("path", "")

    @property
    def consul_test_addr(self):
        return self.consul.get("test_addr", "")

    @property
    def consul_pre_addr(self):
        return self.consul.get("pre_addr", "")

    @property
    def consul_prod_addr(self):
        return self.consul.get("prod_addr", "")

    @property
    def consul_prod_token(self):
        return self.consul.get("prod_token", "")

    @property
    def metirc_port(self):
        return self.metric.get("port", 8000)

    @property
    def consul_addr(self):
        if self.env == ENV_TEST:
            return self.consul_test_addr, ""
        elif self.env == ENV_PRE:
            return self.consul_pre_addr, ""
        elif self.env == ENV_PROD:
            return self.consul_prod_addr, self.consul_prod_token
        else:
            raise Exception("Error ENV")


config = Config()
