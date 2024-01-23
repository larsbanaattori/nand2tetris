from coder import *

def test_dest() -> None:
    assert dest("") == "000"
    assert dest("M") == "001"
    assert dest("D") == "010"
    assert dest("DM") == "011"
    assert dest("A") == "100"
    assert dest("AM") == "101"
    assert dest("AD") == "110"
    assert dest("ADM") == "111"
