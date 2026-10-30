import pytest
from highway_toll import toll_for, toll_charge, pass_advice

#Example test case:
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0

#Code coverage test cases: each one runs lines not executed yet.
def test_invalid_axle_count_raises():
    with pytest.raises(ValueError):
        toll_for(1, True, True)

def test_two_axle_peak_with_fastag():
    assert toll_for(2, True, True) == pytest.approx(112.5)

def test_large_vehicle_peak_with_fastag():
    assert toll_for(5, True, True) == pytest.approx(475.0)

def test_car_is_charged():
    assert toll_charge("car", 2, True, True) == pytest.approx(112.5)

def test_pass_advice_buy_pass():
    assert pass_advice([(True, True)] * 2, 2, 200) == "buy_pass"

def test_pass_advice_either():
    assert pass_advice([(True, True)] * 2, 2, 225) == "either"

def test_pass_advice_pay_per_trip():
    assert pass_advice([(True, True)] * 2, 2, 300) == "pay_per_trip"
