# nae

A simple music organizer, under development...

Max 30 min per day.

## Supported format

- [x] mp3
- [x] flac

## Develop principles

- The music library can be transport, synchronized easily in different place.

- Multi-artist should be dealt with.

## Music library principles

- Every file should be tagged completely, the tags should include
  - title
  - album
  - artist
  - album artist
  - genre
  - data
  - album picture

## About aae

color `#86C166`

## TODO

- [x] upload to github
- [ ] write the motivation
- [x] find a package to get the tag of music: [`mutagen`](https://mutagen.readthedocs.io/en/latest/index.html)
  - [x] define a class to save the tags obtain from `mutagen`
  - [ ] handle the case when tags are not complete.
- [ ] improve the database
  - [ ] add a table to save the info of database, such as `BASE_DIR`
  - [ ] handle playlist
- [ ] complete the WebUI
  - [ ] add the `flac` format support
  - [ ] make the play button better
  - [ ] add a album page
