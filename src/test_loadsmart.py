import json
from pprint import pprint
from collections import OrderedDict
from lib.loadsmart import OptimalTruck
from lib.loadsmart import ProcessData


def test_full_json_reuslt():

    opt_truck = OptimalTruck()
    products = []

    with open('test_files/test_full_json_result.json') as fd:
        input_json = json.load(fd)

    for p in input_json.values():
        products = p
        break

    final = {}

    for p in products:
        resp = opt_truck.choose_truck(p, input_json, final)
        final.update(resp)

    expected = {
        "Allen R Pruittrown City": {"Apples - OH|CA": 897},
        "Arachus Incashville": {"Cell phones - NC|OR": 954},
        "Arrow Towing Llcent": {"Light bulbs - MO|TX": 497},
        "Como Construction Llcottstown": {"Oranges - IA|IL": 325},
        "Dawna L Zanderppleton": {"Recyclables - VA|FL": 985},
        "Dupree Testing Services Incutchinson": {"Wood - KY|LA": 353},
        "Edmon'S Unique Furniture & Stone Gallery Inc.Os Angeles": {"Wood - MN|IL": 135}
    }

    pprint(final)

    for truck in expected:
        assert final[truck] == expected[truck]


def test_get_best_cargo_for_truck():

    opt_truck = OptimalTruck()
    with open('test_files/test_get_best_cargo_for_truck.json') as fd:
        input_json = json.load(fd)

    for p in input_json.values():
        products = p
        break

    final = {}

    for p in products:
        resp = opt_truck.choose_truck(p, input_json, final)
        final.update(resp)

    expected = {'Hartford Plastics Incartford': {'Light bulbs - MO|TX': 231}}

    for truck in expected:
        assert final[truck] == expected[truck]

    assert final == expected


def test_truck_has_two_optimal_route():

    opt_truck = OptimalTruck()
    with open('test_files/test_truck_has_two_optimal_route.json') as fd:
        input_json = json.load(fd)

    for p in input_json.values():
        products = p
        break

    final = {}

    for p in products:
        resp = opt_truck.choose_truck(p, input_json, final)
        final.update(resp)

    expected = {
        "Allen R Pruittrown City": {"Apples - OH|CA": 897},
        "Arachus Incashville": {"Light bulbs - MO|TX": 484}
    }
    for truck in expected:
        assert final[truck] == expected[truck]


def test_load_cargo_file():
    pd = ProcessData()
    out_json = pd.load_cargo('test_files/cargo.csv')
    expected = [OrderedDict([('product', 'Light bulbs'),
                             ('origin_city', 'Sikeston'),
                             ('origin_state', 'MO'),
                             ('origin_lat', '36.876719'),
                             ('origin_lng', '-89.5878579'),
                             ('destination_city', 'Grapevine'),
                             ('destination_state', 'TX'),
                             ('destination_lat', '32.9342919'),
                             ('destination_lng', '-97.0780654')]),
                OrderedDict([('product', 'Recyclables'),
                             ('origin_city', 'Christiansburg'),
                             ('origin_state', 'VA'),
                             ('origin_lat', '37.1298517'),
                             ('origin_lng', '-80.4089389'),
                             ('destination_city', 'Apopka'),
                             ('destination_state', 'FL'),
                             ('destination_lat', '28.6934076'),
                             ('destination_lng', '-81.5322149')])
                ]
    assert out_json == expected


def test_load_trucks_file():
    pd = ProcessData()
    out_json = pd.load_tucks('test_files/trucks.csv')
    expected = [OrderedDict([('truck', 'Hartford Plastics Incartford'),
                             ('city', 'Florence'),
                             ('state', 'AL'),
                             ('lat', '34.79981'),
                             ('lng', '-87.677251')]),
                OrderedDict([('truck', 'Beyond Landscape & Design Llcilsonville'),
                             ('city', 'Fremont'),
                             ('state', 'CA'),
                             ('lat', '37.5482697'),
                             ('lng', '-121.9885719')])
                ]
    assert out_json == expected


def test_gmatrix_distance():
    pd = ProcessData('AIzaSyAkxtZAUKmJWFbdBjPFaEntMA8Qs0sSUFk')

    org_lat = -27.579693
    org_lng = -48.511495
    dest_lat = -27.590058
    dest_lng = -48.510179

    distance = pd.gdistace_matrix(org_lat, org_lng, dest_lat, dest_lng)
    expected = 2736

    assert distance == expected


def test_get_total_distances():
    pd = ProcessData('AIzaSyAkxtZAUKmJWFbdBjPFaEntMA8Qs0sSUFk')
    _trucks = 'test_files/trucks.csv'
    _cargos = 'test_files/cargo.csv'

    matrix, products = pd.get_total_distances(_trucks, _cargos)
    pprint(matrix)
    expected_matrix = {
        'Beyond Landscape & Design Llcilsonville': {'Light bulbs - MO|TX': 7051320,
                                                    'Recyclables - VA|FL': 10028374},
        'Hartford Plastics Incartford': {'Light bulbs - MO|TX': 2325712,
                                         'Recyclables - VA|FL': 3053437}
    }
    expected_products = ['Light bulbs - MO|TX', 'Recyclables - VA|FL']

    for truck in expected_matrix:
        for prod in expected_products:
            distance = matrix.get(truck).get(prod)
            # just to verify if the distance has calculated for all products
            assert distance > 0

    assert not set(products) ^ set(expected_products)
