import os
from typing import Dict
from opencage.geocoder import OpenCageGeocode
from .location_local_constants import LocationLocalConstants
from .country_ml import CountryMl
from .point import Point
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa
from logger_local.Logger import Logger  # noqa: E402
from language_local.lang_code import LangCode  # noqa: E402
api_key = os.getenv("OPENCAGE_KEY")

logger = Logger.create_logger(object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)  # noqa501


class Country(GenericCRUD):
    country_ml = CountryMl()

    def __init__(self):
        logger.start("start init Country")

        super().__init__(default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,  # noqa501
                         default_table_name=LocationLocalConstants.COUNTRY_TABLE_NAME,  # noqa501
                         default_view_table_name=LocationLocalConstants.COUNTRY_VIEW_NAME,  # noqa501
                         default_id_column_name=LocationLocalConstants.COUNTRY_ID_COLUMN_NAME)  # noqa501

        logger.end("end init Country")

    def insert(self, country: str, lang_code: LangCode,
               title_approved: bool = False,
               new_country_data: Dict[str, any] = None,
               coordinate: Point = None) -> int:
        logger.start("start insert country",
                     object={'coordinate': coordinate, 'country': country,
                             'lang_code': lang_code,
                             'title_approved': title_approved,
                             'new_country_data': new_country_data})

        new_country_data = new_country_data or {}
        try:
            country_json = {
                key: value for key, value in {
                    'coordinate': coordinate,
                    'iso': new_country_data.get("iso"),
                    'name': country,
                    'nicename': new_country_data.get("nicename"),
                    'iso3': new_country_data.get("iso3"),
                    'numcode': new_country_data.get("numcode"),
                    'phonecode': new_country_data.get("phonecode")
                }.items() if value is not None
            }
            country_id = super().insert(data_json=country_json)

        except Exception as e:
            logger.exception("error in insert country")
            logger.end()
            raise e
        try:
            country_ml_id = self.country_ml.insert(country=country,
                                                   country_id=country_id,
                                                   lang_code=lang_code,
                                                   title_approved=title_approved)  # noqa501
        except Exception as e:
            logger.exception("error in insert country")
            logger.end()
            raise e
        logger.end("end insert country",
                   object={'country_id': country_id,
                           'country_ml_id': country_ml_id})
        return country_id

    def read(self, location_id: int):
        logger.start("start read location",
                     object={'location_id': location_id})
        result = super().select_one_dict_by_id(id_column_value=location_id,
                                                select_clause_value=LocationLocalConstants.COUNTRY_TABLE_COLUMNS)  # noqa501

        logger.end("end read location",
                   object={"result": result})  # noqa 501
        return result

    @staticmethod
    def get_country_id_by_country_name(country_name: str) -> int:
        logger.start("start get_country_id_by_country_name",
                     object={'country_name': country_name})

        country_id_json = Country.country_ml.select_one_dict_by_where(select_clause_value=LocationLocalConstants.COUNTRY_ID_COLUMN_NAME,  # noqa501
                                                                                     where=f"title='{country_name}'")  # noqa501
        country_id = country_id_json.get(LocationLocalConstants.COUNTRY_ID_COLUMN_NAME)  # noqa501

        logger.end("end get_country_id_by_country_name",
                   object={'country_id': country_id})
        return country_id

    @staticmethod
    def get_country_name(location):
        # Create a geocoder instance
        logger.start("start get_country_name",
                     object={'location': location})

        # Define the city or state
        geocoder = OpenCageGeocode(api_key)

        # Use geocoding to get the location details
        results = geocoder.geocode(location)

        if results and len(results) > 0:
            first_result = results[0]
            components = first_result['components']

            # Extract the country from components
            country_name = components.get('country', '')
            if not country_name:
                # If country is not found, check for country_code as an alternative  # noqa501
                country_name = components.get('country_code', '')
        else:
            country_name = None
            logger.error("country didnt  found for %s." % location)
        logger.end("end get_country_name",
                   object={'country_name': country_name})
        return country_name
