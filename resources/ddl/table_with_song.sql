-- not used, dropped
CREATE TABLE songsspot (
    id varchar NOT NULL,
    song varchar,
    artist varchar,
    danceability FLOAT,
    energy FLOAT,
    loudness FLOAT,
    mode FLOAT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    key INT,
    duration_ms INT,
    PRIMARY KEY (id)
);