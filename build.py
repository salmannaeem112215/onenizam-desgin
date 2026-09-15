"""Build the frontend for Netlify; Python is only needed at build time."""
import re
import shutil

from server import ROOT, ROUTE_MAP, build_screen_nav


def build():
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)

    screens = sorted(
        [*ROOT.glob("*.html"), *ROOT.glob("web/**/*.html"), *ROOT.glob("web/**/*.htm")],
        key=lambda path: path.name,
    )
    unique_screens = []
    seen = set()
    for source in screens:
        if source.name in seen:
            continue
        seen.add(source.name)
        unique_screens.append(source)

    asset_rewrites = {
        '/shared-auth.css': '/web/assets/css/shared-auth.css',
        '/auth-flow.js': '/web/assets/js/auth-flow.js',
        '/canvas.css': '/web/assets/css/canvas.css',
        '/canvas.js': '/web/assets/js/canvas.js',
        '/app-nav.css': '/web/assets/css/app-nav.css',
        '/app-nav.js': '/web/assets/js/app-nav.js',
    }

    for source in unique_screens:
        number = int(source.stem) if source.stem.isdigit() else None
        html = source.read_text(encoding="utf-8")
        for old, new in asset_rewrites.items():
            html = html.replace(old, new)
        injection = build_screen_nav(source.name)
        if number is not None and 4 <= number <= 28 and number != 6:
            injection = (
                '<link rel="stylesheet" href="/web/assets/css/app-nav.css">'
                f'<script src="/web/assets/js/app-nav.js" data-screen="{number}"></script>'
                + injection
            )
        html, count = re.subn(r"</body>", lambda _: injection + "</body>", html, count=1, flags=re.I)
        if count != 1:
            raise ValueError(f"Missing closing body in {source.name}")
        target = output / source.relative_to(ROOT).as_posix().lstrip('/')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    for asset_file in sorted(ROOT.rglob("*.css")) + sorted(ROOT.rglob("*.js")):
        if asset_file.is_dir():
            continue
        if any(part in {"web", "dist"} for part in asset_file.parts):
            pass
        if asset_file.name in {"canvas.css", "canvas.js", "shared-auth.css", "auth-flow.js", "app-nav.css", "app-nav.js"}:
            rel = asset_file.relative_to(ROOT)
            dest = output / rel.as_posix().lstrip('/')
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset_file, dest)

    canvas_source = ROOT / "web" / "canvas.html"
    if not canvas_source.exists():
        canvas_source = ROOT / "canvas.html"
    shutil.copy2(canvas_source, output / "canvas.html")

    routes = dict(ROUTE_MAP)
    for source in unique_screens:
        relative = source.relative_to(ROOT).as_posix()
        routes[f"/{source.stem}"] = relative
        routes[f"/screen/{source.stem}"] = relative
    rules = ["# Generated from routes.json and the numbered screens by build.py."]
    for route, filename in routes.items():
        target = output / filename
        if not target.is_file():
            raise ValueError(f"Route {route} points to missing {filename}")
        rules.append(f"{route} /{filename} 200")
        if route != "/":
            rules.append(f"{route}/ /{filename} 200")
    (output / "_redirects").write_text("\n".join(rules) + "\n", encoding="utf-8")
    root_index = ROOT / ROUTE_MAP["/"]
    if not root_index.exists():
        root_index = ROOT / "web" / ROUTE_MAP["/"]
    shutil.copy2(root_index, output / "index.html")
    print(f"Built {len(unique_screens)} screens and {len(routes)} routes in {output}")


if __name__ == "__main__":
    build()
