from typing import Optional

import ssl, pika

from bunny_m.settings import BunnySettings


class ConnectionProvider:
    def __init__(self, bunny_settings: Optional[BunnySettings] = None):
        self._bunny_settings = bunny_settings or BunnySettings()

    def get_connection(self, **kwargs) -> pika.BlockingConnection:
        credentials = pika.PlainCredentials(self._bunny_settings.RABBIT_USER,
                                       self._bunny_settings.RABBIT_PASSWD)
        ssl_options = None
        if self._bunny_settings.RABBIT_USE_SSL:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            ssl_options = pika.SSLOptions(context, 'localhost')
        params = pika.ConnectionParameters(host=self._bunny_settings.RABBIT_HOST,
                                      port=self._bunny_settings.RABBIT_PORT,
                                      virtual_host=self._bunny_settings.RABBIT_VIRTUAL_HOST,
                                      credentials=credentials,
                                      channel_max=self._bunny_settings.RABBIT_CHANNEL_MAX,
                                      heartbeat=self._bunny_settings.RABBIT_HEARTBEAT,
                                      blocked_connection_timeout=self._bunny_settings.RABBIT_BLOCKING_TIMEOUT,
                                      ssl_options=ssl_options,
                                      **kwargs)
        return pika.BlockingConnection(params)
