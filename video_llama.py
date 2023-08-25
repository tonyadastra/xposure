from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Launch a new browser instance
        browser = p.chromium.launch(headless=False)  # Set headless to True if you don't want to see the browser UI
        page = browser.new_page()

        # Navigate to the Hugging Face page
        page.goto("https://damo-nlp-sg-video-llama.hf.space/")
        
        page.wait_for_selector('id=component-4')
        
        page.locator('input[accept="video/x-m4v,video/*"]').set_input_files('./output/slam_dunk_0.mp4')
        page.wait_for_timeout(1000)
        
        page.locator('#component-7').click()
        
        page.locator('#component-18 > label > textarea').fill('Describe this video in detail, be as descriptive as possible.')
        
        page.keyboard.down("Enter")
        
        page.wait_for_timeout(30000)
        
        # TODO
        # Add any additional actions or interactions you want to perform on the page here

        # Close the browser
        # browser.close()

if __name__ == "__main__":
    run()
