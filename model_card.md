# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeMatch 1.0**

A content-based music recommender that scores songs against a stated user taste
profile and returns the top matches with plain-language explanations.

---

## 2. Goal / Task

VibeMatch tries to answer the question: *"Given what a user tells me they like,
which songs in the catalog are most worth playing next?"*

It does not predict what a user will click, stream, or skip — it has no
behavioral data to learn from. Instead it takes an explicit taste profile
(preferred genre, mood, energy level, and acoustic feel) and scores every song
in the catalog against those stated preferences. The output is a ranked list of
the top-K songs most likely to feel right for that listener in that moment.

This system is designed for classroom exploration of recommender concepts, not
for deployment to real users.

---

## 3. How the Model Works

Imagine you walk into a record shop and hand the clerk a note that says:
*"I want something pop, upbeat, high energy, and not too acoustic."*
The clerk mentally scans every record in the store and assigns each one a
relevance score based on how well it matches your note. VibeMatch does exactly
that, automatically, for every song in the catalog.

Each song is scored on six criteria:

- **Genre match** — if the song's genre exactly matches your preference, it
  earns the largest single bonus. If it matches a related genre you listed as
  acceptable, it earns a smaller partial bonus.
- **Mood match** — if the song's mood matches your preferred mood (e.g., happy,
  chill, intense), it earns the second-largest bonus.
- **Energy closeness** — songs whose energy level is close to your target score
  higher than songs that are far away. A song at exactly your target energy
  earns full marks; a song at the opposite extreme earns nearly zero.
- **Valence closeness** — valence measures how bright or dark a song sounds.
  Songs closer to your preferred brightness score higher.
- **Acousticness closeness** — measures how produced vs. organic a song feels.
  Songs closer to your preference for acoustic or electronic sound score higher.

All five scores are added together to produce a total out of 6.5 points. Songs
are then sorted from highest to lowest, and the top results are returned with a
one-line explanation of why each was chosen.

---

## 4. Data Used

The catalog contains **20 songs** stored in `data/songs.csv`. Each song has
10 attributes: a numeric ID, title, artist, genre, mood, energy (0–1), tempo
in BPM, valence (0–1), danceability (0–1), and acousticness (0–1).

**Genres represented:** pop, lofi, rock, ambient, indie pop, synthwave, jazz
(8 distinct genres across 20 songs).

**Moods represented:** happy, chill, intense, moody, relaxed, focused
(6 distinct moods).

**Genre distribution (approximate):**
pop and lofi have 4 songs each; rock and ambient have 3 each; indie pop,
synthwave, and jazz have 2 each.

**What is missing:** The catalog contains no hip-hop, R&B, classical, country,
folk, electronic dance music, or metal. The 10 original songs were provided as
a starter dataset; 10 additional songs were manually added to improve coverage,
but the catalog still heavily skews toward lofi, pop, and ambient. All songs
are fictional with synthetic attribute values — they do not reflect any real
streaming platform's catalog or listening patterns.

---

## 5. Strengths

**Transparent reasoning.** Every recommendation comes with a plain-language
explanation ("Because it matches your favorite genre 'pop' and energy is very
close to your target"). Unlike black-box collaborative filtering models, every
point in the score can be traced back to a specific feature comparison.

**Works well for well-represented genres.** Users whose preferred genre has 3–4
catalog entries (pop, lofi, rock, ambient) receive recommendations that are
genuinely differentiated by secondary features like valence and acousticness.
For example, the High-Energy Pop and Chill Lofi profiles return completely
different song sets with zero overlap, even though they share no explicit
"avoid" rules.

**Related-genre fallback is plausible.** When a user's primary genre has few
catalog entries (jazz, synthwave), the `related_genres` partial credit
mechanism pulls in musically adjacent songs rather than random ones. The Late
Night Moody profile, for example, falls back to rock songs with moody mood and
high energy — which feels musically reasonable even though it was not explicitly
tuned.

**Robust to weight changes.** Extracting all weights into a single `WEIGHTS`
dictionary made sensitivity experiments easy and reversible. The scoring
function itself did not need to change to explore different tuning strategies.

---

## 6. Limitations and Bias

**Cross-genre contamination from continuous feature dominance.**
The scoring function has no hard genre filter — genre is just one more point
source competing on the same scale as energy, valence, and acousticness. When
the energy weight was doubled during the sensitivity experiment, pop songs like
*Gym Hero* (energy 0.93) and *Cardio Rush* (energy 0.95) started outscoring
rock songs like *Velvet Thunder* (energy 0.88) for a "Deep Intense Rock" user,
purely because their energy values were marginally closer to the target of 0.90.
A user who explicitly says "I want rock" can receive pop recommendations when a
continuous feature alignment overrides the categorical preference — which is
counterintuitive and likely to feel broken to a real user.

**Catalog-level filter bubble for minority genres.**
Genres with only two songs — jazz, synthwave, and indie pop — create a hard
ceiling on recommendation diversity. A jazz user will always see
*Coffee Shop Stories* and *Swing District* in their top results regardless of
mood or energy preferences, because no other songs can earn the genre match
bonus. This filter bubble is caused by uneven catalog coverage, not by the
algorithm itself, but it would worsen as the user pool grows while the catalog
stays fixed.

**Complete invisibility of unrepresented tastes.**
The catalog contains zero songs in hip-hop, R&B, classical, country, or
electronic dance music. Any user whose taste falls outside the eight genres
present will receive recommendations based entirely on continuous feature
proximity — meaning they get the "least wrong" songs rather than anything
genuinely relevant. The system has no mechanism to signal when it lacks
sufficient catalog coverage to serve a user well.

---

## 7. Evaluation Process

Five user profiles were tested against the 20-song catalog:

| Profile | Genre | Mood | Energy |
|---|---|---|---|
| High-Energy Pop | pop | happy | 0.90 |
| Chill Lofi | lofi | chill | 0.35 |
| Deep Intense Rock | rock | intense | 0.90 |
| Late Night Moody | synthwave | moody | 0.75 |
| Jazz Coffee Shop | jazz | relaxed | 0.40 |

For each profile the top 3 recommendations were inspected to check whether the
genre, mood, and energy of the returned songs matched what a real listener with
that taste would expect. All 10 profile pairs were also compared in
`reflection.md` to document how and why different profiles produce different
outputs.

A **sensitivity experiment** was run by doubling the energy weight (1.5 → 3.0)
and halving the genre weight (2.0 → 1.0) using the `WEIGHTS` dictionary in
`recommender.py`. Results were re-inspected under the new weights to observe
which rankings changed and why.

**What worked as expected:** High-Energy Pop and Chill Lofi returned completely
non-overlapping results — the catalog has enough pop and lofi songs to
differentiate by secondary features. Jazz Coffee Shop consistently surfaced its
two jazz songs at the top.

**What was surprising:** After the sensitivity experiment, pop songs crossed
into the Deep Intense Rock top-3 because their energy was marginally closer to
0.90 than the rock options. This revealed that the mood signal (intense vs.
happy) was not strong enough to act as a genre proxy when energy dominated.
Additionally, *Ember Roads* (rock, moody) appeared naturally in the Late Night
Moody results via `related_genres` — an unplanned but musically plausible
outcome.

---

## 8. Intended Use and Non-Intended Use

**Intended use:**
VibeMatch is designed for classroom exploration of content-based recommender
concepts. It is appropriate for learning how feature scoring, weight tuning,
and ranking logic work together to produce recommendations. It can also be used
as a starting point for experimenting with different weighting strategies or
catalog compositions.

**Not intended for:**
- Deployment to real users in a production music application
- Making recommendations based on listening history, implicit signals, or
  behavioral data (it has none)
- Genres, moods, or artists not represented in the 20-song catalog
- Drawing conclusions about fairness or representation in real-world music
  platforms, since the catalog and attribute values are synthetic

---

## 9. Ideas for Improvement

**1. Add a diversity penalty.**
The current system can return five nearly identical songs (e.g., five
pop/happy tracks) with no variety. A re-ranking step that penalizes songs too
similar to already-selected results — for example, reducing the score of any
song whose genre and mood exactly match a song already in the top-K — would
force the list to explore the catalog more broadly.

**2. Replace the single genre string with a genre affinity vector.**
Instead of exact match or related-genre partial credit, represent each user's
genre preferences as a weighted list: `{"pop": 1.0, "indie pop": 0.6,
"synthwave": 0.3}`. This would allow the scoring to reflect nuanced taste
("mostly pop but open to indie pop") rather than a binary in/out decision, and
would eliminate the sharp score cliff between exact and related matches.

**3. Expand the catalog and balance genre representation.**
The most impactful single change would be growing the catalog to 100+ songs
with at least 5 entries per genre, including genres currently missing (hip-hop,
R&B, classical, EDM). This alone would fix the minority-genre filter bubble,
give continuous features more room to differentiate within genres, and make the
system useful for a broader range of listener profiles.

---

## 10. Personal Reflection

**Biggest learning moment**
Doubling the energy weight during the sensitivity experiment caused pop songs to appear in a rock user's top results. That showed me there is no feature hierarchy — every feature competes on the same scale, and changing one weight shifts the entire ranking, not just one slot.

**How AI tools helped — and when I had to double-check**
AI was useful for design decisions like using squared distance and centralizing weights in a `WEIGHTS` dict. I still had to verify the math manually when scores changed — for example, confirming that `MAX_SCORE` propagated correctly from `recommender.py` to the progress bar in `main.py`. Specific predictions about song rankings also needed checking against the actual CSV.

**What surprised me about simple algorithms feeling like recommendations**
The output felt intentional almost immediately. Jazz Coffee Shop returned warm, slow, acoustic songs; High-Energy Pop returned bright, fast ones — and the contrast felt like the system had taste. It did not, it was arithmetic. That gap between what the code does and what it feels like to a human is what makes recommenders both compelling and worth scrutinizing.

**What I would try next**
Add a simple feedback loop — let the user mark a result as "liked" or "skipped" and nudge `target_energy` and `target_valence` slightly in response. That one change would make the recommender feel interactive and is a natural bridge toward understanding how real platforms learn from listening behavior.
