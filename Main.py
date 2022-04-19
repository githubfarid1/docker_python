import asyncio
# from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
#from playwright_stealth import stealth_async
import time
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import random

async def main():
    url = "https://www.villasofdistinction.com/villas?location id=&destination id=28&sub location id=&region id=&villa id=&geo type=&cdds=clicked&location=France&dates=&guests=1"
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless = False)
    # context = await browser.new_context()
    page = await browser.new_page()
    await page.goto(url, timeout = 0)
    await page.click("#emailSubscribeModal > div > div > div.modal-header > button")

    handle = await page.query_selector('input#max_page[type=hidden]')
    maxpage = await handle.get_attribute("value")
    intmaxpage = int(maxpage)
    intcurpage = 0
    while intcurpage < intmaxpage:
        handle = await page.query_selector('input#page[type=hidden]')
        curpage = await handle.get_attribute("value")
        intcurpage = int(curpage)
        await page.evaluate(
            """
            var intervalID = setInterval(function () {
                var scrollingElement = (document.scrollingElement || document.body);
                scrollingElement.scrollTop = scrollingElement.scrollHeight;
            }, 200);

            """
        )
        
        prev_height = None
        while True:
            curr_height = await page.evaluate('(window.innerHeight + window.scrollY)')
            if not prev_height:
                prev_height = curr_height
                await page.wait_for_timeout(random.randint(3, 5) * 1000)
            elif prev_height == curr_height:
                await page.evaluate('clearInterval(intervalID)')
                break
            else:
                prev_height = curr_height
                await page.wait_for_timeout(random.randint(3, 5) * 1000)    



    html = await page.inner_html('#view-grid-serp')
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('div', class_='card-title_wrap')
    await browser.close()

    urls = []
    for res in results:
        href = res.find('a')['href']
        urls.append("https://www.villasofdistinction.com/{}".format(href))
    # print(urls)

    for u in urls:
        browser = await playwright.chromium.launch(headless = True)
        # context = await browser.new_context()
        page = await browser.new_page()
        await page.goto(u, timeout = 0)
        await page.is_visible('#content')
        html = await page.inner_html('#content')
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find('div', {'id':'title'}).find('h1')
        print(title.text)
        # await page.wait_for_timeout(random.randint(3, 5) * 1000)
        await browser.close()
    
if __name__ == '__main__':
    asyncio.run(main())
