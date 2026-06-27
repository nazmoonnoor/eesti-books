#!/bin/bash
# Double-click to open the Estonian wiki preview in your browser.
# No installation needed — it just opens the pre-built HTML pages.
cd "$(dirname "$0")" || exit 1
open "preview/index.html"
