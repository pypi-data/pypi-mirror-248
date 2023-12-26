#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : browser
# @Time         : 2023/11/29 15:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 持续刷新不掉线


from meutils.pipe import *
from playwright.async_api import Playwright, async_playwright

cli = typer.Typer(name="模拟浏览器")


# todo: 触发重试
async def kimi_playwright_run(
        url: str = "https://kimi.moonshot.cn/",
        headless: bool = False,
        storage_state: str = 'kimi_*.json',
        timeout: int = 1000
):
    storages = []

    for storage_state in Path(Path(storage_state).parent).glob(Path(storage_state).name):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=headless)
            context = await browser.new_context(storage_state=storage_state if Path(storage_state).exists() else None)

            page = await context.new_page()

            ####################################################################################

            await page.goto(url)
            await page.wait_for_load_state(state='load')
            await page.wait_for_load_state(state='networkidle')
            await page.wait_for_load_state(state='domcontentloaded')
            await page.wait_for_timeout(timeout=timeout)

            ####################################################################################
            # ---------------------
            # 保存状态文件
            storage = await context.storage_state(path=storage_state)  # 覆盖更新
            storages.append(storage)
            await context.close()
            await browser.close()
    return storages


async def deepseek_playwright_run(
        url: str = "https://chat.deepseek.com/sign_in",
        headless: bool = False,
        storage_state: str = 'kimi_*.json',
        timeout: int = 1000
):
    storages = []

    for storage_state in Path(Path(storage_state).parent).glob(Path(storage_state).name):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=headless)
            context = await browser.new_context(storage_state=storage_state if Path(storage_state).exists() else None)

            page = await context.new_page()

            ####################################################################################

            await page.goto(url)
            await page.get_by_placeholder("请输入手机号/邮箱地址").fill("313303303@qq.com")
            await page.get_by_placeholder("请输入手机号/邮箱地址").press("Tab")
            await page.get_by_placeholder("请输入密码").fill("8643188a")
            await page.get_by_role("img").nth(3).click()
            await page.get_by_role("button", name="登录").click()
            await page.wait_for_load_state(state='load')
            await page.wait_for_load_state(state='networkidle')
            await page.wait_for_load_state(state='domcontentloaded')
            await page.wait_for_timeout(timeout=timeout)

            # # 聊天
            # await page.get_by_placeholder("请输入问题。Enter 发送，Ctrl + Enter 换行").fill("你是谁")
            # await page.get_by_role("button", name="发送").click()

            ####################################################################################

            # ---------------------
            # 保存状态文件
            storage = await context.storage_state(path=storage_state)  # 覆盖更新
            storages.append(storage)
            await context.close()
            await browser.close()
    return storages


@cli.command()
def prun(
        url: str = "https://kimi.moonshot.cn/",
        headless: bool = True,
        storage_state: str = 'state.json',
):
    """
    mecli-browser --no-headless --url  https://kimi.moonshot.cn/
    """
    if 'kimi' in url:
        playwright_run = kimi_playwright_run
    elif 'deepseek' in url:
        playwright_run = deepseek_playwright_run

    storage = asyncio.run(playwright_run(url, headless, storage_state))
    logger.debug(storage)


if __name__ == '__main__':
    cli()
    # storage_state = '/Users/betterme/PycharmProjects/AI/MeUtils/meutils/clis/kimi_*.json'
    # print(Path(Path(storage_state).parent).glob(Path(storage_state).name) | xlist)
