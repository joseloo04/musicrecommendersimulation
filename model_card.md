# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **Waripolo Vicencio 2.2**  

---

## 2. Goal / Task
VibeMatch picks the top 5 songs from an 18-song catalog based on a user's
preferred genre, mood, energy level, and acousticness. Built for a classroom
project — not production.

## 3. Data Used
- 18 songs in `data/songs.csv`
- 10 features per song: id, title, artist, genre, mood, energy, tempo_bpm,
  valence, danceability, acousticness
- 15 genres: pop, lofi, rock, metal, classical, EDM, jazz, folk, soul, and more
- I expanded the original 10-song dataset to 18 for more variety
- Most genres have only 1 song; lofi and pop each have 2

## 4. Algorithm Summary
Every song gets a score against the user profile:

- +2.0 if genre matches
- +1.5 if mood matches
- Up to +1.0 based on energy closeness (exact match = full point)
- Up to +0.5 based on acousticness closeness

Max score is 5.0. Top 5 get returned.

## 5. Observed Behavior and Biases

- **Genre dominance:** Genre is 40% of the total score. A mediocre song in
  the right genre will almost always beat a great song in the wrong one.
- **Catalog imbalance:** Rock, metal, country, and folk each have one song.
  After the #1 match, the system falls back to energy similarity from
  completely different genres.
- **Energy as false proxy:** A rock user got EDM and hip-hop in their top 5
  because those songs happen to be high energy. Sounds nothing like rock.
- **Conflicting preferences break down:** A pop/sad user kept getting intense
  pop songs because the genre weight drowned out the mood signal.
- **Input validation bug (fixed):** Values like energy: 1.4 used to produce
  negative scores. Fixed with clamping to 0.0–1.0.

## 6. Evaluation Process
I tested five profiles:

- Pop/Happy — Sunrise City scored 4.97/5.0, worked well
- Chill Lofi — best results, two songs scored above 4.90
- Intense Rock — strong #1, but positions #2-#5 were unrelated genres
- Adversarial Pop/Sad — genre kept winning over mood
- Adversarial Classical/Out-of-range — broke the scoring, exposed the bug

I also ran one experiment: doubled energy weight, halved genre weight.
The rock user started getting EDM. That told me weights are not neutral
math — they're decisions about what the system thinks matters.

## 7. Intended and Non-Intended Use

**Use it for:**
- Learning how content-based filtering works
- Exploring how scoring weights affect bias and variety

**Don't use it for:**
- Actual music recommendations
- Any catalog larger than a toy dataset
- Replacing Spotify

## 8. Ideas for Improvement
1. Learn weights from user feedback instead of hardcoding them
2. At least 5 songs per genre so minority-genre users get real variety
3. Add collaborative filtering — what did similar users actually enjoy

## 9. Personal Reflection

The weight experiment was the moment things clicked. I doubled energy,
halved genre, and suddenly a rock user was getting EDM recommendations.
That's when I realized every number in a scoring function is a hidden
assumption. Spotify doesn't hardcode those assumptions — it learns them
from billions of plays, which is why it feels personal in a way mine can't.

Copilot was useful for the boring parts: CSV loading, terminal formatting,
docstrings. But it burned me once. It generated a user profile with keys
like `"genre"` instead of `"favorite_genre"`, which is what `score_song`
actually checks. No error, no crash — just silently wrong results. That's
the part nobody warns you about: AI-generated code can be syntactically
fine and semantically broken at the same time.

The thing that genuinely surprised me was how satisfying it felt to see
Sunrise City hit 4.97/5.0. I knew exactly why it happened. The math is
right there. And it still felt like the system "got it right." I think
that's the trick behind all recommendation systems — the output feels
personal even when the process is completely mechanical.

If I kept building this, I'd add a thumbs up/down loop so the weights
could adjust over time. That's the gap between a rule-based system and
something that actually learns.