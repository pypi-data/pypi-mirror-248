from typing import Any
import re

from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from language_local.lang_code import LangCode
from user_context_remote.user_context import UserContext

from .generic_crud import GenericCRUD
from .connector import Connector
from .utils import validate_select_table_name

# Constants
DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_ID = 206
DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_NAME = 'circles_local_database_python\\generic_crud_ml'
DEVELOPER_EMAIL = 'tal.g@circ.zone'
DEFAULT_LIMIT = 100

user_context = UserContext()
user = user_context.login_using_user_identification_and_password()

# Logger setup
logger = Logger.create_logger(object={
    'component_id': DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_ID,
    'component_name': DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
})
'''
city_id = cityMl.add_value( None, ENGLISH, "Jerusalem"...)
cityMl.add_value( city_id, HEBREW, "ירושלים"...)
city_name_english = cityML.get_value( city_id, ENGLISH)
get_id_by_name( name: str, lang_code: LangCode = None) -> int
'''

TEST_TABLE_NAME = 'test_mysql_table'
TEST_ML_TABLE_NAME = 'test_mysql_ml_table'


class GenericCRUDML(GenericCRUD):
    """A class that provides generic CRUD functionality for tables with multi-language support."""

    def __init__(self, default_schema_name: str, default_table_name: str = None,
                 default_ml_table_name: str = None,
                 default_view_table_name: str = None,
                 default_id_column_name: str = None,
                 connection: Connector = None) -> None:
        """Initializes the GenericCRUDML class. If connection is not provided,
        a new connection will be created."""
        logger.start(object={"default_schema_name": default_schema_name,
                             "default_table_name": default_table_name,
                             "id_column_name": default_id_column_name})
        super().__init__(default_schema_name=default_schema_name, default_table_name=default_table_name,
                         default_view_table_name=default_view_table_name, default_id_column_name=default_id_column_name,
                         connection=connection)
        if default_table_name is not None or default_ml_table_name is not None:
            self.default_ml_table_name = default_ml_table_name or re.sub(r'(_table)$', '_ml\\1', default_table_name)
        logger.end()

    def add_value(self, id: int = None, lang_code: LangCode = user_context.get_effective_profile_preferred_lang_code(),
                  data_json: dict[str, any] = None, data_ml_json: dict = None,
                  table_name: str = None, ml_table_name: str = None,
                  view_name: str = None) -> tuple[int, int]:
        logger.start(object={"id": id, "lang_code": lang_code, "data_json": data_json, "data_ml_json": data_ml_json,
                             "table_name": table_name, "ml_table_name": ml_table_name, "view_name": view_name})
        if lang_code is None:
            lang_code = 'en'

        table_name = table_name or self.default_table_name
        ml_table_name = ml_table_name or self.default_ml_table_name
        view_name = view_name or self.default_view_table_name

        # id is the id value of the row in the table_name table
        if id is None:
            id = self.insert(data_json=data_json, ignore_duplicate=True)
            if id is None:
                logger.error("Error inserting data_json", object={"data_json": data_json})
                logger.end()
                return None

        id_column_name = re.sub(r'(_table)$', '_id', table_name)
        data_ml_json[id_column_name] = id
        data_ml_json["lang_code"] = lang_code

        # ml_id is the id value of the row in the ml_table_name table
        ml_id = self.insert(data_json=data_ml_json, table_name=ml_table_name, ignore_duplicate=True)

        logger.end(object={"id": id, "ml_id": ml_id})
        return id, ml_id

    def get_values_tuple(self, id: int, lang_code: LangCode = user_context.get_effective_profile_preferred_lang_code(),
                         id_column_name: str = None) -> tuple:
        logger.start(object={"id": id, "lang_code": lang_code})
        if lang_code is None:
            lang_code = 'en'

        try:
            id_column_name = id_column_name or re.sub(r'(_table)$', '_id', self.default_table_name)
        except Exception:
            message = "id_column_name was not provided and could not be generated from default_table_name"
            logger.error(message)
            logger.end()
            raise Exception(message)
        result = self.select_one_tuple_by_where(where=f"{id_column_name}=%s AND lang_code=%s",
                                                params=(id, lang_code))
        logger.end(object={"result": result})
        return result

    def get_values_dict(self, id: int, lang_code: LangCode = user_context.get_effective_profile_preferred_lang_code(),
                        id_column_name: str = None) -> dict:
        logger.start(object={"id": id, "lang_code": lang_code})
        if lang_code is None:
            lang_code = 'en'

        try:
            id_column_name = id_column_name or re.sub(r'(_table)$', '_id', self.default_table_name)
        except Exception:
            message = "id_column_name was not provided and could not be generated from default_table_name"
            logger.error(message)
            logger.end()
            raise Exception(message)
        result = self.select_one_dict_by_where(where=f"{id_column_name}=%s AND lang_code=%s",
                                               params=(id, lang_code))
        logger.end(object={"result": result})
        return result

    def get_id_by_name(self, name: str, lang_code: LangCode = user_context.get_effective_profile_preferred_lang_code(),
                       id_column_name: str = None) -> int:
        logger.start(object={"name": name, "lang_code": lang_code})
        if lang_code is None:
            lang_code = 'en'

        try:
            id_column_name = id_column_name or re.sub(r'(_table)$', '_id', self.default_table_name)
        except Exception:
            message = "id_column_name was not provided and could not be generated from default_table_name"
            logger.error(message)
            logger.end()
            raise Exception(message)
        try:
            result = self.select_one_tuple_by_where(select_clause_value=id_column_name,
                                                    where="title=%s AND lang_code=%s",
                                                    params=(name, lang_code))
        except Exception:
            logger.warn("select_one_tuple_by_where was not successful for name and lang_code",
                        object={"title": name, "lang_code": lang_code})
            try:
                result = self.select_one_tuple_by_where(select_clause_value=id_column_name,
                                                        where="`name`=%s AND lang_code=%s",
                                                        params=(name, lang_code))
            except Exception:
                logger.warn("select_one_tuple_by_where was not successful for name and lang_code",
                            object={"name": name, "lang_code": lang_code})
                logger.end()
                raise
        logger.end(object={"result": result})
        if result:
            return result[0]
        else:
            return None

    def get_ml_id_by_name(self, name: str,
                          lang_code: LangCode = user_context.get_effective_profile_preferred_lang_code(),
                          id_column_name: str = None) -> int:
        logger.start(object={"name": name, "lang_code": lang_code})
        if lang_code is None:
            lang_code = 'en'

        try:
            ml_id_column_name = id_column_name or re.sub(r'(_table)$', '_id', self.default_ml_table_name)
        except Exception:
            message = "id_column_name was not provided and could not be generated from default_table_name"
            logger.error(message)
            logger.end()
            raise Exception(message)
        try:
            result = self.select_one_tuple_by_where(select_clause_value=ml_id_column_name,
                                                    where="title=%s AND lang_code=%s",
                                                    params=(name, lang_code))
        except Exception:
            logger.warn("select_one_tuple_by_where was not successful for name and lang_code",
                        object={"title": name, "lang_code": lang_code})
            try:
                result = self.select_one_tuple_by_where(select_clause_value=ml_id_column_name,
                                                        where="`name`=%s AND lang_code=%s",
                                                        params=(name, lang_code))
            except Exception:
                logger.warn("select_one_tuple_by_where was not successful for name and lang_code",
                            object={"name": name, "lang_code": lang_code})
                logger.end()
                raise
        logger.end(object={"result": result})
        return result[0]

    def delete_by_name(self, name: str,
                       lang_code: LangCode = user_context.get_effective_profile_preferred_lang_code()) -> None:
        logger.start(object={"name": name, "lang_code": lang_code})
        if lang_code is None:
            lang_code = 'en'

        try:
            self.delete_by_where(table_name=TEST_ML_TABLE_NAME, where="title=%s AND lang_code=%s", params=(name, lang_code))
        except Exception:
            logger.warn("delete_by_where was not successful for name and lang_code",
                        object={"title": name, "lang_code": lang_code})
            try:
                self.delete_by_where(table_name=TEST_ML_TABLE_NAME,
                                     where="`name`=%s AND lang_code=%s", params=(name, lang_code))
            except Exception:
                logger.warn("delete_by_where was not successful for name and lang_code",
                            object={"name": name, "lang_code": lang_code})
                logger.end()
                raise
        logger.end()

    # The follwing methods may be irrelevant since GenericCRUD has equivalent methods
    # TODO: We may want to remove these following methods

    # This method returns the value in a selected column by a condition, the condition can be none or a value
    # for a specific column
    def select_one_by_value_with_none_option(
            self, condition_column_name, condition_column_value,
            view_table_name: str = None,
            select_column_name: str = None) -> Any:
        view_table_name = view_table_name or self.default_view_table_name
        # Returns the row id if select_column_name is None
        select_column_name = select_column_name or self.default_column
        """Selects a column from the table based on a WHERE clause and returns it as a list of dictionaries."""
        logger.start(
            object={"table_name": view_table_name,
                    "select_column_name": select_column_name,
                    "condition_column_name": condition_column_name,
                    "condition_column_value": condition_column_value})
        validate_select_table_name(view_table_name)
        select_query = f"SELECT {select_column_name} " f"FROM {self.schema_name}.{view_table_name} " + (
            f"WHERE `{condition_column_name}` = \"{condition_column_value}\" " if (condition_column_name and
                                                                                   condition_column_value)
            else f"WHERE `{condition_column_name}` IS NULL ")
        try:
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
            # Extract the first element from the first tuple in the result
            result = result[0][0] if result else None
            logger.end(object={"result": str(result)})
            return result
        except Exception as e:
            logger.exception(self._log_error_message(message="Error selecting data_json",
                                                     sql_statement=select_query), object=e)
            logger.end()
            raise

    def select_multi_tuple_by_value_with_none_option(self,
                                                     condition_column_name,
                                                     condition_column_value,
                                                     view_table_name: str = None, select_clause_value: str = "*",
                                                     limit: int = DEFAULT_LIMIT, order_by: str = "") -> list:
        view_table_name = view_table_name or self.default_view_table_name
        # Returns the row id if select_column_name is None
        select_column_name = f"`{select_clause_value}`" if select_clause_value != "*" else "*"
        """Selects a column from the table based on a WHERE clause and returns it as a list of dictionaries."""
        logger.start(
            object={"table_name": view_table_name,
                    "select_column_name": select_column_name,
                    "condition_column_name": condition_column_name,
                    "condition_column_value": condition_column_value})
        validate_select_table_name(view_table_name)
        select_query = f"SELECT {select_column_name} " f"FROM {self.schema_name}.{view_table_name} " + (
            f"WHERE `{condition_column_name}` = \"{condition_column_value}\" " if (condition_column_name and
                                                                                   condition_column_value)
            else f"WHERE {condition_column_name} IS NULL ") + (
                           f"ORDER BY {order_by} " if order_by else "") + f"LIMIT {limit}"
        try:
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
            logger.end("Data selected successfully.",
                       object={"result": str(result)})
            return result
        except Exception as e:
            logger.exception(self._log_error_message(message="Error selecting data_json",
                                                     sql_statement=select_query), object=e)
            logger.end()
            raise

    def select_multi_dict_by_value_with_none_option(self,
                                                    condition_column_name,
                                                    condition_column_value,
                                                    view_table_name: str = None, select_clause_value: str = "*",
                                                    limit: int = DEFAULT_LIMIT, order_by: str = "") -> list:
        """Selects a column from the table based on a WHERE clause and returns it as a list of dictionaries."""
        result = self.select_multi_tuple_by_value_with_none_option(condition_column_name, condition_column_value,
                                                                   view_table_name=view_table_name,
                                                                   select_clause_value=select_clause_value,
                                                                   limit=limit, order_by=order_by)
        return [self._convert_to_dict(row, select_clause_value) for row in result]
