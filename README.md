# PingSense

Website to search for equipment and tutorials, from beginner to professional table tennis.

PingSense is a data-driven hub for table tennis players: a landing page that showcases a rubber equipment database and curated YouTube learning resources.

## Contents

- [`index.html`](index.html) - the PingSense landing page. A single self-contained static page (no build step) with a hero section, equipment/database highlights, and a "Learn From the Best" section linking to curated YouTube channels for coaching, equipment reviews, and match footage.
- [`data/table_tennis_rubbers.csv`](data/table_tennis_rubbers.csv) - dataset of 984 table tennis rubbers across 52 brands, sourced from real user reviews on [revspin.net](https://revspin.net/rubber/). Each rubber lists Price and 0-10 scale ratings for Speed, Spin, Tackiness, and Overall. Rubbers with 3 or fewer user ratings were excluded to keep the data statistically meaningful.

## Viewing the site

Open `index.html` directly in a browser, or serve the folder with any static file server (e.g. `npx serve .`).

## Data source

The dataset is not currently wired into the page dynamically - it's a standalone CSV asset intended for future features (e.g. searchable/filterable equipment tables, rubber comparisons, or recommendation logic). Data was compiled from [revspin.net/rubber](https://revspin.net/rubber/), a community-driven table tennis equipment review site, filtered to rubbers with more than 3 user ratings.
