-- not used, dropped
CREATE TABLE songs (
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
    time_signature FLOAT,
    mode FLOAT,
    key INT,
    duration_ms INT,
    PRIMARY KEY (id)
);

-- not used, dropped
CREATE TABLE music (
    id varchar NOT NULL,
    danceability FLOAT,
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
    PRIMARY KEY (id)
);


-- this the current active table in the database
CREATE TABLE spotify (
    id varchar NOT NULL,
    danceability FLOAT,
    energy FLOAT,
    loudness FLOAT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    popularity INT,
    genre varchar,
    PRIMARY KEY (id)
);
