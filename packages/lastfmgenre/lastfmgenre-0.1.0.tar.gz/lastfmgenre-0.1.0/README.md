# LastFMGenre

`lastfmgenre` is a standalone version of the [lastgenre](https://beets.readthedocs.io/en/stable/plugins/lastgenre.html) plugin from the [Beets](https://beets.io) music library manager by Adrian Sampson.

This packge does one thing: it helps retrieve sane genre values from Last.fm tags. 

It does this by utilizing a pre-built whitelist to exclude unhelpful tags like "seen live" or "female vocalists". You can also provide your own whitelist, or forego the whitelist altogether (see config options below).

An option to "canonicalize" genre names also exists, which will convert more obscure or specific genres into coarser-grained ones that are present in the whitelist. A more detailed breakdown of how this works is provided in the [lastgenre documentation](https://beets.readthedocs.io/en/stable/plugins/lastgenre.html#canonicalization).

## Installing

Install this package with:
```
pip3 install lastfmgenre
```

## Configuration
Configuration parameters are passed to the `LastFMGenre` class on instantiation.

| Parameter | Description |
| --------- | ----------- |
| lastfm_api_key | **Required** The api key for your [last.fm API application](https://www.last.fm/api) |
| canonical      | Use a canonicalization tree. Setting this to `True` will use a built-in tree. You can also set it to a path, like the `whitelist` config value, to use your own tree. Default: `False` (disabled). |
| count          | Number of genres to fetch. Default: `1`. |
| min_weight | Minimum popularity factor below which genres are discarded. Default: `10`. |
| sort | Defines how the returned genres are sorted. Currently supports two options: `popular` (sort genres by most to least popular) and `specific` (sort genres by most to least specific). Default: `popular`. |
| separator | A separator for multiple genres. Default: `, `. |
| whitelist | One of: `True` (use the internal whitelist), `False` (use no whitelist), or a filepath to a custom whitelist. Default `True`. |
| title_case | Convert tags to TitleCase before returning. Default `True`. |


## Usage

The most basic usage goes something like:

```python
from lastfmgenre import LastFMGenre

g = LastFMGenre(config_params={"lastfm_api_key": "my-lastfm-api-key"})
g.fetch_track_genre("Lady Gaga", "Telephone")
```

`LastFMGenre` provides several methods to retrieve genre tags:

- fetch_album_genre(artist, album)
- fetch_artist_genre(artist)
- fetch_track_genre(artist, title)



## Many Thanks
Thanks go to [Adrian Sampson](https://www.cs.cornell.edu/~asampson/) and the [Beets](https://beets.io) project for providing such an extensive genre whitelist and a great plugin for me to ~~steal~~ repurpose. 