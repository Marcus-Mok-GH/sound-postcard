"""Bind a postcard's two local media files into a single offline HTML file."""
import argparse
from base64 import b64encode
from html import escape
from pathlib import Path


def media(path, kind):
    data = path.read_bytes()
    if kind == 'image':
        mime = 'image/png' if data.startswith(b'\x89PNG\r\n\x1a\n') else 'image/jpeg' if data.startswith(b'\xff\xd8\xff') else None
        if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
            mime = 'image/webp'
    else:
        mime = 'audio/mpeg' if data[:3] == b'ID3' or (len(data) > 1 and data[0] == 255 and data[1] & 224 == 224) else None
        if data[:4] == b'RIFF' and data[8:12] == b'WAVE':
            mime = 'audio/wav'
    if not mime:
        raise ValueError(f'Not a supported {kind} file: {path}')
    return f'data:{mime};base64,' + b64encode(data).decode('ascii')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('image', 'audio', 'out'):
        p.add_argument('--' + arg, type=Path, required=True)
    for arg in ('title', 'note', 'alt', 'listen'):
        p.add_argument('--' + arg, required=True)
    a = p.parse_args()
    title, note, alt, listen = map(lambda s: escape(s, quote=True), (a.title, a.note, a.alt, a.listen))
    try:
        picture, sound = media(a.image, 'image'), media(a.audio, 'audio')
        with a.out.open('x', encoding='utf-8') as f:
            f.write(f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · Sound Postcard</title>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#e3ddcd;color:#202e2b;font:1rem/1.45 Georgia,serif}}main{{max-width:64rem;margin:5vh auto;padding:clamp(1rem,3vw,2.6rem);background:#fff9e9;border-top:6px solid #ae432b;box-shadow:0 8px 28px #24392d22}}header,footer,b{{font:700 .78rem/1.5 system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase}}header,footer{{display:flex;justify-content:space-between;gap:1em}}section{{display:grid;grid-template-columns:3fr 2fr;align-items:center;gap:2rem;margin:1.25rem 0}}img{{display:block;width:100%;height:auto}}h1{{font-size:clamp(2rem,4vw,3.6rem);line-height:1;margin:.35em 0}}aside p{{font-size:1.17rem}}.cue{{color:#5a4940}}audio{{width:100%;margin:.4em 0}}footer{{padding-top:1rem;border-top:1px solid #927d6d}}@media(max-width:640px){{main{{margin:0}}section{{grid-template-columns:1fr;gap:.5rem}}}}</style>
<main><header><span>Sound Postcard</span><span>Field recordings / Imagined</span></header>
<section><img src="{picture}" alt="{alt}"><aside><b>Dear listener,</b><h1>{title}</h1><p>{note}</p><b>Listen for</b><p class="cue">{listen}</p><audio controls preload="metadata" aria-label="Soundscape: {title}" src="{sound}"></audio></aside></section>
<footer><span>Picture + sound</span><span>Keep this moment ↗</span></footer></main></html>''')
    except (OSError, ValueError) as err:
        p.exit(1, f'press: {err}\n')
