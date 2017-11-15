from pytest import raises

from typedpy import Structure, Array, Number, String


class Trade(Structure):
    _additionalProperties = True
    _required = []
    #array support, similar to json schema
    a = Array(uniqueItems=True, minItems= 3, items = [String(), Number(maximum=10)])
    b = Array(minItems= 3, maxItems= 5, items = Number(maximum=10))




def test_wrong_type_for_array_err():
    with raises(TypeError) as excinfo:
        Trade(a=2)
    assert "a: Expected <class 'list'>" in str(excinfo.value)

def test_wrong_type_for_array_items_err():
    with raises(TypeError) as excinfo:
        Trade(a = ['aa', [], 2])
    assert "a_1: Expected a number" in str(excinfo.value)

def test_non_unique_items_err():
    with raises(ValueError) as excinfo:
        Trade(a = ['aa', 2, 2])
    assert "a: Expected unique items" in str(excinfo.value)

def test_invalid_number_in_array_err():
    with raises(ValueError) as excinfo:
        Trade(a = ['aa', 12, 2])
    assert "a_1: Expected a maxmimum of 10" in str(excinfo.value)


def test_invalid_number_in_array_variation_err():
    t = Trade(a = ['aa', 5, 2])
    with raises(ValueError) as excinfo:
        t.a[1] += 9
    assert "a_1: Expected a maxmimum of 10" in str(excinfo.value)

def test_no_schema_for_item_so_no_validation():
    t = Trade(a = ['aa', 5, 2])
    t.a[2] = None
    assert t.a==['aa', 5, None]

def test_a_is_valid():
    Trade(a = ['aa', 5, 2])

def test_update_1():
    t = Trade(a = ['aa', 5, 2])
    t.a[2] += 6
    assert t.a==['aa', 5, 8]
    assert t.a[2]==8

def test_update_append():
    t = Trade(a = ['aa', 5, 2])
    t.a.append(6)
    assert t.a==['aa', 5, 2, 6]

def test_update_too_short_err():
    t = Trade(a=['aa', 5, 2])
    with raises(ValueError) as excinfo:
        t.a=['']
    assert "a: Expected length of at least 3" in str(excinfo.value)


def test_update_to_wrong_type_err():
    t = Trade(a = ['aa', 5, 2])
    with raises(TypeError) as excinfo:
        t.a[0] = 1
    assert "a_0: Expected a string" in str(excinfo.value)

def test_not_enough_items_err():
    with raises(ValueError) as excinfo:
        Trade(a = ['aa', 2])
    assert "a: Expected length of at least 3" in str(excinfo.value)

def test_too_many_items_err():
    with raises(ValueError) as excinfo:
        Trade(b = [1,2,3,4,5,6])
    assert "b: Expected length of at most 5" in str(excinfo.value)

def test_single_Field_for_all_items_err():
    with raises(ValueError) as excinfo:
        Trade(b = [1,2,3,99])
    assert "b_3: Expected a maxmimum of 10" in str(excinfo.value)

def test_single_Field_for_all_items_valid():
    t = Trade(b=[1, 2, 3, 9])
    assert t.b==[1,2,3,9]