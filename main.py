
import httpx
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
from dataclasses import asdict, dataclass
import asyncio
import time


@dataclass
class Product:
    company: str | None
    name: str | None
    model_number: str | None
    price: str | None

async def get_html(baseurl: str, client: httpx.AsyncClient) -> HTMLParser:
    headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

    try:
        response = await client.get(baseurl, headers=headers)
        # print(response)

        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f'Error response {exc.response.status_code} while requesting {exc.request.url!r}')
        return None
   
    return HTMLParser(response.text)
    

def extract_text(html: HTMLParser, sel: str) -> str | None:
    try:
        text = html.css_first(sel).text()
        return clean_data(text)
    except AttributeError:
        return None

def clean_data(value):
    chars_remove = ["MODEL #:", "\xa0"]
    for char in chars_remove:
        if char in value:
            value = value.replace(char, "")
    return value.strip()
        
    
# def parse_hardware_page(html: HTMLParser):
#     hardwares = html.css('ul.department-list li')
#     for hardware in hardwares:
#         a_tag = hardware.css_first('a')
#         if a_tag and 'href' in a_tag.attributes:
#             yield urljoin('https://www.hardwareworld.com', a_tag.attributes['href'])
#         else:
#             print("Object is None or href attribute missing")
        
def parse_objects_page(html: HTMLParser):
    
     #products = html.css("div#_ctl0_body_noSubcategoriesPanel")
    #products = html.css("article.product-box")
    #print(products)
    objs = html.css('h2')
    for obj in objs:
        a_tag = obj.css_first('a')
        if a_tag and 'href' in a_tag.attributes:
            yield urljoin('https://www.hardwareworld.com', a_tag.attributes['href'])
        else:
            print("Object is None or href attribute missing")
            

def parse_product_page(html: HTMLParser) -> Product:
    return Product(
        company=extract_text(html, 'span.title'),
        name=extract_text(html, 'h2'),
        model_number=extract_text(html, 'span.model-no'),
        price=extract_text(html, 'span.price'),
    )

            
async def main():
    baseurls = ["https://www.hardwareworld.com/c9w7bs9/Automotive",
                "https://www.hardwareworld.com/crnhca4/Builders-Supplies",
                "https://www.hardwareworld.com/cn7nu5m/Electrical",
                "https://www.hardwareworld.com/ckzr32n/Great-Outdoors",
                "https://www.hardwareworld.com/cyb7lgq/Hand-Tools",
                "https://www.hardwareworld.com/c7oakpi/Heating-Cooling",
                "https://www.hardwareworld.com/cn7nu51/Household-Essentials",
                "https://www.hardwareworld.com/ciruc14/Landscaping-Yard-Garden",
                "https://www.hardwareworld.com/c10kbjf/Lighting",
                "https://www.hardwareworld.com/cw3audu/Masonry-Concrete",
                "https://www.hardwareworld.com/cyb7lgo/Paint-Stain",
                "https://www.hardwareworld.com/cw3auek/Patio-Backyard",
                "https://www.hardwareworld.com/c10kbiv/Plumbing",
                "https://www.hardwareworld.com/cec0twq/Power-Tools",
                "https://www.hardwareworld.com/ckzr33g/Safety-Products-for-Work-Home",
                "https://www.hardwareworld.com/cw3audz/Stationary-Tools",
                "https://www.hardwareworld.com/cw3audz/Stationary-Tools"]
   
        
    for baseurl in baseurls:  
        async with httpx.AsyncClient() as client:
            html = await get_html(baseurl, client)
            if html is None:
                return
        
        # hardware = []
        # hardware_urls = list(parse_hardware_page(html))
        # for url in hardware_urls:
        #     html = await get_html(url, client)
        #     if html is None:
        #         continue
        #     hardware.append(parse_objects_page(html))
        #     print(url)
        
            product_urls = list(parse_objects_page(html))

            products = []
            for url in product_urls:
                html = await get_html(url, client)
                if html is None:
                    continue
                products.append(parse_product_page(html))
                time.sleep(0.5)
                
            

            for item in products:
                print(asdict(item))

if __name__ == "__main__":
    asyncio.run(main())


    


  


    












