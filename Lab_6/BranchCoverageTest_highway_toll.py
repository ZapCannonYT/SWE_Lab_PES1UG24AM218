import pytest
from highway_toll import toll_for, toll_charge, pass_advice

#Example test cases:
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0

def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100

#Code coverage test cases:
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

#Branch coverage test cases: take each decision the other way too.
def test_off_peak_with_fastag():
    assert toll_for(2, False, True) == pytest.approx(90.0)

def test_peak_without_fastag():
    assert toll_for(2, True, False) == pytest.approx(125.0)

def test_three_axle_off_peak_with_fastag():
    assert toll_for(3, False, True) == pytest.approx(142.5)

def test_three_axle_base_toll():
    assert toll_for(3, False, False) == 150

def test_four_axle_base_toll():
    assert toll_for(4, False, False) == 250

def test_large_vehicle_off_peak_no_fastag():
    assert toll_for(6, False, False) == 400

def test_zero_axles_raises():
    with pytest.raises(ValueError):
        toll_for(0, False, False)

def test_fire_engine_is_exempt():
    assert toll_charge("fire_engine", 3, True, False) == 0

def test_exempt_vehicle_skips_axle_check():
    assert toll_charge("ambulance", 1, False, False) == 0

def test_truck_invalid_axles_raises():
    with pytest.raises(ValueError):
        toll_charge("truck", 1, False, False)

def test_truck_off_peak_with_fastag():
    assert toll_charge("truck", 4, False, True) == pytest.approx(237.5)

def test_pass_advice_no_trips_either():
    assert pass_advice([], 2, 0) == "either"

def test_pass_advice_no_trips_pay_per_trip():
    assert pass_advice([], 2, 100) == "pay_per_trip"

def test_pass_advice_mixed_trips():
    assert pass_advice([(True, True), (False, False)], 2, 200) == "buy_pass"
