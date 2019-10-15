import json
from datetime import datetime
import os.path
import sys

from flask import Flask, jsonify, request, make_response
#from flask_restful import Resource, Api
from flask_restplus import Api, Resource, fields
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .landmodel import LandEntry
app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app, version = "1.0", title = "Land Entries", description = "manages land entries for the lifegrow application")

name_space = api.namespace('main', description='Main APIs')

#model = api.models('Land Entry', {'Land entry': fields.String(required = True, description="Entry of the Land", help="Entry cannot be blank.")})

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

count = 0
def increment_landentryId():
    global count
    count = count + 1
    return count

class CounterfeitEntryError(Exception):
    pass

class GetAllLandEntries(Resource):
    land_entries = []
    @classmethod
    def get(self):
        return make_response(jsonify(
            {'entries':GetAllLandEntries.land_entries},
            {"message": "Land Entries successfully fetched"}), 200)


class AddNewLandEntry(Resource):
    @classmethod
    def post(self):
        try:
            landdata = request.get_json()
            landowner = landdata.get('land owner')
            name_owner = landdata.get('name owner')
            farm_location = landdata.get('farm location')
            landsize = landdata.get('land size')
            soiltests = landdata.get('soil tests')
            new_land_entry = LandEntry(increment_landentryId(), landowner, name_owner, farm_location, landsize,
            soiltests, get_timestamp())
            landentry = json.loads(new_land_entry.json())
            GetAllLandEntries.land_entries.append(landentry)

            return make_response(jsonify(
                {'entries': GetAllLandEntries.land_entries},
                {'message': "Land Entry successfully added"}), 200)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}), 400)


class ViewSpecificLandEntry(Resource):
    """get specific entry"""
    @classmethod
    def get(self, entryid):
        land_entries = GetAllLandEntries.land_entries
        land_entry = [eid for eid in land_entries if eid['entryId'] == entryid]
        return make_response(jsonify(
            {'entry': land_entry[0]},
            {"message": "Land Entry successfully fetched"}), 200)


class DeleteSpecificLandEntry(Resource):
    """delete a specify entry"""
    @classmethod
    def delete(self, entryid):
        land_entry = [eid for eid in GetAllLandEntries.land_entries if eid['entryId'] == entryid]
        GetAllLandEntries.land_entries.remove(land_entry[0])
        return make_response(jsonify(
            {'entry': land_entry[0]},
            {"message": "Land Entry successfully removed"}), 200)


class ModifySpecificLandEntry(Resource):
    """modify a specific entry"""
    @classmethod
    def put(self, entryid):
        land_entry = [land_entry for land_entry in GetAllLandEntries.land_entries if land_entry['entryId'] == entryid]
        try:
            landdata = request.get_json()
            landowner = landdata.get('land owner')
            name_owner = landdata.get('name owner')
            farm_location = landdata.get('farm location')
            landsize = landdata.get('land size')
            soiltests = landdata.get('soil tests')
            land_entry[0]['land owner'] = landowner
            land_entry[0]['name owner'] = name_owner
            land_entry[0]['farm location'] = farm_location
            land_entry[0]['land size'] = landsize
            land_entry[0]['soil tests'] = soiltests
            land_entry[0]['time'] = get_timestamp()

            return make_response(jsonify(
                {'entry':land_entry[0]},
                {'message': "Land Entry successfully updated"}), 201)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}), 401)

api.add_resource(GetAllLandEntries, '/api/v1/getlandentries', methods=['GET'])
api.add_resource(AddNewLandEntry, '/api/v1/addlandentries', methods=['POST'])
api.add_resource(ViewSpecificLandEntry, '/api/v1/viewlandentries/<int:entryid>', methods=['GET'])
api.add_resource(DeleteSpecificLandEntry, '/api/v1/dellandentries/<int:entryid>', methods=['DELETE'])
api.add_resource(ModifySpecificLandEntry, '/api/v1/modlandentries/<int:entryid>', methods=['PUT'])

if __name__ == "__main__":
    app.run(port= 5000)