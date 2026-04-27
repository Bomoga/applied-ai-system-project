# Reflection

## What I Learned About Recommenders

Building TuneMatch showed that every weight in the scoring function is a judgment call that encodes a specific theory of musical preference. Setting genre as the dominant signal assumes "what kind of music" always matters more than "how does this music feel", which is wrong for users who browse by mood or activity rather than genre.

Bias through omission was the second major insight, since a catalog with only one classical and one country song will produce worse recommendations for fans of those genres. This is exactly how bias appears in real AI systems: not as malicious intent, but as the accumulated effect of whose tastes were represented when the data was collected.

---

## Profile Comparison Notes

**Pop / Happy vs. High-Energy Rock**
Both profiles share a high energy target, so songs like Gym Hero and Night Drive Loop appeared in both top-5 lists. Genre weight at 2.0 was the primary differentiator, confirming that the genre anchor drives separation between otherwise similar profiles.

**High-Energy Rock vs. Chill Lofi**
This pair produced the starkest contrast, with rock and lofi top results sharing almost no attributes across genre, mood, or energy. The acoustic bonus visibly boosted the lofi profile's results, pulling acoustic tracks above synthwave and ambient tracks that had similar energy scores.

Rooftop Lights ranked 3rd for the pop profile despite having an energy level closer to the lofi target than most pop songs. This shows the genre weight correctly suppressing an energy match, ensuring pop fans and lofi fans receive meaningfully different recommendations.

---

## Responsible AI Reflection

### Limitations and Biases in TuneMatch

The scoring weights were chosen by hand and encode my own theory of musical preference — that genre matters most, then mood, then energy — which is simply wrong for listeners who browse by activity or mood rather than genre. Catalog representation is also uneven: classical, country, and acoustic folk each have only one or two entries, so users who prefer those genres receive structurally worse recommendations regardless of how well the algorithm works.

---

### Could TuneMatch Be Misused?

Scaled to a real platform, the pop-heavy catalog bias would suppress exposure for independent or non-mainstream artists — concentrating streams and revenue among already-dominant genres regardless of quality. If the scoring weights were public, a label could also game rankings by keyword-stuffing song metadata to match high-weight attributes; the safeguard is regular catalog audits and per-user personalization so no single static formula can be exploited universally.

---

### What Surprised Me While Testing

All 38 tests passed and the scoring logic was correct, yet a "jazz/intense/electronic" profile would produce confidently wrong results with no signal to the user — because the catalog has no high-energy jazz songs and the system has no way to flag that it is operating outside its coverage. Testing against profiles that matched the weight assumptions made the system look excellent; testing against underrepresented profiles revealed that "tests pass" and "reliable recommendations" are not the same thing.

---

### Collaboration with AI

**Helpful:** When I originally wrote `score()` as a single function returning a float, Claude suggested having the scorer return both a numeric score and a list of which rules fired — that one change made the explainer essentially free to implement and is why results say "Matched: genre, mood, energy, acoustic" instead of just printing a number.

**Flawed:** For the energy proximity formula, Claude initially suggested `score = 1 - abs(target - song_energy)`, which can return negative values if either input is unclamped; the correct version is `max(0.0, 1 - abs(target - song_energy))`, but Claude only caught the issue after I pushed back and asked what would happen with out-of-range inputs.
