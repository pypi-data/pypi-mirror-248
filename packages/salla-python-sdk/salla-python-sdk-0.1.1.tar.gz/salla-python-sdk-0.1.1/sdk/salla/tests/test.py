from salla import Salla


import asyncio

from salla import ENV, Refresh_Token_Payload, Salla, Webhook_Events, WebhookPayload


s = Salla(ENV.ACCESS_TOKEN)


async def test_merchant_info():
    await s.get_merchant_info()


async def test_store_info():
    await s.get_store_info()


async def test_subscribe_webhook():
    await s.webhook_subscribe(
        WebhookPayload(
            name="Ryuk-me",
            event=Webhook_Events.PRODUCT_UPDATED,
            secret=ENV.WEBHOOK_SECRET,
            url="https://webhook.site/2453453-123n7bad6va123",
            security_strategy="token",
        )
    )

    # Refresh the access token and print the result
    # await s.get_access_token_from_refresh_token(
    #     Refresh_Token_Payload(
    #         client_id=ENV.CLIENT_ID,
    #         client_secret=ENV.CLIENT_SECRET,
    #         refresh_token=ENV.REFRESH_TOKEN,
    #     )
    # )


async def test_active_webhooks():
    await s.get_active_webhooks()


async def test_available_webhooks():
    await s.get_available_webhook_events()


async def test_usubscribewebhooks():
    await s.unsubscribe_webhook(url="https://webhook.site/2453453-123n7bad6va123")
