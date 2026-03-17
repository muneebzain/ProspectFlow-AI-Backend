import httpx
from bs4 import BeautifulSoup


class WebsiteEnrichmentService:
    async def fetch_website_content(self, url: str) -> dict:
        if not url:
            return {
                "website_title": None,
                "website_description": None,
                "website_text": None,
                "website_fetch_status": "missing_url",
            }

        normalized_url = url.strip()
        if not normalized_url.startswith("http://") and not normalized_url.startswith(
            "https://"
        ):
            normalized_url = f"https://{normalized_url}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        }

        try:
            async with httpx.AsyncClient(
                timeout=15.0, follow_redirects=True, headers=headers
            ) as client:
                response = await client.get(normalized_url)
                response.raise_for_status()
        except Exception as e:
            return {
                "website_title": None,
                "website_description": None,
                "website_text": None,
                "website_fetch_status": f"failed: {str(e)}",
            }

        try:
            soup = BeautifulSoup(response.text, "html.parser")

            title = (
                soup.title.string.strip() if soup.title and soup.title.string else None
            )

            meta_description = None
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag and meta_tag.get("content"):
                meta_description = meta_tag["content"].strip()

            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            body_text = soup.get_text(separator=" ", strip=True)
            body_text = " ".join(body_text.split())

            if len(body_text) > 4000:
                body_text = body_text[:4000]

            return {
                "website_title": title,
                "website_description": meta_description,
                "website_text": body_text if body_text else None,
                "website_fetch_status": "success",
            }

        except Exception as e:
            return {
                "website_title": None,
                "website_description": None,
                "website_text": None,
                "website_fetch_status": f"parse_failed: {str(e)}",
            }
