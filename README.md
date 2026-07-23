# PingSense

Website to search for equipment and tutorials, from beginner to professional table tennis.

PingSense is a data-driven hub for table tennis players: a landing page that showcases a rubber equipment database and curated YouTube learning resources.

## Contents

- [`index.html`](index.html) - the PingSense landing page. A single self-contained static page (no build step) with a hero section, equipment/database highlights, and a "Learn From the Best" section linking to curated YouTube channels for coaching, equipment reviews, and match footage.
- [`data/table_tennis_rubbers.csv`](data/table_tennis_rubbers.csv) - dataset of 512 table tennis rubbers across 38 brands, each rated on a 0-10 scale across 10 performance dimensions: Speed, Spin, Control, Tackiness, Weight, Sponge Hardness, Gears, Throw Angle, Consistency, and Durability.

## Viewing the site

Open `index.html` directly in a browser, or serve the folder with any static file server (e.g. `npx serve .`).

## Data source

The dataset is not currently wired into the page dynamically - it's a standalone CSV asset intended for future features (e.g. searchable/filterable equipment tables, rubber comparisons, or recommendation logic).
