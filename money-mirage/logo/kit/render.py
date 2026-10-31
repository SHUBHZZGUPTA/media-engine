import asyncio, os
from playwright.async_api import async_playwright
H = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(H, 'out'); os.makedirs(O, exist_ok=True)
JOBS = [('pfp', 'MoneyMirage_profile_800.png', False), ('banner', 'MoneyMirage_banner_2560x1440.png', False), ('wm', 'MoneyMirage_watermark_150.png', True),
        ('emblem', 'MoneyMirage_emblem_for_dark_bg.png', True), ('emblem_l', 'MoneyMirage_emblem_for_light_bg.png', True), ('lock_dark', 'MoneyMirage_logo_for_dark_bg.png', True), ('lock_light', 'MoneyMirage_logo_for_light_bg.png', True),
        ('lock_h', 'MoneyMirage_logo_horizontal.png', True), ('sheet', 'MoneyMirage_brand_sheet.png', False)]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('HYPERFRAMES_BROWSER_PATH'), args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 2600, 'height': 2000}); await pg.goto('file://' + os.path.join(H, 'kit.html'))
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300); await pg.reload(); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(700)
        for sel, name, transp in JOBS: await pg.locator('#' + sel).screenshot(path=os.path.join(O, name), omit_background=transp)
        await b.close()
asyncio.run(main()); print('ok')
