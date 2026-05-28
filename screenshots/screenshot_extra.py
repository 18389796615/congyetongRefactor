from playwright.sync_api import sync_playwright
import os

screenshots_dir = "/Users/zhenghui/Desktop/从业通重构/screenshots"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    page.goto("http://localhost:8088", wait_until="networkidle")
    page.wait_for_timeout(500)

    # 进入流程配置页面
    page.click('.has-submenu:has-text("配置管理")')
    page.wait_for_timeout(300)
    page.click('.submenu-item:has-text("流程配置")')
    page.wait_for_timeout(800)

    # 触发新增流程弹窗
    page.evaluate("() => { showProcessModal(); }")
    page.wait_for_timeout(800)
    page.screenshot(path=f"{screenshots_dir}/process-add-modal.png", full_page=False)
    print("新增流程弹窗截图完成")

    browser.close()

print("额外截图完成！")