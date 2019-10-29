from abc import ABCMeta, abstractmethod
import psycopg2
from json import loads as json_loads
from pathlib import Path
from shapely.geometry import Point
from wlts.config import BASE_DIR

config_folder = Path(BASE_DIR) / 'json-config/'

class PostgisConnection:
    """

    PostgisConnection

    Args:
        pgisInfo (dic): Python object (dict) with connection info
    Returns:
        psycopg2.connect
    Raises:
        Exception, psycopg2.Error When connection is not stabelish

    """

    def connection_open(pgisInfo):
        try:
            connection = psycopg2.connect(user = pgisInfo["user"],
                                          password = pgisInfo["password"],
                                          host = pgisInfo["host"],
                                          port = pgisInfo["port"],
                                          database = pgisInfo["database"]
                                          )

            print("Connection stabelized! ")
            return connection
        except (Exception, psycopg2.Error) as error:
            print ("Error while connecting to PostgreSQL :{}".format(error))

class PostGisConnectionPool:
    """

    PostGisConnectionPool

    Args:
        pg_source (dic): Python object (dict) with connection info

    """
    def __init__(self, pg_source):
        self.datasource = pg_source
        self.open_conection()

    def __del__(self):
        self.close_connection()

    def open_conection(self):
        self.pg_connection = PostgisConnection.connection_open(self.datasource.get_connection_info())

    def close_connection(self):
        # self.pg_connection.cursor().close()
        self.pg_connection.close()

    def execute_query(self, sql):
        cur = self.pg_connection.cursor()
        cur.execute(sql)
        return cur.fetchall()
        # with self.pg_connection.cursor() as cursor:
        #     cursor.execute(sql)
            # for cs in cursor.fetchall():
            #     result = cs
            # cursor.close()

    def get_connection(self):
        return self.pg_connection


class DataSource(metaclass=ABCMeta):
    """docstring for ."""

    def __init__(self, id, m_conninfo):
        self._id = id
        self._connection_inf = m_conninfo

    def get_id(self):
        return self._id

    # def set_id(self, id):
    #     self._id = id

    def get_connection_info(self):
        return self._connection_inf

    # def set_connection_inf(self, m_conninfo):
    #     self._connection_inf = m_conninfo

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_trajectory(self, feature_type,temporal, x, y, obs, geom_property, classification_class,
                       start_date=None, end_date=None):
        pass


class PostGisDataSource(DataSource):
    """ PostGisDataSource Class """

    _connection_inf = {}

    def __init__(self, id, connection_info):
        super().__init__(id, connection_info)
        self.initialize()

    def initialize(self):
        self.open_connection()

    def get_type(self):
        return "POSTGIS"

    def open_connection(self):
        self.pg_poll = PostGisConnectionPool(self)
        self.pg_poll.open_conection()

    def close_connection(self):
        self.pg_poll.close_connection()
        print("Close Connection")

    def execute_query(self, sql):
        result = self.pg_poll.execute_query(sql)

        return  result
    def get_trajectory(self, feature_type,temporal, x, y, obs, geom_property, classification_class,
                       start_date=None, end_date=None):

        geom = Point(x, y)

        sql = "SELECT"

        where_sql = " WHERE ST_Intersects({}, ST_GeomFromText(\'{}\', {}))".format(geom_property["property_name"], geom.wkt,
                                                                                   geom_property['srid'])

        class_name = classification_class.get_name()

        class_id = classification_class.get_id()

        class_property_name = classification_class.get_class_property_name()

        temporal_type = temporal["type"]


        if(classification_class.get_type() == "Literal" and temporal_type == "STRING"):

            properties = " \'{}\' AS classe, \'{}\' AS data ".format(class_property_name, obs["temporal_property"])
            from_str = "FROM {}".format(feature_type)
            sql += properties + from_str + where_sql

            if (start_date):
                sql += " AND \'{}\' >= {}".format(obs["temporal_property"], start_date)

            if (end_date):
                sql += " AND \'{}\' <= {}".format(obs["temporal_property"], end_date)


        elif(classification_class.get_type() == "Literal" and temporal_type != "STRING"):

            properties = " \'{}\' AS classe, {} AS data ".format(class_property_name, obs["temporal_property"])
            from_str = "FROM {}".format(feature_type)
            sql += properties + from_str + where_sql

            if (start_date):
                sql += " AND {} >= {}".format(obs["temporal_property"], start_date)

            if (end_date):
                sql += " AND {} <= {}".format(obs["temporal_property"],end_date)


        elif (classification_class.get_type() != "Literal" and temporal_type == "STRING"):

            properties = " class.{} AS classe, \'{}\' AS data ".format(class_property_name, obs["temporal_property"])
            from_str = "FROM {} AS dado, {} AS class".format(feature_type, class_name)
            where_sql += " AND dado.{} = class.{} ".format(obs["class_property"], class_id)
            sql += properties + from_str + where_sql

            if (start_date):
                sql += " AND \'{}\' >= {}".format(obs["temporal_property"], start_date)

            if (end_date):
                sql += " AND \'{}\' <= {}".format(obs["temporal_property"], end_date)


        else:

            properties = " class.{} AS classe, {} AS data ".format(class_property_name, obs["temporal_property"])
            from_str = "FROM {} AS dado, {} AS class".format(feature_type, class_name)
            where_sql += " AND dado.{} = class.{} ".format(obs["class_property"], class_id)
            sql += properties + from_str + where_sql

            if (start_date):
                sql += " AND {} >= {}".format(obs["temporal_property"], start_date)

            if (end_date):
                sql += " AND {} <= {}".format(obs["temporal_property"], end_date)

        print(sql)
        # self.open_connection()

        return self.execute_query(sql)[0] if self.execute_query(sql) else None
        #
        # if(self.execute_query(sql)):
        #     result_query = self.execute_query(sql)[0]
        #
        # else:
        #     result_query = [None] * 2
        #     result_query[0] = "No Data found"
        #     result_query[1] = "No Data found"
        #
        # return result_query
        #

class WCSDataSource(DataSource):
    _connection_inf = {}

    def __init__(self, id, connection_info):
        super().__init__(id, connection_info)

    def get_type(self):
        return "WCS"

    def get_trajectory(self, feature_type, temporal, x, y, obs, geom_property, classification_class,
                       start_date = None, end_date = None):
        return


class WFSDataSource(DataSource):
    _connection_inf = {}

    def __init__(self, id, connection_info):
        super().__init__(id, connection_info)

    def get_type(self):
        return "WFS"

    def get_trajectory(self, feature_type,temporal, x, y, obs, geom_property, classification_class,
                       start_date=None, end_date=None):
        return

        # def open(self):
        #     self.wfs_poll = WFSConnectionPool(self.get_connection_info())
        #     self.wfs_poll.openConection()


        # def close(self):
        #     print("close")


class DataSourceFactory:
    """docstring for """

    @staticmethod
    def make(dsType, id, connInfo):
        factorys = {"POSTGIS": "PostGisDataSource", "WCS": "WCSDataSource", "WFS": "WFSDataSource"}
        datasource = eval(factorys[dsType])(id, connInfo)
        return datasource


class DataSourceManager:
    """docstring for ."""

    _datasources = {
        "webservice_source": [],
        "dbms_source": [],
        "file_source": []
    }

    __instance = None

    def __init__(self):
        """ Virtually private constructor. """

        print("Inicializando DatasourceManager")
        if DataSourceManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DataSourceManager.__instance = self
            DataSourceManager.__instance.load_all()

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DataSourceManager.__instance == None:
            DataSourceManager()
        return DataSourceManager.__instance

    def get_datasource(self, ds_id):

        try:
            for ds_list in self._datasources.values():
                for ds in ds_list:
                    if (ds.get_id() == ds_id):
                        return ds
        except:
            return None

    def insert_datasource(self, dsType, connInfo):
        self._datasources[dsType].append(DataSourceFactory.make(connInfo["type"], connInfo["id"], connInfo))

    def load_all(self):

        config_file = config_folder / 'wlts_config.json'

        with config_file.open()  as json_data:

            config = json_loads(json_data.read())

            if "datasources" not in config:
                raise ValueError("No datasource in json config file")
            else:
                datasources = config["datasources"]

                for dstype, datasources_info in datasources.items():
                    for ds_info in datasources_info:
                        self.insert_datasource(dstype, ds_info)


datasource_manager = DataSourceManager()