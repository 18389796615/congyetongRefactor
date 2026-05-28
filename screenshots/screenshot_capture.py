from playwright.sync_api import sync_playwright
import os

screenshots_dir = "/Users/zhenghui/Desktop/从业通重构/screenshots"
os.makedirs(screenshots_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    page.goto("http://localhost:8088", wait_until="networkidle")
    page.screenshot(path=f"{screenshots_dir}/enterprise-list.png", full_page=False)
    print("企业列表页面截图完成")

    page.click('text=用户管理')
    page.wait_for_timeout(500)
    page.screenshot(path=f"{screenshots_dir}/user-list.png", full_page=False)
    print("用户列表页面截图完成")

    page.click('text=配置管理')
    page.wait_for_timeout(500)
    page.screenshot(path=f"{screenshots_dir}/config-management.png", full_page=False)
    print("配置管理页面截图完成")

    page.click('text=流程配置')
    page.wait_for_timeout(500)
    page.screenshot(path=f"{screenshots_dir}/process-config.png", full_page=False)
    print("流程配置页面截图完成")

    browser.close()

print("所有截图完成！")