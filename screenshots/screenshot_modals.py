from playwright.sync_api import sync_playwright
import os

screenshots_dir = "/Users/zhenghui/Desktop/从业通重构/screenshots"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    page.goto("http://localhost:8088", wait_until="networkidle")

    # 关闭所有弹窗
    page.evaluate("() => { document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('show')); }")
    page.wait_for_timeout(300)

    # 截取新增企业弹窗
    page.click('text=新增企业')
    page.wait_for_timeout(800)
    page.screenshot(path=f"{screenshots_dir}/enterprise-add-modal.png", full_page=False)
    print("新增企业弹窗截图完成")

    # 关闭弹窗
    page.evaluate("() => { document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('show')); }")
    page.wait_for_timeout(300)

    # 点击某个企业的入驻进度
    enterprise_rows = page.query_selector_all(".table-container tbody tr")
    if enterprise_rows:
        progress_cell = enterprise_rows[0].query_selector(".action-links")
        if progress_cell:
            progress_link = progress_cell.query_selector("a")
            if progress_link:
                progress_link.click()
                page.wait_for_timeout(800)
                page.screenshot(path=f"{screenshots_dir}/onboarding-progress-modal.png", full_page=False)
                print("入驻进度弹窗截图完成")

    browser.close()

print("弹窗截图完成！")