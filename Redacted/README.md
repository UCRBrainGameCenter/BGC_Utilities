# Redacted

Redacted is a simple script where you need three things:

1. A directory with a bunch of pdfs
2. An empty output directory
3. A pdf that matches the first directory but only contains things you want to put on top of every pdf

This was meant primarly to allow people to easily redact a bunch of pdfs that all follow the exact same format. However, it could also serve as a way to easily add watermarks, page numbers, etc. 

**NOTE** This will only work on macs with `ps2pdf` and `pdf2ps` installed because we need to flatten the pdf as well as merge.