# nae (under development)

A simple music organizer.

Organize and backup the musics in different device.

Max 30 min per day.

## Motivation

- [`beets`](https://beets.readthedocs.io/en/stable/) is nice, but
  - it does not use relative path
  - there is some rules I can not understand.
  - I do not need the auto-tagging, I am used to manually completing the tags
- I enjoy the processes of developing the package.
- I also want to learn and practice the programming skills.

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

## About nae

color `#86C166`

## TODO

- [x] upload to github
- [x] write the motivation
- [x] find a package to get the tag of music: [`mutagen`](https://mutagen.readthedocs.io/en/latest/index.html)
- [ ] compleate the tags handler
  - [x] define a class to save the tags obtain from `mutagen`
  - [ ] handle the case when tags are not complete.
- [ ] improve the database
  - [ ] add a table to save the info of database, such as `BASE_DIR`
  - [ ] handle playlist
- [ ] complete the WebUI
  - [x] add the `flac` format support
  - [ ] make the play button better
  - [ ] add a album page
- [ ] add logging system

## Acknowledge

- [`mutagen`](https://mutagen.readthedocs.io/en/latest/index.html)
- [`FastAPI`](https://fastapi.tiangolo.com/)
- [`HOWLER.JS`](https://howlerjs.com/)