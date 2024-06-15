from napi import NapiPy


def test_should_download_correctly_encoded_subs():
    movie_hash = '25b1087d997bfbf8a4be462255e05a05'
    napi = NapiPy()
    src_enc, tgt_enc, tmp_file = napi.download_subs(movie_hash)
    assert src_enc == 'UTF-8-SIG'

    with open(tmp_file) as subs_file:
        subs = subs_file.read()

    expected_phrases = ['źródło', 'władzę', 'Dziękuję', 'zgłębiają', 'ZWYCIĘŻĄ!']
    for expected_phrase in expected_phrases:
        assert expected_phrase in subs


def test_should_return_none_when_no_subtitles_for_movie():
    movie_hash = '00000000000000000000000000000000'
    napi = NapiPy()
    src_enc, tgt_enc, tmp_file = napi.download_subs(movie_hash)
    assert src_enc is None
    assert tmp_file is None


def test_should_download_subs_with_forced_encoding():
    movie_hash = '0e9b0d0d3dc5abc0538d207d477af4a1'
    napi = NapiPy()
    src_enc, tgt_enc, tmp_file = napi.download_subs(movie_hash, use_enc="utf-8")
    assert  src_enc == "utf-8"

    with open(tmp_file) as subs_file:
        subs = subs_file.read()

    expected_phrases = ['ciąży', 'artykułów', 'Właśnie', 'wyjść', 'wciąż']
    for expected_phrase in expected_phrases:
        assert expected_phrase in subs


def test_should_download_subs_in_utf_16():
    movie_hash = 'f517eb7e09d270a3b83b14403712ab96'
    napi = NapiPy()
    src_enc, tgt_enc, tmp_file = napi.download_subs(movie_hash)
    assert src_enc == 'UTF-16'

    with open(tmp_file) as subs_file:
        subs = subs_file.read()

    expected_phrases = ['Łaskawy', 'powrócili', 'londyńskiej', 'rozbłyśnie', 'wyróżniająca']
    for expected_phrase in expected_phrases:
        assert expected_phrase in subs
