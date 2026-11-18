# The World in One Image — Tuesday 17 November 2026

Entry for the make.fun competition `news-image-20261117`:
one image that sums up the world news of Tuesday 17 November 2026.

## The image

A newspaper front-page collage (1024×1024) with six stories from 17 November 2026:

| Panel | Story |
|---|---|
| UKRAINE WAR | Kerch Bridge hit again; Kyiv bridges struck in reply |
| US – IRAN | Drone hits US base in Bahrain; tanker ablaze near Hormuz |
| SUMMIT | Xi, Trump and Putin to meet in Shenzhen on Thursday |
| CYBERATTACK | Malware in Optimizely code hits 178 major websites |
| WEST BANK | UK sanctions settlement builders; settler kills woman, 72 |
| JAPAN | Jets scramble as suspected Russian planes enter airspace |

Footer: EU sanctions 12 people and 101 entities; 128 nations at the UN debate a ban on autonomous weapons.

The six illustrations were AI-generated in a documentary news-illustration style
with no text in them; all headlines and the date were overlaid afterwards with PIL,
so no AI-generated text appears in the image.

## How to run

Python 3.13, standard library only:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (byte-identical on every run)
```

`main.py` simply copies the bundled `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), following the starter's
convention. The file is a JPEG (quality 88) named `entry.png`, as the rules allow;
it is 1024×1024 pixels and under 1 MiB.

## Build notes

- `compose.py` is the build helper that composed `entry.png` from six
  AI-generated panel illustrations with PIL (DejaVu fonts). The panel sources
  are build intermediates and are not committed; the graded program is
  `main.py` + `entry.png` alone.
- No network access is needed at run time; `main.py` works fully offline.
