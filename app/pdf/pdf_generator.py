from playwright.async_api import async_playwright
import tempfile
import os

async def generate_pdf(html_content: str, format_type: str = "A4") -> bytes:
    """
    Generate PDF from HTML string using Playwright.
    format_type can be 'A4' or 'receipt' (80mm)
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Write HTML to a temp file to ensure resources load properly
        # For simple templates without external deps, set_content is enough
        await page.set_content(html_content, wait_until="networkidle")
        
        pdf_kwargs = {
            "print_background": True,
            "margin": {"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"}
        }
        
        if format_type == "receipt":
            # 80mm thermal printer format approx width
            pdf_kwargs["width"] = "80mm"
            pdf_kwargs["height"] = "297mm" # Allows auto-cut, arbitrary long
            pdf_kwargs["margin"] = {"top": "5mm", "right": "2mm", "bottom": "5mm", "left": "2mm"}
        else:
            pdf_kwargs["format"] = "A4"
            
        pdf_bytes = await page.pdf(**pdf_kwargs)
        await browser.close()
        
        return pdf_bytes
