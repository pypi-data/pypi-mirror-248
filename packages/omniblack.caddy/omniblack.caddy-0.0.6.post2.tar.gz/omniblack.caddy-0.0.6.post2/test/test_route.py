import pytest

from omniblack.caddy import MatcherList


def test_list_and():
    with pytest.raises(TypeError):
        MatcherList() & MatcherList()
