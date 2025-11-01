# wiki-test (Nuxt 3 + Nuxt UI)

A small Nuxt 3 app that loads 10 recent Wikipedia stories, performs a naive positive/negative/neutral sentiment analysis, and renders a visualization page using @nuxt/ui.

## Run locally (Windows PowerShell)

```pwsh
# From repo root
cd "d:\School\GoIT\Courses\Product_Analytics\wiki-test"

# Install deps
npm install

# Start dev server
npm run dev

# Or build for production and preview
npm run build
npm run preview
```

Then open the local URL shown in the terminal (usually http://localhost:3000).

## Notes
- Sentiment is computed client-side via a simple lexicon in `composables/useSentiment.ts`.
- Data lives in `data/stories.json`. Update it to change inputs.
- UI built with `@nuxt/ui` cards, badges, table, and simple progress bars.

## Structure
- `pages/index.vue` – main visualization
- `data/stories.json` – stories dataset
- `composables/useSentiment.ts` – naive sentiment scorer
- `nuxt.config.ts` – Nuxt 3 config with `@nuxt/ui` module
