#!/usr/bin/env python
# Author: Heitor Freitas Tancredo - heitortancredo@gmail.com
# Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 05:52:31)

import json
import argparse
from pprint import pprint
from lib.loadsmart import ProcessData
from lib.loadsmart import OptimalTruck


def main(trucks_file, cargo_file, json_matrix):

    matrix = {}
    products = []

    process_data = ProcessData('AIzaSyAkxtZAUKmJWFbdBjPFaEntMA8Qs0sSUFk')
    optimal_truck = OptimalTruck()

    # Load matrix with distances
    if trucks_file and cargo_file:
        matrix, products = process_data.get_total_distances(trucks_file, cargo_file)

    if json_matrix and not (trucks_file and cargo_file):
        with open(json_matrix) as fd:
            matrix = json.load(fd)

        # getting products list
        for p in matrix.values():
            products = p
            break

    final_result = {}

    for product in products:
        item = optimal_truck.choose_truck(product, matrix, final_result)
        final_result.update(item)

    print('\n\nResult:')

    pprint(final_result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loadsmart Backend test -\
                                     Author: Heitor Freitas Tancredo')
    parser.add_argument('-t', help='Trucks CSV file', required=False,
                        dest='trucks')
    parser.add_argument('-c', help='Cargos CSV file', required=False,
                        dest='cargos')
    parser.add_argument('-j', help='JSON file with matrix Cargos vs Trucks',
                        required=False, dest='json_file')
    args = vars(parser.parse_args())

    t_file = args.get('trucks')
    c_file = args.get('cargos')
    j_matrix = args.get('json_file')

    if not (t_file or c_file or j_matrix):
        print('\n **** No args found, run with default option: -j matrix.json ****')
        print('\n **** Run with -h to more options ****')
        j_matrix = 'matrix.json'

    main(t_file, c_file, j_matrix)
