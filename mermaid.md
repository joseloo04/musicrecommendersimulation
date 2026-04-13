flowchart TD
    A([UserProfile\nfavorite_genre · favorite_mood\ntarget_energy · target_acousticness]) --> C
    B([songs.csv catalog]) --> C

    C[Load all songs] --> D[Initialize scored_songs = empty list]
    D --> E[Pick next song from catalog]

    E --> F{song.genre ==\nuser.favorite_genre?}
    F -- Yes --> G[score += 2.0]
    F -- No  --> H[score += 0.0]
    G --> I{song.mood ==\nuser.favorite_mood?}
    H --> I

    I -- Yes --> J[score += 1.5]
    I -- No  --> K[score += 0.0]
    J --> L[score += 1.0 × (1 − |song.energy − target_energy|)]
    K --> L

    L --> M[score += 0.5 × (1 − |song.acousticness − target_acousticness|)]
    M --> N[Append song + score to scored_songs]

    N --> O{More songs\nin catalog?}
    O -- Yes --> E
    O -- No  --> P[Sort scored_songs by score descending]

    P --> Q[Return top-K songs]
    Q --> R([Recommendations])
