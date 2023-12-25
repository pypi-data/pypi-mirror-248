from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum

PHONE_LOCAL_PYTHON_COMPONENT_ID = 200
PHONE_LOCAL_PYTHON_COMPONENT_NAME = "phone_local_python_package/src/phones_local.py"
DEVELOPER_EMAIL = 'jenya.b@circ.zone'

object_init = {
    'component_id': PHONE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': PHONE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=object_init)


class PhonesLocal(GenericCRUD):
    def __init__(self) -> None:
        GenericCRUD.__init__(self, default_schema_name="phone",
                             default_table_name="phone_table",
                             default_view_table_name="phone_view",
                             default_id_column_name="phone_id")

    def get_phone_number_normalized_by_phone_id(self, phone_number: int) -> int:
        logger.start(object={"phone_number": phone_number})
        data = self.select_one_dict_by_id(select_clause_value="local_number_normalized",
                                          id_column_value=phone_number)
        if not data:
            logger.end("No phone number found for phone_number " + str(phone_number))
            return -1
        phone_number = int(data["local_number_normalized"])
        logger.end("Return Phone Number of a specific phone id", object={'phone_number': phone_number})
        return phone_number

    def verify_phone_number(self, phone_number: int) -> None:
        logger.start(object={"phone_number": phone_number})
        self.update_by_id(id_column_value=phone_number, data_json={"is_verified": 1})
        logger.end()
