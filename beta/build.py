"""Builds reef-lite.html and reef-pro.html from one source file.

Nothing is deleted to make the lite build — the TIER line is rewritten and the
app switches the Pro features off itself. Each build gets its own storage key,
so testing the lite version can never touch the real tank log.

Usage:  python3 build.py
"""
import io, os, sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reef-source.html')
OUT = os.path.dirname(os.path.abspath(__file__))

BUILDS = [
    # file name           tier    storage key            <title>                  home screen name
    ('reef-pro.html',    'pro',  'reef-tank-data',      'Reef Key',       'Reef Key'),
    ('reef-lite.html',   'lite', 'reef-tank-data-lite', 'Reef Key Lite',  'Reef Key Lite'),
]


def build():
    src = io.open(SRC, encoding='utf-8').read()

    for name, tier, key, title, short in BUILDS:
        out = src

        def swap(old, new):
            global_count = out.count(old)
            if global_count != 1:
                sys.exit('%s: expected 1 occurrence of %r, found %d' % (name, old[:60], global_count))
            return out.replace(old, new, 1)

        out = swap("var TIER = 'pro'; /* build:tier */",
                   "var TIER = '%s'; /* build:tier */" % tier)
        out = swap("var KEY = 'reef-tank-data';",
                   "var KEY = '%s';" % key)
        out = swap("<title>Reef Key</title>",
                   "<title>%s</title>" % title)
        out = swap('<meta name="apple-mobile-web-app-title" content="Reef Key">',
                   '<meta name="apple-mobile-web-app-title" content="%s">' % short)

        path = os.path.join(OUT, name)
        io.open(path, 'w', encoding='utf-8').write(out)
        print('%-16s tier=%-4s key=%-20s %7d bytes' % (name, tier, key, len(out)))


if __name__ == '__main__':
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    build()
