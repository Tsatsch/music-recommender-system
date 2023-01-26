# Config
Here is a short docu of what config data and credentials you will need.

## Config data
can be found in config/config.json
```json
{
    "clientId": "",
    "dbHost": "",
    "dbName": "",
    "dbUser": "",
    "dbPort": ""
}
```
|Variable| Description|
|---|---|
|clientId|Spotify client id|
|dbHost|Host name of the database|
|dbName|Name of the database|
|dbUser|Username with that you can enter the database|
|dbPort|Port of the database|

## Secrets data
can be found in config/.env
```env
DB_PWD=
SPOTIFY_CLIENT_SECRET=
WEATHER_API=
GEO_API=
```
|Variable| Description|
|---|---|
|DB_PWD|Password for the database user dbUser|
|SPOTIFY_CLIENT_SECRET|Spotify secret for the client with clientId provided |
|WEATHER_API|API token for [openweathermap](https://openweathermap.org/)|
|GEO_API|API token for [ipstack](https://ipstack.com/|

## How to get the data?
Please ask @Tsatsch or other contributors of this repository. We will either give you the access to the data or guide you on how to get the data by yourself.

- client_id, client_secret: spotify developer authorization data. Please read [Spotify Authorization Guides](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/) to undestand how to get this data.
- db_*: data needed to access your database. We have used [Digital Ocean](https://www.digitalocean.com/) to create our own database.
- ip_key: key needed to get your location data from [ipstack](https://ipstack.com/). You can issue a token in your profile (so you need to register)
- weather_key: token need to get weather information (for your location). You can issue the api token on [Open Weather](https://openweathermap.org/) in your profile (you need to register)