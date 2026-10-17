#!/usr/bin/env python3
"""Download demos/posters into site/slug/, dedup by sha256 hardlink/symlink."""
from __future__ import annotations
import hashlib, os, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path('/workspace/awesome-meme-video')
BLOB = ROOT / '_blobs'  # content-addressed store
BLOB.mkdir(exist_ok=True)

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def filename_from_url(url: str) -> str:
    path = unquote(urlparse(url).path)
    name = Path(path).name
    if not name or name in ('video.mp4', 'example.mp4', 'poster.jpg'):
        # keep parent folder hint
        parts = Path(path).parts
        if len(parts) >= 2:
            name = f"{parts[-2]}-{parts[-1]}"
    return name

def download(url: str, dest: Path) -> tuple[bool, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + '.part')
    if dest.exists() and dest.stat().st_size > 0:
        return True, 'exists'
    cmd = ['curl', '-fsSL', '--retry', '3', '--retry-delay', '1', '-o', str(tmp), url]
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        if tmp.exists():
            tmp.unlink()
        return False, 'curl_fail'
    digest = sha256_file(tmp)
    blob = BLOB / digest[:2] / digest
    blob.parent.mkdir(parents=True, exist_ok=True)
    if not blob.exists():
        tmp.rename(blob)
    else:
        tmp.unlink()
    # hardlink into place if possible else symlink
    if dest.exists():
        dest.unlink()
    try:
        os.link(blob, dest)
    except OSError:
        os.symlink(os.path.relpath(blob, dest.parent), dest)
    return True, digest[:12]

def main(kind: str):
    tsv = ROOT / '_raw' / f'download-{kind}.tsv'
    rows = [l.strip().split('\t') for l in tsv.read_text().splitlines() if l.strip()]
    ok = fail = 0
    log = []
    for i, (src, slug, url) in enumerate(rows, 1):
        out_dir = ROOT / ('makeviral' if src=='makeviral' else 'remakeyourmeme') / slug / ('demos' if kind=='videos' else 'posters')
        name = filename_from_url(url)
        dest = out_dir / name
        success, info = download(url, dest)
        status = 'OK' if success else 'FAIL'
        if success: ok += 1
        else: fail += 1
        line = f'{status}\t{src}\t{slug}\t{info}\t{url}\t{dest}'
        log.append(line)
        if i % 25 == 0 or not success:
            print(f'[{i}/{len(rows)}] {status} {slug} {name} {info}', flush=True)
    (ROOT / '_raw' / f'download-{kind}.log').write_text('\n'.join(log)+'\n')
    print(f'DONE {kind}: ok={ok} fail={fail}')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'videos')
