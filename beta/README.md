# Reef Key — lite and pro builds

## The files

| File | What it is |
|---|---|
| `reef-source.html` | **The one you edit.** Single source for both builds. |
| `reef-pro.html` | Built output — everything switched on. |
| `reef-lite.html` | Built output — free version. |
| `build.py` | Regenerates the two builds from the source. |

Never edit `reef-pro.html` or `reef-lite.html` directly — they get overwritten.
Edit `reef-source.html`, then run:

```
python3 build.py
```

## Branding

The app is **Reef Key**. The Red Sea logo and red palette are gone — they were
not ours to use, and an app that calculates from any brand's products should
not wear one manufacturer's livery.

- Palette: deep water. Near-black ground (`#060b10`), bioluminescent cyan
  accent (`#2fe0c6`). Red is the first wavelength water absorbs, so at depth
  what is left is blue-green and the one bright thing is bioluminescent.
- Type: the system face (SF on Apple devices). Nothing is downloaded, and it
  makes the app read as native rather than as a web page.
- Mark: a key whose teeth read as the notches on a test strip, over water.
  Drawn inline as SVG in the masthead; `icons.py` renders the PNG set.

**The app now makes no network requests at all.** Google Fonts, the Red Sea
CDN pack shots and the Wikipedia/Commons species photos are all gone. That
matters twice over: an app that degrades without a connection is what App
Store guideline 4.2 is looking for, and the Commons photographs were licensed
works that mostly require attribution — not something to ship in a paid app
without credit.

## Icon files

`icon-1024.png` is for App Store Connect. `icon-512.png` and `icon-192.png`
are referenced by the manifest, `apple-touch-icon.png` by the home screen.
Regenerate them all with `python3 icons.py`.

## How the two builds differ

Only two lines change, and `build.py` changes them:

```js
var TIER = 'pro';              // or 'lite'
var KEY  = 'reef-tank-data';   // or 'reef-tank-data-lite'
```

Nothing is deleted to make the lite build. Every Pro feature is still in the
file; the app switches it off and shows a short note in its place. That means a
tank set up in Pro can be opened in Lite without damage, and upgrading later
just flips the flag back.

The separate storage key means **testing the lite build cannot touch your real
tank log.** The pro build keeps the original key, so your existing history
loads straight into Tank 1 with nothing to migrate by hand.

## What is free and what is Pro

**Lite:** one tank, all logging, trend charts, target bands, the salt and water
change calculator, maintenance reminders, backup and restore.

**Pro:** the correction engine, livestock-refined targets, unlimited tanks,
running costs, CSV export.

## Putting them on the iPad

Both builds need the image files (`redsea-logo-512.png`, `icon-512.png`,
`apple-touch-icon.png`, `manifest.webmanifest`) sitting alongside them, so keep
each build in its own folder with a copy of those files.

For two separate home screen icons, host them at two paths — for example
`/reef-app/` and `/reef-app/lite/` on GitHub Pages — and add each to the home
screen from Safari. They will appear as **Reef** and **Reef Lite**.

## Multiple tanks

- The tank pills appear under the title once there are two or more tanks.
- Add, duplicate and delete live in the ⚙ panel, top right.
- Each tank keeps its own targets, shelf, livestock, costs and test log.
- **Duplicate** copies the setup but starts a fresh log — the right choice for a
  frag tank run on the same regime.
- Backup files now carry every tank in one file.

## ICP analysis (Triton)

On the Test screen, below the corrections. Pro only.

**Setpoints are deliberately incomplete.** Triton's published reference values
are filled in for the major ions and for Li, Mo and Ni. Everything else is
blank, because a Triton report prints its own setpoint beside every element —
the keeper copies it across and the app follows the lab rather than a figure
guessed here. Anything left blank is skipped and listed at the bottom of the
assessment, never assumed.

**What it does with a report:**

- Contaminants first — anything above zero, ranked ahead of everything else.
- For an excess, the exact water change that reaches the setpoint, worked from
  the tank's net volume. Over 40% it stages the change instead of asking for a
  half-tank swap in one go.
- Where a water change cannot get there (the replacement water is not lower
  than the target), it says so rather than inventing a number.
- For a shortfall, the mass the tank is actually missing, so any brand of
  supplement can be measured against it.
- Where nothing on the shelf lists that element, it says that plainly.

**Still to do:** ATI, Oceamo and Fauna Marin have different element lists and
report layouts — the entry form is driven by `ICP_ELEMENTS`, so adding a lab is
a data change rather than a code change. PDF parsing comes after that.

## Tests

`test.js` runs the tank logic under node with a stubbed DOM — migration from the
old single-tank save, switching, persistence, and the awkward cases (empty
storage, corrupt storage, a deleted active tank).

```
node test.js
```
