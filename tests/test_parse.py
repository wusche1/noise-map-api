from noise_map.parse import parse_db


def test_lden_range():
    assert parse_db("Lden5559") == "55-59 dB(A)"


def test_lnight_range():
    assert parse_db("Lnight5054") == "50-54 dB(A)"


def test_high_range():
    assert parse_db("Lden7074") == "70-74 dB(A)"


def test_above_75():
    assert parse_db("Lden75") == ">75 dB(A)"


def test_unknown_passthrough():
    assert parse_db("something_weird") == "something_weird"
