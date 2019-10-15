from flask import Blueprint
from flask_restful import Api
from .landentries import AddNewLandEntry, ModifySpecificLandEntry, GetAllLandEntries, DeleteSpecificLandEntry, ViewSpecificLandEntry

entry = Blueprint('Land_entries', __name__)
api = Api(entry)
api.add_resource(GetAllLandEntries, '/api/v1/getlandentries')
api.add_resource(AddNewLandEntry, '/api/v1/addlandentries')
api.add_resource(ViewSpecificLandEntry, '/api/v1/viewlandentries/<int:entryid>')
api.add_resource(DeleteSpecificLandEntry, '/api/v1/dellandentries/<int:entryid>')
api.add_resource(ModifySpecificLandEntry, '/api/v1/modlandentries/<int:entryid>')