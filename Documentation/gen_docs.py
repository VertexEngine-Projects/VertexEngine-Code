import json
from pathlib import Path

with open("C:/Vertex/Documentation/functions.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

template = Path("C:/Vertex/Documentation/template.html").read_text(encoding="utf-8")

def render_parameters(params):
    if not params:
        return "<ul><li>None</li></ul>"

    html = "<ul>"
    for p in params:
        html += f"<li><code>{p['name']}</code> ({p['type']}): {p['description']}</li>"
    html += "</ul>"
    return html

for item in docs:
    out_dir = Path(item["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    html = template
    html = html.replace("{{title}}", item["title"])
    html = html.replace("{{signature}}", item["signature"])
    html = html.replace("{{description}}", item["description"])
    html = html.replace("{{usage}}", item["usage"])
    html = html.replace("{{parameters}}", render_parameters(item["parameters"]))
    html = html.replace("{{returns}}", item["returns"])

    (out_dir / item["file"]).write_text(html, encoding="utf-8")

print("✅ Documentation generated using locked template.")
