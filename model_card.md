# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests the top 5 songs from a 20-song catalog that best match a user's stated taste preferences. It is designed for classroom exploration of how content-based recommendation systems work — not for production use with real users.

The system assumes the user can describe their taste in four concrete dimensions: preferred genre, preferred mood, a target energy level (0.0 = very calm, 1.0 = very intense), and whether they prefer acoustic or electronic instrumentation. It makes no attempt to learn from listening history or implicit feedback.

---

## 3. How the Model Works

Imagine you are a music journalist who has to recommend songs to a friend. You know your friend likes pop, happy vibes, and high-energy tracks. For every song in your collection, you mentally check: does the genre match? does the mood match? how close is the energy to what they like? You add points for each hit and then hand over the songs with the highest totals.

VibeFinder works the same way. For each song in the catalog, it awards:
- 2 points if the genre matches the user's preference (genre is the strongest signal)
- 1 point if the mood matches
- Between 0 and 1 points based on how close the song's energy is to the user's target (a perfect match gives the full 1 point)
- A bonus 0.5 points if the user likes acoustic music and the song is heavily acoustic

After scoring every song, it sorts the list from highest to lowest and returns the top 5. Each result comes with a plain-English reason (e.g., "genre match (+2.0); energy score (+0.98)") so the recommendation is explainable.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. The starter dataset had 10 songs; 10 more were added to improve genre and mood diversity.

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, edm, country, acoustic folk, classical, hip-hop, r&b

**Moods represented:** happy, chill, intense, relaxed, focused, moody, energetic, nostalgic, sad, romantic

Each song has 10 attributes: id, title, artist, genre, mood, energy (0.0–1.0), tempo_bpm, valence (0.0–1.0), danceability (0.0–1.0), and acousticness (0.0–1.0). The current scoring function uses genre, mood, energy, and acousticness. Valence, danceability, and tempo_bpm are stored but not yet used in scoring.

The catalog skews slightly toward Western popular music styles. Classical, country, and acoustic folk each have only 1–2 songs, which limits what the system can recommend to users who prefer those genres.

---

## 5. Strengths

- **Transparency:** Every recommendation comes with a specific, human-readable reason, so the system never feels like a black box.
- **Genre-coherent results:** Because genre carries the highest weight (2.0), users almost always see their preferred genre at the top of the list, which matches most people's intuition about music discovery.
- **Acoustic preference detection:** The acoustic bonus correctly surfaces acoustic and folk tracks for users who prefer unplugged sounds, even when those tracks don't perfectly match on genre.
- **Works well for well-represented genres:** The lofi/chill profile produced results that felt spot-on — Library Rain and Midnight Coding both genuinely sound like what a lofi study playlist would contain.

---

## 6. Limitations and Bias

**Genre over-matching:** The genre weight of 2.0 is strong enough that a mediocre genre match (e.g., energy and mood are wrong) will almost always outscore a nearly perfect match in a different genre. A pop fan listening in a sad mood will still get happy pop songs because the mood weight (1.0) can't overcome the genre bonus.

**Pop-heavy dataset:** The original 10-song starter catalog had 3 songs that could be classified as pop or indie pop (30%). Even after expansion, pop-adjacent genres still have more catalog entries than genres like classical or country, which each have only one song. A classical music fan gets exactly one classical recommendation and then irrelevant results.

**Binary genre matching:** "Indie pop" and "pop" are treated as entirely different genres. A pop fan would likely enjoy both, but the system scores them as no match.

**No sub-genre or tempo awareness:** Two rock songs — one at 90 BPM (classic rock) and one at 170 BPM (metal) — look identical to this system. Tempo is stored in the CSV but not used in scoring.

**Static weights for all users:** The scoring weights are hard-coded. A user who cares deeply about mood but not genre gets the same scoring formula as everyone else. Real systems learn personalized weights from behavior.

---

## 7. Evaluation

Three user profiles were tested by running the CLI and inspecting whether the top 5 results matched musical intuition:

**Pop / Happy (energy=0.8, likes_acoustic=False)**
- Sunrise City correctly ranked first (pop + happy + high energy). Results felt accurate.
- Gym Hero ranked second despite being "intense" mood — the genre weight alone elevated it above non-pop songs with matching moods.

**High-Energy Rock (energy=0.9, likes_acoustic=False)**
- Storm Runner correctly ranked first (rock + intense + energy=0.91). The match was nearly perfect.
- Fade to Black ranked second as the only other rock song, even though its mood (sad) and energy (0.72) are quite different from the target. This exposed the "only one option per genre" problem.

**Chill Lofi (energy=0.35, likes_acoustic=True)**
- Library Rain and Midnight Coding ranked 1st and 2nd — both are exactly what a lofi study playlist listener would want. This was the most satisfying result.
- Focus Flow ranked 3rd despite being "focused" mood rather than "chill" — the genre + acoustic bonus compensated for the mood miss.

**Surprising finding:** The energy proximity score never exceeded 1.0, which means no song can score above 4.5 total (2.0 + 1.0 + 1.0 + 0.5). Songs with a perfect genre + mood + energy + acoustic match are indistinguishable from one another in score. This means tie-breaking is effectively random (dictionary order from the CSV), which could matter in a larger catalog.

---

## 8. Future Work

- **Use valence and danceability in scoring:** These are stored in the CSV but currently ignored. A user who wants danceable music could benefit from a danceability weight.
- **Fuzzy genre matching:** Treat "indie pop" as a partial match for "pop" using a genre similarity map, rather than binary match/no-match.
- **Diversity injection:** The current system can return 5 near-identical songs if the catalog has many entries in one genre. A diversity penalty could ensure the top 5 span at least 2 genres.
- **Learned weights:** Instead of hard-coded weights, allow the user to rate recommendations and adjust weights based on what they liked or skipped.
- **Expanded catalog:** 20 songs is too small for meaningful variety. A real evaluation would need at least 500–1000 songs across all represented genres.

---

## 9. Personal Reflection

The most surprising thing about building VibeFinder was how much the weighting decisions felt like value judgments rather than technical choices. Setting genre to 2.0 points is essentially saying "genre is twice as important as mood" — but that's not obviously true for everyone. Some people discover music by mood (study playlists, workout playlists) without caring about genre at all. The weights I chose reflect one particular model of how music preference works, and that model is baked invisibly into every recommendation the system produces.

Building this also changed how I think about Spotify's Discover Weekly. What seemed like magic — the system somehow knowing what I'd like — now looks more like a very large version of this: hundreds of audio features, millions of users, and carefully tuned weights. The difference is that Spotify's weights are learned from billions of listening events, so they adapt to individual behavior instead of applying a one-size-fits-all formula. The core idea, though, is exactly what VibeFinder does: score each candidate against a model of what the user likes, then rank.
