"""Build the frontend for Netlify; Python is only needed at build time."""
import re
import shutil

from server import ROOT, ROUTE_MAP, build_screen_nav


def build():
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    screens = sorted(ROOT.glob("[0-9]*.html"))
    for source in screens:
        number = int(source.stem)
        html = source.read_text(encoding="utf-8")
        injection = build_screen_nav(source.name)
        if 4 <= number <= 28 and number != 6:
            injection = (
                '<link rel="stylesheet" href="/app-nav.css">'
                f'<script src="/app-nav.js" data-screen="{number}"></script>'
                + injection
            )
        html, count = re.subn(r"</body>", lambda _: injection + "</body>", html, count=1, flags=re.I)
        if count != 1:
            raise ValueError(f"Missing closing body in {source.name}")
        (output / source.name).write_text(html, encoding="utf-8")

    for pattern in ("*.css", "*.js"):
        for source in ROOT.glob(pattern):
            shutil.copy2(source, output / source.name)

    shutil.copy2(ROOT / "canvas.html", output / "canvas.html")

    routes = dict(ROUTE_MAP)
    for source in screens:
        routes[f"/{source.stem}"] = source.name
        routes[f"/screen/{source.stem}"] = source.name
    rules = ["# Generated from routes.json and the numbered screens by build.py."]
    for route, filename in routes.items():
        if not (output / filename).is_file():
            raise ValueError(f"Route {route} points to missing {filename}")
        rules.append(f"{route} /{filename} 200")
        if route != "/":
            rules.append(f"{route}/ /{filename} 200")
    (output / "_redirects").write_text("\n".join(rules) + "\n", encoding="utf-8")
    shutil.copy2(output / ROUTE_MAP["/"], output / "index.html")
    print(f"Built {len(screens)} screens and {len(routes)} routes in {output}")


if __name__ == "__main__":
    build()
