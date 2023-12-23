import httpx

from stsdk.utils.log import log

timeout = 1


class Request:
    def get(self, url, headers=None, params=None):
        log.info("get info: ", url, params)
        resp = httpx.get(url, headers=headers, params=params, timeout=timeout)
        return resp.json()

    def post(self, url, data, headers=None):
        log.info("post info: ", url, data)
        resp = httpx.post(url, headers=headers, data=data, timeout=timeout)
        return resp.json()

    def patch(self, url, data, headers=None):
        log.info("patch info: ", url, data)
        resp = httpx.patch(url, headers=headers, data=data, timeout=timeout)
        return resp.json()

    def delete(self, url, data, headers=None):
        log.info("delete info: ", url, data)
        resp = httpx.delete(url, headers=headers, data=data, timeout=timeout)
        return resp.json()

    def close(self):
        self.session.close()


request = Request()
