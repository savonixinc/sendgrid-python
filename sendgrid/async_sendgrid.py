import sys

if sys.version_info < (3, 5):
    raise ImportError("Python 3.5 or later is required")

import aiohttp
import python_http_client

from .sendgrid import SendGridAPIClient


class AsyncSendGridAPIClient(SendGridAPIClient):
    """
    Asynchronous implementation of SendGridAPIClient

    Example of usage::

        import asyncio

        from sendgrid.async_sendgrid import AsyncSendGridAPIClient
        from sendgrid.helpers.mail import *

        async def send_message():
            async with AsyncSendGridAPIClient(api_key='SENDGRID_API_KEY') as client:
                 await client.send(mail)

        from_email = Email("test@example.com")
        from_email = Email("mail@k-vinogradov.ru")
        to_email = To("kostya.vinogradov@gmail.com")
        subject = "Sending with SendGrid is Fun 2"
        content = Content("text/plain", "and easy to do anywhere, even with Python")
        mail = Mail(from_email, to_email, subject, content)

        asyncio.run(send_message())
    """

    def __init__(self, *args, client_session=None, **kwargs):
        self._client_session = client_session or aiohttp.ClientSession()
        self.use_external_session = client_session is not None
        super().__init__(*args, **kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.use_external_session:
            await self.close_client_session()

    def get_client(self):
        return python_http_client.AsyncClient(
            host=self.host,
            client_session=self.client_session,
            request_headers=self._default_headers,
            version=3)

    @property
    def client_session(self):
        return self._client_session

    @client_session.setter
    def client_session(self, session):
        if not self.use_external_session:
            self.use_external_session = session != self._client_session
        self._client_session = session

    async def close_client_session(self):
        if not self.use_external_session:
            await self._client_session.close()

    async def send(self, message):
        return await super().send(message)
