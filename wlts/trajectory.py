from werkzeug.exceptions import BadRequest, NotFound

from wlts.collection import collection_manager


class TrajectoryParams:
    """Object wrapper for Trajectory Request Parameters"""

    def __init__(self, **properties):
        """Creates a trajectory parameter object
        Args:
            **properties (dict) - Request parameters
        """
        self.collections = properties.get('collections').split(',') if properties.get('collections') else None
        self.longitude = float(properties.get('longitude'))
        self.latitude = float(properties.get('latitude'))
        self.start_date = properties.get('start_date') if properties.get('start_date') else None
        self.end_date = properties.get('end_date') if properties.get('end_date') else None
        self.class_type = properties.get('class_type') if properties.get('class_type') else None
        # self.collections =  properties.get('collections').split(',')
        # self.start_date = properties.get('start_date')
        # self.end_date = properties.get('end_date')
        # self.class_type = properties.get('class_type')

    def to_dict(self):
        """Export Trajectory params to Python Dictionary"""

        return {
            k: v
            for k, v in vars(self).items() if not k.startswith('_')
            }


class Trajectory:
    @classmethod
    def list_coverage(cls):

        collections = collection_manager.get_all_collection_names()
        return collections['feature_collection'] + collections['image_collection']

    @classmethod
    def check_collection(cls, collection):
        """Utility to check coverage existence in memory"""

        print(collection)
        print(cls.list_coverage())
        if collection not in cls.list_coverage():
            raise NotFound('Collection "{}" not found'.format(collection))

    @staticmethod
    def get_collections(ts_params):

        """Retrieves collections"""
        features = []
        try:

            for collections_name in ts_params.collections:
                features.append(collection_manager.get_collection(collections_name))

            return features

        except RuntimeError:
            raise BadRequest('No Collection found')

    @classmethod
    def get_trajectory(cls, ts_params: TrajectoryParams):
        """
        Retrieves time series object
        Args:
            ts_params (TrajectoryParams): WLTS Request parameters
        Returns:
            dict trajectory object.
                See `json-schemas/trajectory_response.json`
        """

        if (ts_params.collections):

            # Validate collection existence
            for collection in ts_params.collections:
                cls.check_collection(collection)

            collections = cls.get_collections(ts_params)
        else:
            print("All Collections")

            collections = collection_manager.get_all_collection()

        # Retrieves the collections that matches the Trajectory collections name arguments

        tj_attr = []

        for collection in collections:
            print("Get trajectory off Collection Name: {}".format(collection.get_name()))

            collection.trajectory(tj_attr, ts_params.latitude, ts_params.longitude, ts_params.start_date,
                                  ts_params.end_date)

        newtraj = sorted(tj_attr, key=lambda k: k['data'])

        return {
            "query": ts_params.to_dict(),
            "result": {
                "trajectory": newtraj
            }

        }
