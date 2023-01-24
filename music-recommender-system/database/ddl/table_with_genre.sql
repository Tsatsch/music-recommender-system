-- not used, dropped
CREATE TABLE music_plus_genre (
    id varchar NOT NULL,
    danceability FLOAT,
    energy FLOAT,
    loudness FLOAT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    mode FLOAT,
    key INT,
    duration_ms INT,
    popularity INT,
    genre varchar,
    PRIMARY KEY (id)
);