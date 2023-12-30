# Scrapy Nimble Middleware

`scrapy-nimble` is a [Scrapy Downloader Middleware](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html) that helps to integrate
[Scrapy](https://scrapy.org) with [Nimble Web API](https://nimbleway.com/nimble-api/web/).

## Install

You can install `scrapy-nimble` as a regular Python package from
[PyPI](https://pypi.org/) using:

```shell
pip install scrapy-nimble
```

## Configuration

1. If you don't have it yet, [open an account](https://nimbleway.com/contact/) with [Nimble](https://nimbleway.com/).

1. Provide your credentials and enable the middleware through Scrapy settings.

   ```python
   # settings.py
   NIMBLE_ENABLED = True

   NIMBLE_USERNAME = "username"
   NIMBLE_PASSWORD = "password"
   ```

1. Add the downloader middleware to your `DOWNLOADER_MIDDLEWARES` Scrapy setting.

   ```python
   # settings.py
   DOWNLOADER_MIDDLEWARES = {
       "scrapy_nimble.middlewares.NimbleWebApiMiddleware": 570,
   }
   ```

   If you have `scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware` enabled
   (it is enabled by default in [DOWNLOADER_MIDDLEWARES_BASE](https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-DOWNLOADER_MIDDLEWARES_BASE)
   setting with default order equal to 590), configure `scrapy-nimble` middleware **before** it.

## Usage

Once the downloader middleware is properly configured, every request goes through the Nimble's Web API.
There is no need to change anything in your spider's code.
