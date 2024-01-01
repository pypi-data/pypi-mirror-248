from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from phonenumbers import parse, NumberParseException, format_number, PhoneNumberFormat
from .phone_local_constans import code_object_init


logger = Logger.create_logger(object=code_object_init)


class PhonesLocal(GenericCRUD):
    def __init__(self) -> None:
        GenericCRUD.__init__(self, default_schema_name="phone",
                             default_table_name="phone_table",
                             default_view_table_name="phone_view",
                             default_id_column_name="phone_id")

    def get_normalized_phone_number_by_phone_id(self, phone_id: int) -> int:
        logger.start(object={"phone_id": phone_id})
        data = self.select_one_dict_by_id(select_clause_value="local_number_normalized",
                                          id_column_value=phone_id)
        if not data:
            logger.end("No phone number found for phone_id " +
                       str(phone_id))
            return None
        phone_number = int(data["local_number_normalized"])
        logger.end("Return Phone Number of a specific phone id",
                   object={'phone_number': phone_number})
        return phone_number

    def verify_phone_number(self, phone_number: int) -> None:
        logger.start(object={"phone_number": phone_number})
        self.update_by_id(id_column_value=phone_number,
                          data_json={"is_verified": 1})
        logger.end()

    def is_verified(self, phone_number: int) -> bool:
        logger.start(object={"phone_number": phone_number})
        data = self.select_one_dict_by_id(select_clause_value="is_verified",
                                          id_column_value=phone_number)
        if not data:
            logger.end("No phone number found for phone_number " +
                       str(phone_number))
            return False
        is_verified = data["is_verified"]
        logger.end("Return is_verified of a specific phone id",
                   object={'is_verified': is_verified})
        return is_verified

    def normalize_phone_number(self, original_number: str, region: str) -> dict:
        try:
            parsed_number = parse(original_number, region)
            international_code = parsed_number.country_code
            full_number_normalized = format_number(
                parsed_number, PhoneNumberFormat.E164)
            number_info = {
                "international_code": international_code,
                "full_number_normalized": full_number_normalized
            }
            return number_info
        except NumberParseException as e:
            logger.error(
                f"Invalid phone number: {original_number}. Exception: {str(e)}")
            return None

    def get_test_phone_id(self) -> int:
        logger.start()
        phone_id = self.select_one_tuple_by_id(select_clause_value="phone_id",
                                               id_column_value=1)[0]
        logger.end()
        return phone_id
