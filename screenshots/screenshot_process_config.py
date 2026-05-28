from playwright.sync_api import sync_playwright
import os

screenshots_dir = "/Users/zhenghui/Desktop/从业通重构/screenshots"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    # 直接访问流程配置页面
    page.goto("http://localhost:8088", wait_until="networkidle")
    page.wait_for_timeout(500)

    # 点击配置管理主菜单
    page.click('.has-submenu:has-text("配置管理")')
    page.wait_for_timeout(300)

    # 点击流程配置子菜单
    page.click('.submenu-item:has-text("流程配置")')
    page.wait_for_timeout(800)
    page.screenshot(path=f"{screenshots_dir}/process-config.png", full_page=False)
    print("流程配置页面截图完成")

    # 点击新增流程按钮
    add_btn = page.query_selector('.page-header .btn-primary')
    if add_btn:
        add_btn.click()
        page.wait_for_timeout(800)
        page.screenshot(path=f"{screenshots_dir}/process-add-modal.png", full_page=False)
        print("新增流程弹窗截图完成")

    browser.close()

print("流程配置相关截图完成！")