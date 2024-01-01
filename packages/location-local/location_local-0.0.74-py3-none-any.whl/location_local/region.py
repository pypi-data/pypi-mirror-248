from .location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
from .region_ml import RegionMl
from .point import Point
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa
from logger_local.Logger import Logger  # noqa: E402
from language_local.lang_code import LangCode  # noqa: E402

logger = Logger.create_logger(object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)  # noqa501


class Region(GenericCRUD):
    region_ml = RegionMl()

    def __init__(self):
        logger.start("start init Region")
        super().__init__(default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,  # noqa501
                         default_table_name=LocationLocalConstants.REGION_TABLE_NAME,  # noqa501
                         default_view_table_name=LocationLocalConstants.REGION_VIEW_NAME,  # noqa501
                         default_id_column_name=LocationLocalConstants.REGION_ID_COLUMN_NAME)  # noqa501

        logger.end("end init Region")

    def insert(
            self, coordinate: Point,
            region: str, lang_code: LangCode, title_approved: bool = False,
            country_id: int = None, group_id: int = None) -> int:
        logger.start("start insert Region",
                     object={'coordinate': coordinate, 'region': region,
                             'lang_code': lang_code,
                             'title_approved': title_approved,
                             'country_id': country_id, 'group_id': group_id})
        region_json = {
                key: value for key, value in {
                    'coordinate': coordinate,
                    'country_id': country_id,
                    'group_id': group_id
                }.items() if value is not None
            }

        region_id = super().insert(data_json=region_json)

        region_ml_id = self.region_ml.insert(region_id=region_id,
                                             region=region,
                                             lang_code=lang_code,
                                             title_approved=title_approved)

        logger.end("end insert region",
                   object={'region_id': region_id,
                           'region_ml_id': region_ml_id})
        return region_id

    def read(self, location_id: int):
        logger.start("start read location",
                     object={'location_id': location_id})
        result = super().select_one_dict_by_id(id_column_value=location_id,
                                                select_clause_value=LocationLocalConstants.REGION_TABLE_COLUMNS)  # noqa501

        logger.end("end read location",
                   object={"result": result})  # noqa 501
        return result

    @staticmethod
    def get_region_id_by_region_name(region_name: str, country_id: int = None) -> int:  # noqa501
        logger.start("start get_region_id_by_region_name",
                     object={'region_name': region_name,
                             'country_id': country_id})

        region_id_json = Region.region_ml.select_one_dict_by_where(select_clause_value=LocationLocalConstants.REGION_ID_COLUMN_NAME,  # noqa501
                                                                                     where=f"title='{region_name}'")  # noqa501
        region_id = region_id_json.get(LocationLocalConstants.REGION_ID_COLUMN_NAME)  # noqa501

        logger.end("end get_region_id_by_region_name",
                   object={'region_id': region_id})
        return region_id
