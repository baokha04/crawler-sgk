import asyncio
from playwright.async_api import async_playwright
from app.domains.books.book_service import BookService

class SGKCrawler:
    def __init__(self, book_service: BookService):
        self.book_service = book_service

    async def crawl(self, url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            print(f"Navigating to {url}...")
            await page.goto(url, wait_until="networkidle")
            
            # Wait a bit for the viewer to initialize
            await asyncio.sleep(5)

            # Extract title and total pages
            title = await page.title()
            
            total_pages = 151 # Default fallback
            try:
                # Try to find total pages in the UI
                # Common selectors for these types of readers
                selectors = [".total-page", ".totalPages", ".page-count", "#totalPages"]
                for selector in selectors:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        if text:
                            # Extract numbers from text like "/ 151" or "151 pages"
                            import re
                            match = re.search(r"(\d+)", text)
                            if match:
                                total_pages = int(match.group(1))
                                break
            except Exception as e:
                print(f"Error finding total pages: {e}")
            
            print(f"Book title and pages loaded.")
            book = await self.book_service.get_or_create_book(title, url, total_pages)

            # We'll iterate through the pages. 
            # Since it's a hash-based navigation, we can just update the hash.
            # We'll try to go page by page.
            for p_num in range(total_pages):
                page_url = f"{url.split('#')[0]}#page={p_num}"
                print(f"Processing page {p_num}...")
                
                await page.goto(page_url)
                # Wait for images to load
                await asyncio.sleep(2) 
                
                # Extract all images in .page-content
                images = await page.query_selector_all(".page-content img")
                if not images:
                    # Try a more generic selector if needed
                    images = await page.query_selector_all("img[src*='data:image'], img[src*='blob']")
                
                for idx, img in enumerate(images):
                    src = await img.get_attribute("src")
                    if src:
                        # We might have multiple images if it's double page, 
                        # but if we go #page=0, #page=1, it should work fine.
                        # We'll use p_num as the page identifier.
                        await self.book_service.add_page(book.id, p_num, src)
                        print(f"Saved page {p_num} image.")
                        break # Usually one main image per page in single view

            await browser.close()
            print("Crawl completed.")
