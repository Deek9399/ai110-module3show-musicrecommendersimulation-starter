# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This simulation is a content-based music recommender that scores a catalog of 20 songs against a user taste profile and returns the top K matches with plain-language explanations. It uses no play history or collaborative data — every recommendation is derived entirely from song attributes and stated user preferences, making the reasoning fully transparent and inspectable.

---

## How The System Works

### Real-world vs. this simulation

Real-world recommenders (Spotify, YouTube, Netflix) use collaborative filtering — they don't just look at a song's attributes, they look at what millions of other users with similar taste histories listened to next. They also factor in implicit signals: how long you played a track, whether you skipped it, time of day, and session context. The result is a system that can surface songs you'd never have described yourself as liking, because it learned from people who are like you.

This simulation prioritizes **content-based filtering** instead — it compares the attributes of a song directly against the stated preferences of a user, with no historical play data needed. The tradeoff is transparency: every recommendation has a clear, explainable reason tied to features the user already understands (genre, mood, energy level). The system rewards songs that match the user's preferred genre and mood first (high-weight categorical match), then fine-tune rankings using continuous audio features to break ties.

---

### Song features used

| Feature | Type | Role in scoring |
|---|---|---|
| `genre` | categorical | Primary match — highest point value |
| `mood` | categorical | Secondary match — strong contextual signal |
| `energy` | float 0–1 | Continuous similarity — widest range in dataset |
| `valence` | float 0–1 | Tiebreaker — bright vs. dark sound |
| `acousticness` | float 0–1 | Tiebreaker — produced vs. organic feel |
| `tempo_bpm` | float | Not scored — correlated with genre, low added value |
| `danceability` | float 0–1 | Not scored — correlated with energy |

### User profile fields

| Field | Type | Purpose |
|---|---|---|
| `genre` | str | Exact genre preference |
| `related_genres` | list[str] | Genres that earn partial credit |
| `mood` | str | Preferred mood/activity context |
| `target_energy` | float 0–1 | Ideal energy level |
| `target_valence` | float 0–1 | Ideal musical positivity |
| `target_acousticness` | float 0–1 | Ideal acoustic vs. electronic feel |
| `likes_acoustic` | bool | Boolean form of acousticness preference |

---

### Algorithm Recipe

Each song is scored out of a maximum of **6.0 points**. The rules are applied in order:

```
1. GENRE RULE (categorical)
   Exact genre match   → +2.0 pts
   Related genre match → +1.0 pt
   No match            → +0.0 pts

2. MOOD RULE (categorical)
   Exact mood match    → +1.5 pts
   No match            → +0.0 pts

3. ENERGY SIMILARITY (continuous)
   +1.5 × (1 − (song.energy − target_energy)²)
   max = 1.5 pts   (full points when energies are identical)

4. VALENCE SIMILARITY (continuous)
   +0.5 × (1 − (song.valence − target_valence)²)
   max = 0.5 pts

5. ACOUSTICNESS SIMILARITY (continuous)
   +0.5 × (1 − (song.acousticness − target_acousticness)²)
   max = 0.5 pts
```

Songs are then sorted by score descending and the top K are returned, each with a plain-language explanation of why it was recommended.

**Data flow:**
```
user_prefs + songs.csv
       ↓
   load_songs()        — parse CSV into list of dicts
       ↓
   score_song()        — apply recipe above to each song
       ↓
   recommend_songs()   — sort by score, slice top K, attach explanations
       ↓
   print results
```

---

### Known Biases and Limitations

- **Genre dominance:** At +2.0 pts, genre is the single largest signal. A perfect mood + energy match without a genre match (2.0 pts) can still outscore a mood mismatch within the same genre — which means a "wrong mood, right genre" song may rank above a "right mood, wrong genre" song. This could surface energetic pop songs to a user who wanted something calm.

- **Cold-start taste assumption:** The profile requires the user to know and state their preferred genre, mood, and energy upfront. A user who says "I like whatever is on" cannot be served well.

- **Catalog bias:** The 20-song catalog skews toward lofi, pop, and ambient. Genres like hip-hop, classical, or R&B are entirely absent — users with those tastes will always get poor recommendations regardless of weighting.

- **No diversity control:** The ranking picks the K closest matches, which means a user could receive five nearly identical songs (e.g., five pop/happy tracks) with no variety introduced.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

**Example output:**

![Music Recommender terminal output](src/assets/Screenshot%202026-04-18%20184129.png)

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

