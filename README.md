# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

In this recommendation system,  the song features I used, in order of their weight, are: genre(+2), mood(+1), energy(closeness value) and acousticness(+0.5)
Similar user preferences are considered: favorite_genre, favorite_mood, target_energy and likes_acoustic; in order to be able to make the comparisons and calculate the song scores catered for each individual.
- Our model sums up all feature scores into a cumulative song score that we can then use in ranking to determine the ones to recommmend based on their values
- Since genre is usually a big factor to consider while recommending, the system works well by applying the largest weight for it but not too much for it to overshadow the other features.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

- Real-world recommender systems work by utilizing a hybrid of the recommendation systems to curate a list of recommended items for a given user. Since they have a lot of data gathered it is easier to cross check and find users with similar interests or a specific user's tastes to use as inputs for the recommendation systems.

- In our case, I'll focus more on content-based system since we are currently working with data for an individual user.
* User profile stores: favorite_genre, favorite_mood, target_energy, likes_acoustic
  * for the song's energy feature, the formula I'll use for a scoring value is:
    closeness = 1 - |song_energy - target_energy| to get a [0,1] scale
  * for the categorical data, we'll weigh genre above mood thus the weights we'll use is +2.0 in the score for every matching genre and +1.0 for every matching mood
  * for acousticness, I'll convert the song's value to boolean based on whether it's greater than the threshold 0.5. then have +0.5 for matching acousticness
  * For ranking, I'd then sort the songs in descending order based off their scores, filter out the heard songs and use alphabetical order to break a tie and recommend the first n songs.
  (2.0(genre) + 1.0(mood) + 1.0(energy) + 0.5(acoustic))

  Potential biases: the system may over prioritize genre making it highly possible for a song with matching mood and similar energy but different genre to get buried
  the acoustic cutoff point renders similar songs one with say 0.49 and another 0.51 in different categories making one earn +0.5 points while the other doesn't.

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

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# Loaded songs: 18
User profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False

Top recommendations:

1. Sunrise City - Score: 4.48
Reason: genre match (+2.0); mood match (+1.0); energy closeness (+0.98); acoustic match (+0.5)

2. Gym Hero - Score: 3.37
Reason: genre match (+2.0); energy closeness (+0.87); acoustic match (+0.5)

3. Rooftop Lights - Score: 2.46
Reason: mood match (+1.0); energy closeness (+0.96); acoustic match (+0.5)

4. Concrete Jungle - Score: 1.50
Reason: energy closeness (+1.00); acoustic match (+0.5)

5. Night Drive Loop - Score: 1.45
Reason: energy closeness (+0.95); acoustic match (+0.5)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---
when I change the weight from 2.0 to 0.5, more genre variety surfaces in the recommended list. However, while it increases diversity, since genre is usually a huge factor in a user's preferences, the recommended list isn't necessarily better or more attuned to what one would love in real-life

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---
it over favors represented genres and moods.

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
I learnt that some features tend to weigh more and determine recommended songs a bit more compared to others and that the recommendation system is a dynamic one, that is highly dependent on the feedback loop for it to work well. I also learnt that the data available plays a huge role in the recommendations algorithm and may create biases depending on what is mostly represented and what isn't
