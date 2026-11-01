"""Tests specific to VanillaBPE-Byte: pure byte-level BPE."""

import pytest

from conftest import tok


def test_variant():
    assert tok.VARIANT == "vanillabpe_byte"


def test_no_cross_script_sharing(enc):
    hi = enc.encode_ordinary(" सरकार")
    bn = enc.encode_ordinary(" সরকার")
    assert len(hi) == len(bn) == 1
    assert hi != bn


def test_no_script_markers(enc):
    with pytest.raises(ValueError):
        enc.script_marker("deva")


def test_base_vocab_is_bytes(enc):
    # an unseen Indic character is its 3 UTF-8 bytes
    assert enc.encode_ordinary("ક") == list("ક".encode())
    assert enc.token_phonemes(enc.encode_ordinary("a")[0]) == ["<0x61>"]
