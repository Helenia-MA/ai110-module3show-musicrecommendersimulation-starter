# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.
Example: **VibeFinder 1.0**
"EarWorm 1.0"
---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

It recommends a list of songs for a user based on their preference; solely uses content-based recommendation system.
In this case, genre carries the most weight, then mood matches and energy similarity and finally the acousticness of the song.
We've made a simple system mainly for classroom exploration; the user can only fill in one entry for each feature which doesn't really efficiently map out to how real-life systems work with people having maybe a range for energy and maybe ranked favorite genres and moods to allow for a more diverse and accurate recommendation system
---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

- The song features I used, in order of their weight, are: genre(+2), mood(+1), energy(closeness value) and acousticness(+0.5)
Similar user preferences are considered: favorite_genre, favorite_mood, target_energy and likes_acoustic; in order to be able to make the comparisons and calculate the song scores catered for each individual.
- Our model sums up all feature scores into a cumulative song score that we can then use in ranking to determine the ones to recommmend based on their values
- In the starter logic, I had included tempo, valence and danceability but realized in summing, their cumulative score led to a significant weight that could overpower genre match and mood in determining the scores.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

- there are now 18 songs in the catalog; there were originally 10 songs, I added 8 more
- The genres represented are: lofi, pop and one each for rock, ambient, jazz, indie pop, classical, edm, folk, r&b, metal, country, reggae
- the moods represented are: chill, happy, intense, and one each for relaxed, moody, focused, aggressive, melancholy, energetic, nostalgic, romantic, dark, uplifting, carefree
- some musical tastes missing include maybe language, and instrumental vs vocal preference

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

The strength of the system is found when a user's genre and mood both exist in the catalog, the 2.0 genre weight reliably dominates and the recommended songs are thus reliable too.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

**Genre-representation filter bubble.** The biggest weakness I found is that the
2.0 genre weight rewards users whose taste is well-represented in the catalog
and quietly ignores everyone else. Of the 18 songs, `lofi` has 3 and `pop` has 2, while the other 13 genres have exactly one song each; so the Chill Lofi
user got three genuine lofi matches in their top 5, but any fan of a niche genre can receive at most a single on-genre song before the list falls back to tracks that have nothing to do with their stated taste. In the "Rock lover who wants calm" run, showed this clearly: after the one rock song at #1, positions 2–5 were filled with classical, ambient, and lofi tracks chosen purely by the energy gap.
The way we calculate the energy gap compounds the problem, where `1 - |song - target|` gives mid-energy songs (0.4–0.6) a high score for almost every user, so the same "safe" middle-of-the-road tracks keep surfacing as filler regardless of what the user actually asked for.
Our system serves majority-genre and moderate-energy listeners well, and pushes minority-taste and extreme-energy users toward a homogenized set of recommendations.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

I built a small evaluation harness in `src/main.py` that runs the recommender
against seven profiles and prints the top-5 songs plus a scoring breakdown for
each. Three are realistic listeners; four are deliberately "adversarial" edge
cases meant to try to trick the scoring logic. (Reminder: the recipe is
`2.0*genre + 1.0*mood + 1.0*energy_closeness + 0.5*acoustic`, so the maximum
possible score is 4.5.)

### Normal profiles

| Profile | Top result | Score | Behaved as expected? |
| --- | --- | --- | --- |
| High-Energy Pop (pop / happy / 0.9) | Sunrise City | 4.42 | ✅ Perfect genre+mood+acoustic match, only docked on energy. |
| Chill Lofi (lofi / chill / 0.35, acoustic) | Library Rain | 4.50 | ✅ Hit the maximum possible score. |
| Deep Intense Rock (rock / intense / 0.9) | Storm Runner | 4.49 | ✅ Clear winner; the only rock+intense track. |

For all three, the intended "obvious" song rose to the top and the explanations
matched intuition.

### Adversarial / edge case profiles — what I looked for and what surprised me

1. **Conflicting energy + mood** (`energy 0.9`, `mood "sad"`). "sad" isn't a
   mood in the catalog, so the mood term never fires. The scorer gracefully
   fell back to genre + energy, ranking high-energy pop (Gym Hero, 3.47) on top.
   No crash, the conflicting preference was simply ignored rather
   than reconciled.

2. **Nonexistent genre** (`polka`). The 2.0 genre weight never fires, so the
   ceiling drops to 2.5 and ranking is decided by mood + energy + acoustic
   (Rooftop Lights, 2.24). Reasonable fallback, no error.

3. **Neutral / empty preferences** (`genre=""`, `mood=""`, `energy 0.5`).
   Ranking collapses to energy-closeness + acoustic only. This exposed the
   **tie-break behavior**: Island Time and Velvet Hours both scored 1.48, and
   the sort broke the tie alphabetically by title (Island before Velvet).

4. **Rock lover who wants calm** (`rock/intense` but `energy 0.0`, acoustic).
   Genre+mood (3.0) still beat the huge energy penalty: Storm Runner won at 3.09
   despite an energy closeness of only +0.09 and *no* acoustic match (it's a
   loud rock song). This confirms genre/mood can overpower a badly mismatched
   energy target — the system "overfits" to the categorical match.

### Takeaways

- The scorer is **robust to missing/unknown values** (unknown genre, mood, or
  empty strings) — it degrades gracefully instead of erroring.
- Ties are resolved deterministically (alphabetical by title), which is
  predictable but arbitrary from a user's perspective.

### Terminal output (top 5 per profile)

Produced by running `python3 -m src.main`.

**Normal — High-Energy Pop**

```
PROFILE: High-Energy Pop
  prefs: genre='pop', mood='happy', target_energy=0.9, likes_acoustic=False
----------------------------------------------------------------------
  1. Sunrise City           [pop/happy, energy=0.82]  score=4.42
       reason: genre match (+2.0); mood match (+1.0); energy closeness (+0.92); acoustic match (+0.5)
  2. Gym Hero               [pop/intense, energy=0.93]  score=3.47
       reason: genre match (+2.0); energy closeness (+0.97); acoustic match (+0.5)
  3. Rooftop Lights         [indie pop/happy, energy=0.76]  score=2.36
       reason: mood match (+1.0); energy closeness (+0.86); acoustic match (+0.5)
  4. Storm Runner           [rock/intense, energy=0.91]  score=1.49
       reason: energy closeness (+0.99); acoustic match (+0.5)
  5. Pulse Reactor          [edm/energetic, energy=0.95]  score=1.45
       reason: energy closeness (+0.95); acoustic match (+0.5)
```

**Normal — Chill Lofi**

```
PROFILE: Chill Lofi
  prefs: genre='lofi', mood='chill', target_energy=0.35, likes_acoustic=True
----------------------------------------------------------------------
  1. Library Rain           [lofi/chill, energy=0.35]  score=4.50
       reason: genre match (+2.0); mood match (+1.0); energy closeness (+1.00); acoustic match (+0.5)
  2. Midnight Coding        [lofi/chill, energy=0.42]  score=4.43
       reason: genre match (+2.0); mood match (+1.0); energy closeness (+0.93); acoustic match (+0.5)
  3. Focus Flow             [lofi/focused, energy=0.4]  score=3.45
       reason: genre match (+2.0); energy closeness (+0.95); acoustic match (+0.5)
  4. Spacewalk Thoughts     [ambient/chill, energy=0.28]  score=2.43
       reason: mood match (+1.0); energy closeness (+0.93); acoustic match (+0.5)
  5. Coffee Shop Stories    [jazz/relaxed, energy=0.37]  score=1.48
       reason: energy closeness (+0.98); acoustic match (+0.5)
```

**Normal — Deep Intense Rock**

```
PROFILE: Deep Intense Rock
  prefs: genre='rock', mood='intense', target_energy=0.9, likes_acoustic=False
----------------------------------------------------------------------
  1. Storm Runner           [rock/intense, energy=0.91]  score=4.49
       reason: genre match (+2.0); mood match (+1.0); energy closeness (+0.99); acoustic match (+0.5)
  2. Gym Hero               [pop/intense, energy=0.93]  score=2.47
       reason: mood match (+1.0); energy closeness (+0.97); acoustic match (+0.5)
  3. Pulse Reactor          [edm/energetic, energy=0.95]  score=1.45
       reason: energy closeness (+0.95); acoustic match (+0.5)
  4. Iron Lungs             [metal/dark, energy=0.97]  score=1.43
       reason: energy closeness (+0.93); acoustic match (+0.5)
  5. Sunrise City           [pop/happy, energy=0.82]  score=1.42
       reason: energy closeness (+0.92); acoustic match (+0.5)
```

**Adversarial — Conflicted (energy 0.9 + sad)**

```
PROFILE: Conflicted (energy 0.9 + sad)
  prefs: genre='pop', mood='sad', target_energy=0.9, likes_acoustic=False
----------------------------------------------------------------------
  1. Gym Hero               [pop/intense, energy=0.93]  score=3.47
       reason: genre match (+2.0); energy closeness (+0.97); acoustic match (+0.5)
  2. Sunrise City           [pop/happy, energy=0.82]  score=3.42
       reason: genre match (+2.0); energy closeness (+0.92); acoustic match (+0.5)
  3. Storm Runner           [rock/intense, energy=0.91]  score=1.49
       reason: energy closeness (+0.99); acoustic match (+0.5)
  4. Pulse Reactor          [edm/energetic, energy=0.95]  score=1.45
       reason: energy closeness (+0.95); acoustic match (+0.5)
  5. Iron Lungs             [metal/dark, energy=0.97]  score=1.43
       reason: energy closeness (+0.93); acoustic match (+0.5)
```

**Adversarial — Nonexistent genre (polka)**

```
PROFILE: Nonexistent genre (polka)
  prefs: genre='polka', mood='happy', target_energy=0.5, likes_acoustic=False
----------------------------------------------------------------------
  1. Rooftop Lights         [indie pop/happy, energy=0.76]  score=2.24
       reason: mood match (+1.0); energy closeness (+0.74); acoustic match (+0.5)
  2. Sunrise City           [pop/happy, energy=0.82]  score=2.18
       reason: mood match (+1.0); energy closeness (+0.68); acoustic match (+0.5)
  3. Island Time            [reggae/carefree, energy=0.52]  score=1.48
       reason: energy closeness (+0.98); acoustic match (+0.5)
  4. Velvet Hours           [r&b/romantic, energy=0.48]  score=1.48
       reason: energy closeness (+0.98); acoustic match (+0.5)
  5. Night Drive Loop       [synthwave/moody, energy=0.75]  score=1.25
       reason: energy closeness (+0.75); acoustic match (+0.5)
```

**Adversarial — Neutral / empty prefs**

```
PROFILE: Neutral / empty prefs
  prefs: genre='', mood='', target_energy=0.5, likes_acoustic=False
----------------------------------------------------------------------
  1. Island Time            [reggae/carefree, energy=0.52]  score=1.48
       reason: energy closeness (+0.98); acoustic match (+0.5)
  2. Velvet Hours           [r&b/romantic, energy=0.48]  score=1.48
       reason: energy closeness (+0.98); acoustic match (+0.5)
  3. Night Drive Loop       [synthwave/moody, energy=0.75]  score=1.25
       reason: energy closeness (+0.75); acoustic match (+0.5)
  4. Rooftop Lights         [indie pop/happy, energy=0.76]  score=1.24
       reason: energy closeness (+0.74); acoustic match (+0.5)
  5. Concrete Jungle        [hip hop/aggressive, energy=0.8]  score=1.20
       reason: energy closeness (+0.70); acoustic match (+0.5)
```

**Adversarial — Rock lover who wants calm (energy 0.0)**

```
PROFILE: Rock lover who wants calm (energy 0.0)
  prefs: genre='rock', mood='intense', target_energy=0.0, likes_acoustic=True
----------------------------------------------------------------------
  1. Storm Runner           [rock/intense, energy=0.91]  score=3.09
       reason: genre match (+2.0); mood match (+1.0); energy closeness (+0.09)
  2. Moonlit Reverie        [classical/melancholy, energy=0.25]  score=1.25
       reason: energy closeness (+0.75); acoustic match (+0.5)
  3. Spacewalk Thoughts     [ambient/chill, energy=0.28]  score=1.22
       reason: energy closeness (+0.72); acoustic match (+0.5)
  4. Library Rain           [lofi/chill, energy=0.35]  score=1.15
       reason: energy closeness (+0.65); acoustic match (+0.5)
  5. Coffee Shop Stories    [jazz/relaxed, energy=0.37]  score=1.13
       reason: energy closeness (+0.63); acoustic match (+0.5)
```

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

I would add more entries for user preferences, such as ranked genre/mood pref rather than just one and the preferred energy as a range rather than a specific value. This would help in curating a better recommendation system for the user.
Collecting data for more users and making comparisons could also help in incorporating collaborative system for a more diverse but reliable recommendation system
We can also include logic that takes user feedback such as likes or skips and adjusts the feature weights accordingly
---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps

I learnt that some features tend to weigh more and determine recommended songs a bit more compared to others and that the recommendation system is a dynamic one, that is highly dependent on the feedback loop for it to work well. I also learnt that the data available plays a huge role in the recommendations algorithm and may create biases depending on what is mostly represented and what isn't
