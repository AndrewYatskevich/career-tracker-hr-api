from urllib.parse import urlparse


def extract_domain(received_url: str) -> str:
    """Извлекает доменное имя из url-адреса."""
    parsed_url = urlparse(received_url)
    domain = parsed_url.netloc.replace("www.", "").split(".")[0].title()
    if domain == "Github":
        domain = "GitHub"
    return domain
