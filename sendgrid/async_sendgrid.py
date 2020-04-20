import sys

if sys.version_info < (3, 5):  # pragma: no cover
    raise ImportError("Python 3.5 or later is required")

from typing import Optional, Union
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

        from_email = Email("sender@example.com")
        to_email = To("recepient@example.com")
        subject = "Sending with SendGrid is Fun 2"
        content = Content("text/plain", "and easy to do anywhere, even with Python")
        mail = Mail(from_email, to_email, subject, content)

        asyncio.run(send_message())
    """

    def __init__(
            self,
            *args,
            client_session: Optional[aiohttp.ClientSession] = None,
            **kwargs):
        """Create AsyncSendGridAPIClient instance

        All arguments beside client_session are passed
        to SendGridAPIClient instance
        
        :param Optional[aiohttp.ClientSession] client_session: ClientSession
            instance, defaults to None
        """

        self._client_session = None
        super().__init__(*args, **kwargs)
        self.internal_client_session_used = False
        if client_session:
            self.set_client_session(client_session)

    async def __aenter__(self):
        if not self.get_client_session():
            self.set_client_session(aiohttp.ClientSession(), True)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.internal_client_session_used:
            await self.get_client_session().close()

    def get_client_session(self) -> Union[aiohttp.ClientSession, None]:
        """Get applied aiohttp.ClientSession instance
        
        :return: Returns the instance of aiohttp.ClientSession
                 that has been applied
        :rtype: Union[aiohttp.ClientSession, None]
        """
        return self._client_session

    def set_client_session(self, session: aiohttp.ClientSession, internal: bool = False):
        """Apply aiohttp.ClientSession instance
        
        :param aiohttp.ClientSession session: aiohttp.ClientSession instance
        :param bool internal: treat session as internal (don't close it on
                              context manager exit),defaults to False
        """
        self.client.set_client_session(session)
        self._client_session = session
        self.internal_client_session_used = internal

    def get_client(self) -> python_http_client.AsyncClient:
        return python_http_client.AsyncClient(
            host=self.host,
            client_session=self.get_client_session(),
            request_headers=self._default_headers,
            version=3)

    async def send(self, message):
        return await super().send(message)
