# blog-pipeline

> AI blog generator that doesn't sound like AI.

6-pass Claude API pipeline with a built-in humanizer, topic deduplication,
internal linking, and Supabase sync. The humanizer is the key differentiator —
it enforces a strict writing ruleset that removes every common AI tell.

---

## Passes

| Pass | What it does |
|------|-------------|
| 0 | Fetches existing titles from Supabase (prevents duplicates) |
| 1 | Identifies new topics (skips anything already written) |
| 2 | Plans structure per topic (comparison / deep-dive / case-study / how-to / opinion) |
| 3 | Generates full markdown content |
| 4 | **Humanizer** — strips AI tells (see below) |
| 5 | Adds internal links across all posts |
| 6 | Pushes to Supabase + updates local registry |

---

## The Humanizer

Pass 4 enforces these rules on every post:

- **Banned words**: leverage, seamless, robust, cutting-edge, game-changer,
  revolutionize, synergy, paradigm, transformative, unlock, delve, streamline,
  elevate, empower, holistic, utilize, facilitate, innovative
- **No em-dashes** (—) — replaced with commas or full stops
- **No semicolons** connecting sentences
- **No emojis**
- **Contractions required**: it's, we're, you'll, don't
- **Active voice only**
- **Max 1 exclamation mark** per post
- No "In conclusion / In summary" section openers

Use the humanizer standalone:

```python
from src.humanizer import humanize_post
clean = humanize_post(my_ai_draft)
```

---

## Setup

```bash
git clone https://github.com/YOUR_ORG/blog-pipeline
cd blog-pipeline
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
```

---

## Run

```bash
# Full pipeline: generate 5 blogs
python src/pipeline.py --passes 1-6 --count 5 --niche "developer tooling and SaaS"

# Re-humanize existing drafts only
python src/pipeline.py --passes 4

# Push already-written files to Supabase
python src/pipeline.py --passes 6

# Generate content without pushing
python src/pipeline.py --passes 1-5 --count 3
```

---

## Output

- `blogs/<slug>.md` — humanized markdown files
- `blogs/_topics.json` — topic cache
- `blogs/_plans.json` — structure plans
- `blogs/_registry.json` — pushed blog tracking

---

## Immediate next steps
1. Make the humanizer prompt configurable via `HUMANIZER_RULES` env / YAML
2. Add `--audit` flag: re-score all pushed blogs and unpublish weak ones
3. Add SEO scoring pass (keyword density check, meta description generation)
4. Package as a GitHub Action: auto-generate blogs on schedule

---

## Commercial viability
- Package the humanizer as a standalone API: `POST /humanize` → clean post
- Charge per post ($0.10–0.50) or monthly flat ($49–149)
- Differentiator: "the only AI blog writer that bans its own clichés by design"
- Add AI-detector score before/after to prove improvement
