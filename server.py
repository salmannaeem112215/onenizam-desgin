import io
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PORT = 8000

ROUTE_MAP = {
    "/": "1.html",
    "/index": "1.html",
    "/login": "1.html",
    "/create-password": "2.html",
    "/password-updated": "3.html",
    "/sales": "4.html",
    "/checkout": "5.html",
    "/appointment": "6.html",
    "/calendar": "7.html",
    "/front-desk": "9.html",
    "/hub": "10.html",
    "/messages": "11.html",
    "/services": "12.html",
    "/resources": "13.html",
    "/staff-create": "15.html",
    "/staff": "16.html",
    "/customers": "17.html",
    "/customer-add": "18.html",
    "/reviews": "19.html",
    "/reports": "20.html",
    "/service-new": "21.html",
    "/settings": "22.html",
    "/billing": "23.html",
    "/business-setup": "24.html",
    "/business-hours": "25.html",
    "/contact-details": "26.html",
    "/location-setup": "27.html",
    "/media": "28.html",
}


def resolve_route(path: str):
    parsed = urlparse(path)
    request_path = parsed.path.rstrip("/") or "/"

    if request_path in ROUTE_MAP:
        return ROUTE_MAP[request_path]

    if request_path.startswith("/screen/"):
        screen_name = request_path.split("/screen/", 1)[1]
        if screen_name and screen_name.isdigit():
            file_name = f"{screen_name}.html"
            if (ROOT / file_name).exists():
                return file_name

    if request_path.startswith("/") and request_path[1:].isdigit():
        file_name = f"{request_path[1:]}.html"
        if (ROOT / file_name).exists():
            return file_name

    return None


def build_screen_nav(current_file_name: str):
    numbers = []
    for i in range(1, 29):
        if (ROOT / f"{i}.html").exists():
            numbers.append(i)

    current = 1
    try:
        current = int(Path(current_file_name).stem)
    except Exception:
        current = 1

    links = []
    for num in numbers:
        active = " is-active" if num == current else ""
        links.append(f'<a class="screen-nav-link{active}" href="/{num}">{num}</a>')

    return f"""
    <style>
      .screen-nav-wrap {{
        position: fixed;
        left: 50%;
        transform: translateX(-50%);
        bottom: 12px;
        z-index: 99999;
        width: auto;
        max-width: calc(100% - 24px);
        background: rgba(17, 28, 46, 0.96);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.2);
        padding: 10px 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        font-family: Arial, sans-serif;
      }}
      .screen-nav-links {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin: 0 auto;
      }}
      .screen-nav-link {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 38px;
        height: 38px;
        border-radius: 10px;
        background: rgba(255,255,255,0.08);
        color: white;
        text-decoration: none;
        font-size: 13px;
        font-weight: 700;
        padding: 0 10px;
      }}
      .screen-nav-link:hover {{ background: rgba(255,255,255,0.16); }}
      .screen-nav-link.is-active {{ background: #ffffff; color: #111c2e; }}
      .screen-nav-spacer {{
        height: 60px;
      }}
    </style>
    <div class="screen-nav-wrap">
      <div class="screen-nav-links">{''.join(links)}</div>
    </div>
    <div class="screen-nav-spacer"></div>
    """


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        mapped = resolve_route(self.path)
        if mapped:
            self.path = "/" + mapped

        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.build_index().encode("utf-8"))
            return

        return super().do_GET()

    def send_head(self):
        path = self.translate_path(self.path)
        if path.lower().endswith(".html"):
            try:
                with open(path, "rb") as file:
                    content_bytes = file.read()
            except OSError:
                return super().send_head()

            text = content_bytes.decode("utf-8", errors="ignore")
            marker = "</body>"
            if marker.lower() in text.lower():
                injection = build_screen_nav(Path(path).name)
                text = text.replace(marker, injection + marker, 1)
                content_bytes = text.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content_bytes)))
            self.end_headers()
            return io.BytesIO(content_bytes)

        return super().send_head()

    def build_index(self):
        files = sorted(ROOT.glob("*.html"), key=lambda p: p.name)
        links = []
        for file in files:
            num = file.stem
            links.append(f'<li><a href="/{num}">{file.name}</a></li>')
        return """
        <!doctype html>
        <html>
        <head><meta charset="utf-8"><title>Screen Routes</title></head>
        <body>
            <h1>Available Screens</h1>
            <ul>
                {links}
            </ul>
        </body>
        </html>
        """.format(links="\n".join(links))


if __name__ == "__main__":
    print(f"Starting simple screen router on http://localhost:{PORT}")
    print("Example routes: /, /1, /2, /login, /sales, /calendar, /messages, /customers")
    try:
        httpd = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
