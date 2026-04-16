# Reflection

## What I Learned About Recommenders

Building VibeFinder showed that every weight in the scoring function is a judgment call that encodes a specific theory of musical preference. Setting genre as the dominant signal assumes "what kind of music" always matters more than "how does this music feel," which is wrong for users who browse by mood or activity rather than genre.

Bias through omission was the second major insight, since a catalog with only one classical and one country song will produce worse recommendations for fans of those genres. This is exactly how bias appears in real AI systems: not as malicious intent, but as the accumulated effect of whose tastes were represented when the data was collected.

---

## Profile Comparison Notes

**Pop / Happy vs. High-Energy Rock**
Both profiles share a high energy target, so songs like Gym Hero and Night Drive Loop appeared in both top-5 lists. Genre weight at 2.0 was the primary differentiator, confirming that the genre anchor drives separation between otherwise similar profiles.

**High-Energy Rock vs. Chill Lofi**
This pair produced the starkest contrast, with rock and lofi top results sharing almost no attributes across genre, mood, or energy. The acoustic bonus visibly boosted the lofi profile's results, pulling acoustic tracks above synthwave and ambient tracks that had similar energy scores.

Rooftop Lights ranked 3rd for the pop profile despite having an energy level closer to the lofi target than most pop songs. This shows the genre weight correctly suppressing an energy match, ensuring pop fans and lofi fans receive meaningfully different recommendations.
