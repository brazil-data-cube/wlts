from flask_restplus import Namespace
from bdc_core.utils.flask import APIResource
from bdc_core.decorators.validators import require_model
from flask import jsonify, request
from wlts.schemas import describe_collection, collections_list, trajectory

"""Controllers of Web Land Trajectory Service
The WLTS consists in five operations:
    - `wlts/list_collections` Retrieve list of available collections
    - `wlts/describe_collection` Retrieves collection description
    - `wlts/trajectory` etrieves the trajectories of collections associated with a given location in space.
    - `wlts/list_classification_sytem` Retrieve list of available classification system
    - `wlts/list_legend_system` Retrieves avaliable legend of classification system
"""

api = Namespace('wlts', description='status')

@api.route('/list_collections')
class ListCollectionsController(APIResource):

    @require_model(collections_list)
    def get(self):
        if 'collectionstype' in request.args:
            collection_type = request.args['collectionstype']
            response = {
                "feature_collection":["Prodes", "Deter"]

            }
            return jsonify(response)
        else:
            response = {
                "feature_collection":["Prodes", "Deter"],
                "image_collection":["MapBiomas"]
            }
            return jsonify(response)

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
        return jsonify({'trajectory': 'teste'})

# @api.route('/list_classification_sytem')
# class ListClassificationSystemController(APIResource):

#     @require_model(trajectory)
#     def get(self):
#         return {}

# @api.route('/list_classification_sytem')
# class ListLegendSystemController(APIResource):

#     @require_model(trajectory)
#     def get(self):
#         return {}