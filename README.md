# napi-py [![Build Status](https://travis-ci.com/emkor/napi-py.svg?branch=master)](https://travis-ci.com/emkor/napi-py)
CLI tool for downloading subtitles from napiprojekt.pl, fork of [gabrys/napi.py](https://github.com/gabrys/napi.py)

## prerequisites
- Python 3.6 or newer

## installation
- `pip install napi-py` for user-wide installation

## usage as CLI tool
- `napi-py ~/Downloads/MyMovie.mp4` will download and save subtitles under `~/Downloads/MyMovie.srt`

## usage as lib
```python
from napi import NapiPy

movie_path = "~/Downloads/MyMovie.mp4"

napi = NapiPy()
movie_hash = napi.calc_hash(movie_path)
source_encoding, target_encoding, tmp_file = napi.download_subs(movie_hash)
subs_path = napi.move_subs_to_movie(tmp_file, movie_path)
print(subs_path)
```

## in case of issues
- if there's issue with weird characters in downloaded subtitles, try to re-download and use flag `--from-enc utf-8`
- if there's no subtitles for your movie, there's still hope:
    - open the movie web page on `napiprojekt.pl` in your browser, as in example: `https://www.napiprojekt.pl/napisy1,1,1-dla-55534-Z%C5%82odziejaszki-(2018)`
    - choose subtitles that might match your movie, right-click them and select "Copy link" on link containing hash, which looks like this `napiprojekt:96edd6537d9852a51cbdd5b64fee9194`
    - use flag `--hash YOURHASH` in this tool, i.e. `--hash 96edd6537d9852a51cbdd5b64fee9194` or `--hash napiprojekt:96edd6537d9852a51cbdd5b64fee9194`

## development
- `make config` installs `venv` under `.venv/napi-py`
- `make test` runs tests
- `make build` creates installable package
