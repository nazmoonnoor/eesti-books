#!/bin/bash
# Double-click to open the Estonian wiki site in your browser (no install needed).
cd "$(dirname "$0")" || exit 1
open "docs/index.html"
