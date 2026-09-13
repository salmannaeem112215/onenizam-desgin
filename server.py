import io
import os
import sys
import threading
import time
import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PORT = 8000


def project_version():
    files = list(ROOT.glob("*.html")) + list(ROOT.glob("*.css")) + list(ROOT.glob("*.js")) + [Path(__file__)]
    return max((p.stat().st_mtime_ns for p in files if p.exists()), default=0)


LIVE_RELOAD_SCRIPT = """
<script>
(function () {
  let version = null;
  async function checkForChanges() {
    try {
      const response = await fetch('/__live_version', { cache: 'no-store' });
      const next = await response.text();
      if (version !== null && next !== version) window.location.reload();
      version = next;
    } catch (_) {}
  }
  checkForChanges();
  setInterval(checkForChanges, 1000);
})();
</script>
"""

ROUTE_MAP = {
    "/": "9.html",
    "/index": "9.html",
    "/login": "1.html",
    "/forgot-password": "29.html",
    "/create-account": "30.html",
    "/verify-code": "31.html",
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
    available_numbers = [i for i in range(1, 32) if (ROOT / f"{i}.html").exists()]
    auth_flow = [1, 29, 30, 31, 2, 3]
    home_flow = [10, 9, 7, 4, 11]
    grouped_numbers = auth_flow + home_flow
    numbers = [num for num in grouped_numbers if num in available_numbers]
    numbers.extend(num for num in available_numbers if num not in grouped_numbers)
    auth_labels = {num: f"A.{index}" for index, num in enumerate(auth_flow, start=1)}
    home_labels = {10: "H0", 9: "H1", 7: "H2", 4: "H3", 11: "H4"}

    current = 1
    try:
        current = int(Path(current_file_name).stem)
    except Exception:
        current = 1

    links = []
    for num in numbers:
        active = " is-active" if num == current else ""
        label = auth_labels.get(num, home_labels.get(num, str(num)))
        links.append(f'<a class="screen-nav-link{active}" href="/{num}">{label}</a>')

    return f"""
    <style>
      .screen-nav-wrap {{
        position: fixed;
        left: 50%;
        bottom: 12px;
        transform: translateX(-50%);
        z-index: 99999;
        width: auto;
        max-width: calc(100% - 24px);
        background: rgba(17, 28, 46, 0.40);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.2);
        padding: 10px 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        font-family: Arial, sans-serif;
        backdrop-filter: blur(8px);
        transition: background .2s ease, width .2s ease, padding .2s ease;
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
      .screen-nav-toggle {{
        width: 38px;
        height: 38px;
        flex: 0 0 38px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.18);
        color: #fff;
        cursor: pointer;
        font: 700 18px/1 Arial, sans-serif;
      }}
      .screen-nav-toggle:hover {{ background: rgba(255,255,255,0.30); }}
      .screen-nav-wrap.is-collapsed {{
        width: 46px;
        height: 46px;
        padding: 4px;
        border-radius: 50%;
      }}
      .screen-nav-wrap.is-collapsed .screen-nav-links {{ display: none; }}
      .screen-nav-wrap.is-collapsed .screen-nav-toggle::before {{ content: '\u2630'; }}
      .screen-nav-wrap:not(.is-collapsed) .screen-nav-toggle::before {{ content: '\u2212'; }}
      .screen-nav-wrap.is-collapsed:hover {{
        width: auto;
        height: auto;
        padding: 10px 14px;
        border-radius: 18px;
      }}
      .screen-nav-wrap.is-collapsed:hover .screen-nav-links {{ display: flex; }}
      .screen-nav-wrap.is-collapsed:hover .screen-nav-toggle::before {{ content: '\u2212'; }}
    </style>
    <div class="screen-nav-wrap is-collapsed" id="screen-nav">
      <div class="screen-nav-links">{''.join(links)}</div>
      <button class="screen-nav-toggle" type="button" aria-label="Expand screen picker" title="Expand screen picker"></button>
    </div>
    <script>
      (() => {{
        const picker = document.getElementById('screen-nav');
        const toggle = picker && picker.querySelector('.screen-nav-toggle');
        if (!picker || !toggle) return;
        toggle.addEventListener('click', () => {{
          const collapsed = picker.classList.toggle('is-collapsed');
          toggle.setAttribute('aria-label', collapsed ? 'Expand screen picker' : 'Minimize screen picker');
          toggle.title = collapsed ? 'Expand screen picker' : 'Minimize screen picker';
        }});
      }})();
    </script>
    """


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if urlparse(self.path).path == "/__live_version":
            body = str(project_version()).encode("ascii")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
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
                try:
                    screen_number = int(Path(path).stem)
                except ValueError:
                    screen_number = 0
                if 4 <= screen_number <= 28 and screen_number != 6:
                    injection = (
                        '<link rel="stylesheet" href="/app-nav.css">'
                        f'<script src="/app-nav.js" data-screen="{screen_number}"></script>'
                        + injection
                    )
                text = text.replace(marker, injection + LIVE_RELOAD_SCRIPT + marker, 1)
                content_bytes = text.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
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

        def watch_server_file():
            last_mtime = os.path.getmtime(__file__)
            while True:
                time.sleep(1)
                try:
                    current_mtime = os.path.getmtime(__file__)
                    if current_mtime != last_mtime:
                        os.execv(sys.executable, [sys.executable, *sys.argv])
                    last_mtime = current_mtime
                except OSError:
                    pass

        threading.Thread(target=watch_server_file, daemon=True).start()
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
