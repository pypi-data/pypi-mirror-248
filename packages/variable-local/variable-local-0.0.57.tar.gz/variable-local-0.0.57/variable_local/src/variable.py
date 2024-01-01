from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from dotenv import load_dotenv
from language_local.lang_code import LangCode
from logger_local.Logger import Logger

from .constants import variable_local_logger_init_object

# from src.template import ReplaceFieldsWithValues
load_dotenv()

logger = Logger.create_logger(object=variable_local_logger_init_object)


class VariablesLocal(GenericCRUD):
    # TODO Shall we run the constructor of GenericCRUD
    def __init__(self):
        # TODO: integrate with GenericCRUD
        self.name2id_dict = {}
        self.id2name_dict = {}
        self.next_variable_id = 1
        self.connector = Connector.connect('field')
        self.cursor = self.connector.cursor(dictionary=True, buffered=True)
        variable_names_dict = self.load_variable_names_dict_from_variable_table()
        for variable_id in variable_names_dict:
            self.add(variable_id=variable_id,
                     variable_name=variable_names_dict[variable_id])

    def add(self, variable_id: int, variable_name: str) -> None:
        logger.start(object={'variable_id': variable_id,
                             'variable_name': variable_name})
        try:
            if variable_id is not None and variable_name is not None:
                self.name2id_dict[variable_name] = variable_id
                self.id2name_dict[variable_id] = variable_name
            # TODO: just make bad performance, seems that can be removed
            # self.cursor.execute("""INSERT INTO variable_table(variable_id, name) VALUES (%s, %s)""", [
            #                     variable_id, variable_name])
            # GenericCRUD(schema_name=VARIABLE_LOCAL_SCHEMA_NAME).insert(
            #     table_name='variable_table', json_data={'variable_id': variable_id, 'name': variable_name})
            # self.connector.commit()

        # TODO change ex to exception
        except Exception as ex:
            message = 'error: Failed to add variable'
            logger.exception(message, object=ex)
            logger.end()
            raise
        logger.end()

    def get_variable_id_by_variable_name(self, variable_name: str) -> int:
        logger.start(object={'variable_name': variable_name})
        variable_id = self.name2id_dict.get(variable_name)
        logger.end(object={'variable_id': variable_id})
        return variable_id

    def get_variable_name_by_variable_id(self, variable_id: int) -> str:
        logger.start(object={'variable_id': variable_id})
        variable_name = self.id2name_dict[variable_id]
        logger.end(object={'variable_name': variable_name})
        logger.end(object={'variable_name': variable_name})
        return variable_name

    def get_variable_value_by_variable_name_and_lang_code(self, variable_name: str, lang_code: LangCode) -> str:
        logger.start(object={'lang_code': lang_code,
                             'variable_name': variable_name})
        variable_id = self.get_variable_id_by_variable_name(
            variable_name=variable_name)
        variable_value = VariablesLocal.get_variable_value_by_variable_id(
            lang_code=lang_code, variable_id=variable_id)
        logger.end(object={'variable_value': variable_value})
        return variable_value

    @staticmethod
    def set_variable_value_by_variable_id(variable_id: int, variable_value: str) -> None:
        logger.start(object={'variable_id': variable_id,
                             'variable_value': variable_value})
        connection = Connector.connect('logger')
        cursor = connection.cursor(dictionary=True, buffered=True)
        # TOOD Use our database package 
        # TODO I believe we should keep more fields
        cursor.execute(
            """INSERT INTO logger_table(variable_id, variable_value_new) VALUES (%s, %s)""",
            (variable_id, variable_value))
        logger.end()

    @staticmethod
    def get_variable_value_by_variable_id(variable_id: int, lang_code: LangCode, profile_id: int = None) -> str:
        connection = Connector.connect('logger')
        cursor = connection.cursor(dictionary=True, buffered=True)
        logger.start(object={'lang_code': lang_code,
                             'variable_id': variable_id})
        params = (variable_id, profile_id) if profile_id is not None else (variable_id,)
        # TODO Change to our database-mysql-python-package
        query = ("SELECT variable_value_new " +
                 "FROM logger_dialog_workflow_state_history_view "
                 "WHERE variable_id= %s AND variable_value_new IS NOT NULL " +
                 (f"AND profile_id= %s " if profile_id is not None else "") +
                 "ORDER BY timestamp DESC")
        cursor.execute(query, params)
        result = cursor.fetchone()
        if not result:
            if profile_id is not None:
                return VariablesLocal.get_variable_value_by_variable_id(variable_id=variable_id, lang_code=lang_code)
            else:
                # No value found for variable XYZ
                logger.warn("No variable value found")
        variable_value = result["variable_value_new"]
        # GenericCRUD_instance=GenericCRUD(schema_name='dialog_workflow')
        # GenericCRUD_instance.cursor=GenericCRUD_instance.connection.cursor(dictionary=True,buffered=True)
        # variable_value = GenericCRUD_instance.select_one(table_name='dialog_workflow_state_history_view',select_clause_value='variable_value_new',
        #                                                                                   where='variable_id= {} ORDER BY timestamp DESC' .format(variable_id))
        logger.end(object={'variable_value': variable_value})
        return variable_value

    @staticmethod
    def load_variable_names_dict_from_variable_table(person_id: int = None) -> dict:
        logger.start()
        connection = Connector.connect('field')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("""SELECT variable_id, name FROM variable_view""")
        # TODO Add logger.info()
        if person_id is not None:
            cursor.execute("SELECT variable_id, name FROM variable_view WHERE person_id = %s", person_id)
        else:
            cursor.execute("SELECT variable_id, name FROM variable_view")
        rows = cursor.fetchall()
        # rows = GenericCRUD(schema_name=VARIABLE_LOCAL_SCHEMA_NAME).select(table_name='variable_table',id_column_name=['variable_id','name'])
        data = {}
        # backward_data = {}
        for row in rows:
            variable_id, variable_name = row['variable_id'], row['name']
            # backward_data[variable_name] = variable_id
            data[variable_id] = variable_name
        logger.end(object={'data': data})
        return data
