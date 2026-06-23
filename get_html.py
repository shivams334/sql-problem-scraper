from playwright.sync_api import sync_playwright

EMAIL = "shivams334@gmail.com"
PASSWORD = "Microsoft@1234"

def scrape_problem(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Log in
        page.goto("https://www.namastesql.com/login")
        page.wait_for_selector('input[name="email"]', timeout=15000)
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_url(lambda u: "login" not in u, timeout=30000)

        # Navigate to problem
        page.goto(url)
        page.wait_for_selector('#runCodeBtn', timeout=30000)

        # Extract schema from question description (everything from "Tables:" onward)
        question_text = page.inner_text('#questionTxt')
        schema = ""
        if "Tables:" in question_text:
            schema = question_text[question_text.index("Tables:"):].strip()

        # Click Run Code and wait for output
        page.click('#runCodeBtn')
        page.wait_for_function(
            "document.querySelector('#output-view') && document.querySelector('#output-view').innerText.trim().length > 0",
            timeout=30000
        )
        table_data = page.inner_text('#output-view').strip()

        browser.close()
        return schema, table_data


url = input("Enter problem URL: ").strip()

schema, table_data = scrape_problem(url)

output = f"=== TABLE SCHEMA ===\n{schema}\n\n=== TABLE DATA ===\n{table_data}\n"

print(output)

with open("problem_data.txt", "w", encoding="utf-8") as f:
    f.write(output)

print("Saved to problem_data.txt")
