from bdc_core.decorators.validators import require_model
from bdc_core.utils.flask import APIResource
from flask import jsonify, request
from flask_restplus import Namespace

from wlts.classificationsys import classification_sys_manager
from wlts.collection import collection_manager
from wlts.schemas import (collections_list, describe_collection,
                          list_classification_system, trajectory)
from wlts.trajectory import Trajectory, TrajectoryParams

"""Controllers of Web Land Trajectory Service
The WLTS consists in five operations:
    - `wlts/list_collections` Retrieve list of available collections
    - `wlts/describe_collection` Retrieves collection description
    - `wlts/trajectory` etrieves the trajectories of collections associated with a given location in space.
    - `wlts/list_classification_sytem` Retrieve list of available classification system
"""

api = Namespace('wlts', description='status')

@api.route('/list_collections')
class ListCollectionsController(APIResource):

    @require_model(collections_list)
    def get(self):
        if 'collection_type' in request.args:
            collection_type = request.args['collection_type']

            names = collection_manager.get_collection_name(collection_type)

            response = {
                collection_type:names

            }
            return jsonify(response)
        else:
            all_names = collection_manager.get_all_collection_names()

            return jsonify(all_names)

@api.route('/describe_collections')
class DescribeCollection(APIResource):

    @require_model(describe_collection)
    def get(self):
        collection_name = request.args['name']
        data = { "name": collection_name,  "class_attribute": "class_name",   "period_attribute":"data_observacao", "resolution_unit":"year|month-year|day-month-year"}
        return jsonify({"collection_name":data})

@api.route('/trajectory')
class TimeSeries(APIResource):

    @require_model(trajectory)
    def get(self):
        params = TrajectoryParams(**request.args.to_dict())

        return jsonify(Trajectory.get_trajectory(params))

@api.route('/list_classification_system')
class ListClassificationSystemController(APIResource):

    @require_model(list_classification_system)
    def get(self):
        all_classification = classification_sys_manager.get_all_classification_system()

        return jsonify({"classification_system": all_classification})
