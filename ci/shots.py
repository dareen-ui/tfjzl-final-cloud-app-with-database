# Takes the screenshots for the final project from the running app and the source files
import os
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from playwright.sync_api import sync_playwright

OUT = "screenshots"
BASE = "http://127.0.0.1:8000"
os.makedirs(OUT, exist_ok=True)


def code_html(path, start_marker=None):
    text = open(path).read()
    first_line = 1
    if start_marker:
        idx = text.index(start_marker)
        first_line = text[:idx].count("\n") + 1
        text = text[idx:]
    fmt = HtmlFormatter(linenos="table", linenostart=first_line, style="default", noclasses=True)
    body = highlight(text, get_lexer_for_filename(path), fmt)
    return (f"<html><body style='margin:0;font-family:monospace;background:#fff'>"
            f"<div style='background:#2d2d2d;color:#fff;padding:8px 14px;font:14px sans-serif'>{path}</div>"
            f"<div style='padding:8px 14px;font-size:14px'>{body}</div></body></html>")


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    files = [
        ("01-models", "onlinecourse/models.py", "# Question model"),
        ("02-admin-file", "onlinecourse/admin.py", None),
        ("04-course-details", "onlinecourse/templates/onlinecourse/course_detail_bootstrap.html", None),
        ("05-views", "onlinecourse/views.py", None),
        ("06-urls", "onlinecourse/urls.py", None),
    ]
    for name, path, marker in files:
        page.set_content(code_html(path, marker))
        page.screenshot(path=f"{OUT}/{name}.png", full_page=True)

    # 03: admin site
    page.goto(f"{BASE}/admin/login/")
    page.fill("#id_username", "admin")
    page.fill("#id_password", os.environ["ADMIN_PW"])
    page.click("input[type=submit]")
    page.wait_for_url(f"{BASE}/admin/")
    page.screenshot(path=f"{OUT}/03-admin-site.png", full_page=True)

    # 07: take the mock exam as a learner and capture the result
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    lp = ctx.new_page()
    lp.goto(f"{BASE}/onlinecourse/login/")
    lp.fill("#username", "dareen")
    lp.fill("#psw", os.environ["LEARNER_PW"])
    lp.click("form:has(#username) button[type=submit]")
    lp.wait_for_load_state("networkidle")
    lp.goto(f"{BASE}/onlinecourse/1/enroll/")
    lp.wait_for_load_state("networkidle")
    lp.click("text=Start Exam")
    lp.wait_for_selector("#questionform", state="visible")
    for label in ["Python", "CharField", "ForeignKey"]:
        lp.check(f"label:has-text('{label}') input")
    lp.click("input[type=submit][value=Submit]")
    lp.wait_for_load_state("networkidle")
    print("Result URL:", lp.url)
    print(lp.inner_text("body"))
    lp.screenshot(path=f"{OUT}/07-final.png", full_page=True)
    browser.close()
