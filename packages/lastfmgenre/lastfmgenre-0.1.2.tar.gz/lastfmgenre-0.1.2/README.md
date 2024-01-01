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
| group_canonical | If `True`, ignore `sort` and returns the most popular genres, nested into groups with their canonical 'parent' tags. If `canonical` is `False`, this parameter is ignored. Default: `False`.
| min_weight | Minimum popularity factor below which genres are discarded. Default: `10`. |
| sort | Defines how the returned genres are sorted. Currently supports two options: `popular` (sort genres by most to least popular) and `specific` (sort genres by most to least specific). Default: `popular`. |
| whitelist | One of: `True` (use the internal whitelist), `False` (use no whitelist), or a filepath to a custom whitelist. Default `True`. |
| title_case | Convert tags to TitleCase before returning. Default `True`. |


## Usage Examples

The most basic usage goes something like:

```python
>>> from lastfmgenre import LastFMGenre
>>> g = LastFMGenre(config_params={"lastfm_api_key": "my-lastfm-api-key", "count": 3})
>>> g.fetch_track_genre("Lady Gaga", "Telephone")
['Pop', 'Dance', 'Electropop']
```

Setting `sort` to `specific`:
```python
>>> from lastfmgenre import LastFMGenre
>>> g = LastFMGenre(config_params={"lastfm_api_key": "my-lastfm-api-key", "count": 3, "sort": "specific"})
>>> g.fetch_track_genre("Lady Gaga", "Telephone")
['Electropop', 'Pop', 'Electronic']
```

Setting `group_canonical` to True:
```python
>>> from lastfmgenre import LastFMGenre
>>> g = LastFMGenre(config_params={"lastfm_api_key": "my-lastfm-api-key", "count": 3, "canonical": True, "group_canonical": True})
>>> g.fetch_track_genre("Lady Gaga", "Telephone")
[['Pop'], ['Dance'], ['Electropop', 'Electro', 'Electronic']]
```

`LastFMGenre` provides several methods to retrieve genre tags:

- fetch_album_genres(artist, album)
- fetch_artist_genres(artist)
- fetch_track_genres(artist, title)



## Many Thanks
Thanks go to [Adrian Sampson](https://www.cs.cornell.edu/~asampson/) and the [Beets](https://beets.io) project for providing such an extensive genre whitelist and a great plugin for me to ~~steal~~ repurpose. 