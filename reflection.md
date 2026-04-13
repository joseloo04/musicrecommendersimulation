[![Built with Claude](https://img.shields.io/badge/Built%20with-Claude%E2%84%A2-blueviolet?logo=anthropic&logoColor=white)](https://claude.ai/claude-code)

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

## 6. Limitations and Bias

1. **Catalog imbalance:** Genres like rock, metal, country, and folk each have only one 
song in the dataset. Users with these preferences receive one strong recommendation 
and then fall back to energy-based matches from completely different genres, making 
the system unreliable for minority genres.

2. **Genre weight dominance:** The genre match contributes +2.0 out of a maximum 5.0 
points (40% of the total score). This means a mediocre song in the right genre will 
almost always outrank an excellent song in the wrong genre, regardless of how well 
the other features match.

3. **Energy as a false proxy:** When no genre match exists, the system ranks songs 
purely by energy proximity. This caused EDM and hip-hop songs to appear in a rock 
user's top 5 simply because they share high energy values — a result that would feel 
wrong to a real user.

4. **No input validation (known bug, now fixed):** Out-of-range values for target_energy 
or target_acousticness (e.g. 1.4 or -0.2) previously produced negative proximity 
scores. The system now clamps all inputs to the valid 0.0–1.0 range.

5. **Conflicting preferences produce genre-biased results:** A user with a valid but 
conflicting profile (e.g. pop genre + sad mood) will always see genre-matched songs 
at the top even when those songs completely contradict the requested mood, because 
genre weight alone outweighs a mood match.

---

## 7. Evaluation  
## 7. Evaluation

I tested five user profiles against the 18-song catalog:

- **Pop/Happy** — system worked well, Sunrise City scored 4.97/5.0 as a near-perfect match
- **Chill Lofi** — strongest performance, found two high-scoring matches (4.96 and 4.90) 
  because the catalog has two lofi/chill songs
- **Intense Rock** — good #1 result but weak variety, songs #3-#5 were EDM and hip-hop 
  ranked purely on energy proximity
- **Adversarial (Pop/Sad/High Energy)** — genre weight dominated, sad mood only appeared 
  at #3 in a soul song despite being the stated preference
- **Adversarial (Classical/Out-of-range values)** — exposed a negative score bug from 
  invalid input, now fixed with input clamping

I also ran a weight experiment doubling energy importance and halving genre importance, 
which confirmed that genre weight is the primary driver of recommendation quality.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

# Reflection

## Profile Comparisons

**Pop/Happy vs Chill Lofi:**
Both profiles found strong #1 matches, but the lofi profile found two high-scoring 
results while pop only found one. This makes sense — the catalog has two lofi/chill 
songs and only one pop/happy song. The system is only as good as the diversity of 
the dataset behind it.

**Intense Rock vs High-Energy Pop:**
Both profiles want high energy, but their genre results are completely different. 
The rock profile's #2-#5 results were non-rock songs that only matched on energy, 
while the pop profile's #2 was still a pop song. This shows that catalog size per 
genre directly determines recommendation quality beyond the #1 result.

**Adversarial Pop/Sad vs Normal Pop/Happy:**
Changing only the mood from happy to sad completely broke the top results — the 
system kept recommending intense pop songs because genre weight (2.0) overpowered 
the mood signal. A real user asking for sad pop would be frustrated by these results.

**Weight Experiment (2x Energy, 0.5x Genre):**
Doubling energy made the system more vibe-aware but less genre-loyal. Rock fans 
started getting EDM recommendations. This taught me that weights are not just numbers 
— they represent a design decision about what the system thinks matters most to users.

## What I Learned

Building this recommender taught me that the hardest part of a recommendation system 
is not the math — it is deciding what the numbers should represent. Every weight is 
a assumption about human taste baked into the algorithm. Real platforms like Spotify 
solve this by learning weights from millions of users rather than hardcoding them, 
which is why their recommendations feel personal in a way mine cannot.
