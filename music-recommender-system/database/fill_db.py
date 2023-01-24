import os
import io
import json
import csv
import time
import progressbar
import psycopg2
from dotenv import dotenv_values
from utils import parser
from utils.spotify import Spotify
from utils.database import Database


def main():
    config, secrets = parser.setup()
    sp = Spotify(config=config, secrets=secrets)
    db = Database(config=config, secrets=secrets)
    parsed_data_arr = parse_json("../resources/open-data/mpd.slice.0-999.json")

    FROM = 60000
    TO = 6300
    print(f"max: {len(parsed_data_arr)}")
    generate_data_new_way(sp, parsed_data_arr[FROM:TO])
    insert_csv_into_db(db, "music1", "songs.tsv")


def parse_json(path):
    # [{'id': uri, 'song': track['track_name'], 'artist': track['artist_name']}, ...]
    main_data = []
    with open(path) as f:
        data = json.load(f)
        for line in data["playlists"]:
            for track in line["tracks"]:
                uri = track["track_uri"].split(":")[-1]
                song_dict = {
                    "id": uri,
                    "song": track["track_name"],
                    "artist": track["artist_name"],
                }
                main_data.append(song_dict)
    return main_data


def preprocess_playlist_1(playlist, spotify_conn):  # playlist here is csv with uri
    start = time.time()
    list_of_songs = []  # store songname
    list_of_uris = []  # store uris for songs
    artist_name = []
    popularity = []
    limit = 100  # maxmum 100 at once
    l = len(playlist)  # amount of songs
    limitcount = int(l / limit)  # (#songs) /limit
    songleft = 0
    uri_of_playlist = [song["id"] for song in playlist]
    # Get all the features of the song
    for i in range(l):
        result = spotify_conn.track(uri_of_playlist[i])
        list_of_songs.append([{"song": result["name"]}])
        artist_name.append(
            {"artist": result["artists"][0]["name"]}
        )  # get the artist_name
        popularity.append(
            {"popularity": result["popularity"]}
        )  # get the popularity of the song
    for j in range(limitcount + 2):
        songleft = l - j * limit
        if songleft > limit:
            Features = spotify_conn.audio_features(
                uri_of_playlist[j * limit : j * limit + limit]
            )
            for i in range(limit):
                list_of_songs[j * limit + i][0].update(artist_name[i])
                list_of_songs[j * limit + i][0].update(popularity[i])
                list_of_songs[j * limit + i][0].update(Features[i])
                del list_of_songs[j * limit + i][0]["type"]
                del list_of_songs[j * limit + i][0]["track_href"]
                del list_of_songs[j * limit + i][0]["analysis_url"]
                del list_of_songs[j * limit + i][0]["uri"]
        elif limit >= songleft > 0:
            Features = spotify_conn.audio_features(
                uri_of_playlist[j * limit : j * limit + songleft]
            )
            for i in range(songleft):
                list_of_songs[j * limit + i][0].update(artist_name[i])
                list_of_songs[j * limit + i][0].update(popularity[i])
                list_of_songs[j * limit + i][0].update(Features[i])
                del list_of_songs[j * limit + i][0]["type"]
                del list_of_songs[j * limit + i][0]["track_href"]
                del list_of_songs[j * limit + i][0]["analysis_url"]
                del list_of_songs[j * limit + i][0]["uri"]

        else:
            end = time.time()
            print(f"Time for preprocess_playlist_1: {end - start} sec.")
            cleaned = [dictionary[0] for dictionary in list_of_songs]
            write_tsv(cleaned, True)


def generate_data_new_way(spotify_connection, playlist):
    list_of_songs = []  # store songname
    artist_name = []
    popularity = []
    limit = 100  # maxmum 100 at once
    l = len(playlist)  # amount of songs
    limitcount = int(l / limit)  # (#songs) /limit
    uri_of_playlist = [song["id"] for song in playlist]
    start = time.time()
    # Get all the features of the song
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=l).start()
    for i in range(l):
        result = spotify_connection.track(
            uri_of_playlist[i],
        )
        list_of_songs.append([{"song": result["name"]}])
        artist_name.append(
            {"artist": result["artists"][0]["name"]}
        )  # get the artist_name
        popularity.append(
            {"popularity": result["popularity"]}
        )  # get the popularity of the song
        bar.update(i)
    bar.finish()
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=limitcount + 2).start()
    for j in range(limitcount + 2):
        songleft = l - j * limit
        Features = spotify_connection.audio_features(
            uri_of_playlist[j * limit : j * limit + limit]
        )
        if songleft > limit:
            for i in range(limit):
                list_of_songs[j * limit + i][0].update(artist_name[i])
                list_of_songs[j * limit + i][0].update(popularity[i])
                list_of_songs[j * limit + i][0].update(Features[i])
                del list_of_songs[j * limit + i][0]["type"]
                del list_of_songs[j * limit + i][0]["track_href"]
                del list_of_songs[j * limit + i][0]["analysis_url"]
                del list_of_songs[j * limit + i][0]["uri"]
        elif limit >= songleft > 0:
            for i in range(songleft):
                list_of_songs[j * limit + i][0].update(artist_name[i])
                list_of_songs[j * limit + i][0].update(popularity[i])
                list_of_songs[j * limit + i][0].update(Features[i])
                del list_of_songs[j * limit + i][0]["type"]
                del list_of_songs[j * limit + i][0]["track_href"]
                del list_of_songs[j * limit + i][0]["analysis_url"]
                del list_of_songs[j * limit + i][0]["uri"]

        else:
            cleaned = [dictionary[0] for dictionary in list_of_songs]
            write_tsv(cleaned, True)
        bar.update(j)
    bar.finish()

    end = time.time()
    print(f"Time for generate_data_new_way: {end - start} sec.")


def generate_data(spotify_connection, json_data):
    full_arr = []
    start = time.time()
    counter = 0
    SPLIT = 200
    # use the split to write down the data into file
    # every 100 lines, so if there should be a crash
    # for long csv files, then at least we have not lost
    # most of the data and can reuse it
    bar = progressbar.ProgressBar().start(max_value=len(json_data))
    for json_song in json_data:
        if counter != 0 and counter % SPLIT == 0:
            if counter == SPLIT:
                write_tsv(full_arr, True)
            else:
                write_tsv(full_arr, False)
            full_arr.clear()
        features_dic = spotify_connection.audio_features(json_song["id"])[0]
        del (
            features_dic["type"],
            features_dic["uri"],
            features_dic["track_href"],
            features_dic["analysis_url"],
        )
        popularity = spotify_connection.track(f'{json_song["id"]}')["popularity"]
        features_dic["popularity"] = popularity
        full_arr.append(json_song | features_dic)
        counter += 1
        bar.update(counter)
    bar.finish()
    # if counter < SPLIT:
    #     write_tsv(full_arr, True)
    # else:
    #     write_tsv(full_arr, False)

    end = time.time()
    print(f"Time for add_features: {end - start} sec.")


def write_tsv(data, is_first):
    # write data
    keys = data[0].keys()
    if is_first:
        with open(
            "songs.tsv",
            "w",
            newline="",
        ) as output_file:
            dict_writer = csv.DictWriter(output_file, keys, delimiter="\t")
            dict_writer.writeheader()
            dict_writer.writerows(data)
    else:
        with open(
            "songs.tsv",
            "a",
            newline="",
        ) as output_file:
            dict_writer = csv.DictWriter(output_file, keys, delimiter="\t")
            dict_writer.writerows(data)


def connect_db(config_file):
    """Connect to the PostgreSQL database server
    with given config"""

    with open(config_file) as f:
        config = json.load(f)

    conn = None
    try:
        conn = psycopg2.connect(
            host=config["db_host"],
            dbname=config["db_name"],
            port=config["db_port"],
            user=config["db_user"],
            password=config["db_pw"],
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def clean_csv_value(value):
    if value is None:
        return r"\N"
    return str(value).replace("\n", "\\n")


def csv_to_dict(csv_file):
    # needed to create csv like object for copy_from()
    res = []
    with open(csv_file) as f:
        header = f.readline().strip().split("\t")
        for line in f.readlines():
            dic = {}
            for i, value in enumerate(line.split("\t")):
                dic[header[i]] = value.strip()
            res.append(dic)
    return res


def insert_csv_into_db(db, table_name, data_file):
    start = time.time()
    cur = db.cursor()

    # remove data that is already in the database (acc. to ids that are PK)
    query = f"SELECT id FROM {table_name};"
    cur.execute(query)
    db_ids = cur.fetchall()
    db_ids_clean = []
    for ids in db_ids:
        db_ids_clean.append(ids[0])

    with open(data_file, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader, None)
        filtered_data = [row for row in reader if row[-3] not in db_ids_clean]

    with open(data_file, "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(header)
        writer.writerows(filtered_data)

    # remove duplicates in file (in the current segment of data we use)
    with open(data_file, "r") as f, open("clean_songs.tsv", "w") as out_file:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader, None)
        writer = csv.writer(out_file, delimiter="\t")
        writer.writerow(header)
        current_ids = []
        for row in reader:
            if row[-3] not in current_ids:
                writer.writerow(row)
            current_ids.append(row[-3])

    csv_as_dict = csv_to_dict("clean_songs.tsv")
    csv_file_like_object = io.StringIO()

    for arg in csv_as_dict:
        csv_file_like_object.write(
            "~".join(
                map(
                    clean_csv_value,
                    (
                        arg["id"],
                        arg["song"],
                        arg["artist"],
                        arg["danceability"],
                        arg["energy"],
                        int(arg["key"]),
                        arg["loudness"],
                        arg["mode"],
                        arg["speechiness"],
                        arg["acousticness"],
                        arg["instrumentalness"],
                        arg["liveness"],
                        arg["valence"],
                        arg["tempo"],
                        int(arg["duration_ms"]),
                        int(arg["time_signature"]),
                        int(arg["popularity"]),
                    ),
                )
            )
            + "\n"
        )
    csv_file_like_object.seek(0)

    cur.copy_from(csv_file_like_object, table_name, sep="~")
    # commit request
    db.commit()
    end = time.time()
    print(f"Time for insert_csv_into_db: {end - start} sec.")
    print("Import done")


if __name__ == "__main__":
    main()
