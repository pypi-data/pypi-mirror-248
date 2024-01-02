# mk_badge

A python script to help making SVG badges like the ones made by travis-ci to show the status of a build

# Examples

```bash
mk_badge -f examples/blackNwhite.svg \
    --left-fill-color 0,0,0 --left-text-color 255,255,255 \
    --right-fill-color 255,255,255 --right-text-color 0,0,0 \
    "Black" "White"
```

![](/examples/blackNwhite.svg)

```bash
mk_badge -f examples/redNgreen_comicsans.svg \
    --left-fill-color 255,0,0 --left-text-color 255,255,255 \
    --right-fill-color 0,255,0 --right-text-color 0,0,0 \
    --font "Comic Sans MS" \
    "Comics Sans MS:" "Serious"
```

![](/examples/redNgreen_comicsans.svg)

```bash
mk_badge -f examples/build_passing.svg \
    --left-fill-color 93,93,93 --left-text-color 255,255,255 \
    --right-fill-color 77,199,31 --right-text-color 255,255,255 \
    --left-stroke-color 93,93,93 --right-stroke-color 93,93,93 \
    "build" "passing"
```

![](/examples/build_passing.svg)
