# Profile Comparison Reflections

Observations on how each pair of user profiles produces different outputs,
and why those differences make sense given the scoring logic.

---

## 1. High-Energy Pop vs. Chill Lofi

These two profiles sit at opposite ends of every feature dimension, making
them the clearest test of whether the scoring function separates contrasting
tastes correctly.

High-Energy Pop targets genre=pop, mood=happy, energy=0.90, acousticness=0.10.
Chill Lofi targets genre=lofi, mood=chill, energy=0.35, acousticness=0.80.

Their top results share zero songs, which is exactly right. High-Energy Pop
surfaces Gym Hero, Cardio Rush, and Sunrise City — all produced, fast, and
bright. Chill Lofi surfaces Library Rain, Midnight Coding, and Deep Study —
all acoustic, slow, and calm. The energy gap alone (0.90 vs 0.35) is wide
enough that even without genre matching, the two profiles would land in
completely different parts of the catalog. This pair confirms that the
continuous energy feature is doing meaningful work as a separator, not just
the categorical genre bonus.

---

## 2. High-Energy Pop vs. Deep Intense Rock

This is the most instructive comparison because both profiles target the same
energy level (0.90) but differ on genre (pop vs rock), mood (happy vs
intense), valence (0.82 vs 0.45), and acousticness (0.10 vs 0.10).

At baseline weights, genre dominated: pop songs stayed in the pop list and
rock songs stayed in the rock list. After the sensitivity experiment (energy
doubled, genre halved), Gym Hero and Cardio Rush began appearing in the Deep
Intense Rock results — both are pop/intense with energy 0.93 and 0.95, which
is marginally closer to 0.90 than Storm Runner (0.91). This revealed that
mood=intense carries meaningful weight for the rock profile, but it is not
enough to fully counteract a very large energy advantage when weights shift.
The key lesson: valence (0.82 pop vs 0.45 rock) is the feature that most
cleanly separates these two profiles, but it only carries 0.5 weight — too
low to act as a reliable genre proxy when energy is dominant.

---

## 3. Chill Lofi vs. Jazz Coffee Shop

Both profiles target low energy and high acousticness, making this a test of
whether the mood and genre signals can distinguish two "quiet" listener types.

Chill Lofi: genre=lofi, mood=chill, energy=0.35, acousticness=0.80.
Jazz Coffee Shop: genre=jazz, mood=relaxed, energy=0.40, acousticness=0.87.

Their energy targets are only 0.05 apart, so the continuous features alone
would not separate them well. Genre and mood do the heavy lifting: lofi songs
cluster around chill/focused moods, while jazz songs sit in relaxed territory.
The Jazz Coffee Shop profile always returns Coffee Shop Stories and Swing
District at the top (the only two jazz songs), then pulls in lofi and ambient
songs via related_genres. Chill Lofi does the reverse — lofi songs first, then
ambient and jazz as fallbacks. The overlap in their fallback results (both
pulling from ambient/jazz/lofi) illustrates that acousticness-heavy profiles
collapse into a shared "quiet music" pool once the exact genre matches are
exhausted. This is a mild filter bubble: two different listener types end up
seeing the same songs once the top 2 catalog slots are filled.

---

## 4. Deep Intense Rock vs. Late Night Moody

Both profiles are dark and non-acoustic, but differ in energy level and genre.
Deep Intense Rock targets energy=0.90 and mood=intense. Late Night Moody
targets energy=0.75 and mood=moody, with genre=synthwave.

The rock profile returns high-energy songs (Storm Runner 0.91, Velvet Thunder
0.88, Ember Roads 0.84) that feel aggressive and raw. The moody profile
returns Night Drive Loop and Neon Heartbeat (the two synthwave songs), then
pulls in rock songs via related_genres — Ember Roads (rock, moody, energy
0.84) ranks highly because it matches both the mood and the energy target
closely. The shared appearance of Ember Roads in both profiles makes sense:
it is a rock song with a moody mood and medium-high energy, sitting at the
intersection of both taste profiles. This demonstrates the related_genres
mechanism working correctly — it bridges genres that share sonic character
rather than randomly pulling unrelated songs.

---

## 5. Late Night Moody vs. Jazz Coffee Shop

This is the sharpest contrast in the set: one profile is electronic, dark,
and medium-high energy; the other is acoustic, warm, and low energy.

Late Night Moody (synthwave, moody, energy=0.75, acousticness=0.18) and Jazz
Coffee Shop (jazz, relaxed, energy=0.40, acousticness=0.87) share no songs in
their top 3 and no related_genres overlap. The energy gap (0.75 vs 0.40) and
acousticness gap (0.18 vs 0.87) are both large enough that even if genre
matching failed for both, the continuous features would push their results in
opposite directions. This pair is the best evidence that the three continuous
features (energy, valence, acousticness) form a meaningful "taste space" —
profiles that are far apart in that space receive genuinely different
recommendations even when the categorical genre signals are weak.
