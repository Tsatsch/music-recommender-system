# Secrets

Here all the secret data for config.json will be stored.

## How to get the data?
Please ask @Tsatsch or other contributors of this repository. We will either give you the access to the data or guide you on how to get the data by yourself.

## Overview of needed tokens
```json
{
    "client_id": "",
    "client_secret": "",
    "db_host" : "",
    "db_name" : "",
    "db_user" : "",
    "db_port" : "",
    "db_pw": "",
    "ip_key": "",
    "weather_key": ""
}
```
- client_id, client_secret: spotify developer authorization data. Please read [Spotify Authorization Guides](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/) to undestand how to get this data.
- db_*: data needed to access your database. We have used [Digital Ocean](https://www.digitalocean.com/) to create our own database.
- ip_key: key needed to get your location data from [ipstack](https://ipstack.com/). You can issue a token in your profile (so you need to register)
- weather_key: token need to get weather information (for your location). You can issue the api token on [Open Weather](https://openweathermap.org/) in your profile (you need to register)