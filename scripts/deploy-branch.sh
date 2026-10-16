#!/bin/sh
# Builds the site and publishes it to the gh-pages branch (Settings -> Pages -> Deploy from a branch -> gh-pages, / (root)).
# Use this when GitHub Actions is unavailable. Needs: node, npm, python3, and push access to origin.
set -e
cd "$(dirname "$0")/.."
npm ci
BASE=${BASE:-/gtps-guide/} npm run build
out=$(mktemp -d)
cp -r .vitepress/dist/. "$out"
touch "$out/.nojekyll"
cd "$out"
git init -q -b gh-pages
git add -A
git commit -q -m "Publish the guide"
git push -f "$(git -C "$OLDPWD" remote get-url origin)" gh-pages
