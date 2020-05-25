#!/usr/bin/env python
# Author: Heitor Freitas Tancredo - heitortancredo@gmail.com
# Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 05:52:31)
import csv
import googlemaps


class ProcessData:

    def __init__(self, google_api_key='AIzaSyBtWEygdpZ9-cfOU7eazfwFZgQbSvdpyDk'):
        self.gmaps_hdle = googlemaps.Client(google_api_key)
        pass

    def load_tucks(self, filename):
        """Loads the csv file with list of Trucks"""
        data = self.__load_csv(filename)
        return data

    def load_cargo(self, filename):
        """Loads the csv file with de list of Cargos"""
        data = self.__load_csv(filename)
        return data

    def __load_csv(self, filename):
        """Loads generic csv file and convert to JSON"""
        with open(filename) as fd:
            csv_reader = csv.DictReader(fd)
            data = [r for r in csv_reader]

        return data

    def gdistace_matrix(self, orig_lat, orig_lgn, dest_lat, dest_lgn):
        """Use Google Maps API to get the distance of two coordinates"""
        orig = '{0}, {1}'.format(orig_lat, orig_lgn)
        dest = '{0}, {1}'.format(dest_lat, dest_lgn)
        result = self.gmaps_hdle.distance_matrix(orig, dest, 'driving')
        try:
            meters = result.get('rows')[0].get('elements')[0].get('distance').get('value')
            return meters
        except Exception:
            return None

    def get_total_distances(self, trucks_file, cargo_file):
        """Creates the matrix with cargos and trucks distances"""
        trucks = self.load_tucks(trucks_file)
        cargos = self.load_cargo(cargo_file)

        travels = {}
        products_list = []

        print('Calculating distances: ', end='', flush=True)

        # CARGOS x TRUCKS
        for truck in trucks:
            print('+', end='', flush=True)
            origin_lat = truck.get('lat')
            origin_lng = truck.get('lng')
            truck_name = truck.get('truck')
            travels[truck_name] = {}

            for cargo in cargos:
                print('.', end='', flush=True)
                origin_state = cargo.get('origin_state')
                dest_state = cargo.get('destination_state')
                pickup_lat = cargo.get('origin_lat')
                pickup_lng = cargo.get('origin_lng')
                delivery_lat = cargo.get('destination_lat')
                delivery_lng = cargo.get('destination_lng')
                product = cargo.get('product')
                product = '{0} - {1}|{2}'.format(product, origin_state, dest_state)
                products_list.append(product)

                origin_pickup = self.gdistace_matrix(origin_lat, origin_lng, pickup_lat, pickup_lng)
                pickup_delivery = self.gdistace_matrix(pickup_lat, pickup_lng, delivery_lat, delivery_lng)
                delivery_origin = self.gdistace_matrix(delivery_lat, delivery_lng, origin_lat, origin_lng)
                total_distance = origin_pickup + pickup_delivery + delivery_origin

                travels[truck_name].update({product: total_distance})

        return travels, list(set(products_list))


class OptimalTruck:
    def __init__(self):
        pass

    def choose_truck(self, product, matrix, result, ignore=[]):
        """Gets the optimal route for the cargo"""
        distance = {}
        item = {}
        for truck in matrix:
            if truck in ignore:
                continue
            # takes the distance from the truck to the product
            distance[truck] = matrix.get(truck).get(product)
        if not distance:
            return {}
        best_truck = min(distance, key=distance.get)
        route = distance[best_truck]  # get the distance

        item = {
            best_truck: {product: route}
        }

        busy_truck = result.get(best_truck)

        if busy_truck:
            # if truck has the best route for two (or more) cargo choose the best one
            for prod, dist in busy_truck.items():

                ignore.append(best_truck)

                if dist < distance[best_truck]:
                    item = self.choose_truck(product, matrix, result, ignore)
                else:
                    # saves the new value and recalculate the route for the old cargo
                    result.update(item)
                    item = self.choose_truck(prod, matrix, result, ignore)
        return item
