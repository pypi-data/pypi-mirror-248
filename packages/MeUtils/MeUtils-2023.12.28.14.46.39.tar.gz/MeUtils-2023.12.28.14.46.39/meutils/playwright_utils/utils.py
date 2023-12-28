#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2023/12/27 17:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://mp.weixin.qq.com/s/OldGmXfoJZ9cObKU5f-q2Q

from meutils.pipe import *
from playwright.async_api import Playwright, async_playwright, expect, Request, Response


# 监听所有的请求和响应
async def open():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, args=["--start-maximized"])
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()
        page.on("response", filter_response)
        ''''''


async def filter_response(response):
    if 'souhu......' in response.url:
        response_data = await Response.body(response)
        if isinstance(response_data, bytes):
            response_data = response_data.decode()  # 请求返回数据


async def my_request(request):
    """https://blog.csdn.net/B11050729/article/details/131293769
    """
    print(await request.all_headers())


async def monitor_requests(request: Request):
    if request.method == "POST":
        # _ = await request.post_data()

        _ = request.post_data_json

        logger.debug(_)
        return _


async def monitor_responses(response: Response):
    if response:
        _ = await response.all_headers()
        logger.debug(_)
        return _
