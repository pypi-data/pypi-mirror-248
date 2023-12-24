from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud import GenericCRUD

PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 190
PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "profile_profile_local"
DEVELOPER_EMAIL = "idan.a@circ.zone"
SCHEMA_NAME = "profile_profile"
PROFILE_PROFILE_TABLE_NAME = "profile_profile_table"
PROFILE_PROFILE_VIEW_TABLE_NAME = "profile_profile_view"
PROFILE_PROFILE_ID_COLUMN_NAME = "profile_profile_id"
obj = {
    'component_id': PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

logger = Logger.create_logger(object=obj)


class ProfileProfile(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name=SCHEMA_NAME, default_table_name=PROFILE_PROFILE_TABLE_NAME,
                         default_view_table_name=PROFILE_PROFILE_VIEW_TABLE_NAME,
                         default_id_column_name=PROFILE_PROFILE_ID_COLUMN_NAME)

    def insert_profile_profile(self, profile_id1: int, profile_id2: int, relationship_type_id: int,
                               job_title: str = None, is_test_data : bool = False) -> int:
        json = {
            'profile_id1': profile_id1,
            'profile_id2': profile_id2,
            'relationship_type_id': relationship_type_id,
            'job_title': job_title,
            'is_test_data': is_test_data
        }
        logger.start(object=json)
        data = {
            'profile_id1': profile_id1,
            'profile_id2': profile_id2,
            'relationship_type_id': relationship_type_id,
            'job_title': f"'{job_title}'",
            'is_test_data': is_test_data
        }
        # TODO Please use parameter by name to make the code more readable
        profile_profile_id = self.insert(data_json=data)
        logger.end(object={"profile_profile_id": profile_profile_id})
        return profile_profile_id

    def update_profile_profile_by_profile_profile_id(self, profile_profile_id: int, profile_profile_json: object) -> None:
        json = {
            'data': profile_profile_json
        }
        logger.start(object=json)
        self.update_by_id(data_json=profile_profile_json,
                          id_column_value=profile_profile_id)
        logger.end("profile_profile updated")

    def delete_by_profile_profile_id(self, profile_profile_id: int) -> None:
        json = {
            "profile_profile_id": profile_profile_id,
        }
        logger.start(object=json)
        self.delete_by_id(id_column_value=profile_profile_id)
        logger.end("profile_profile deleted")

    def get_by_profile_profile_id(self, profile_profile_id: int) -> any:
        json = {
            "profile_profile_id": profile_profile_id
        }
        logger.start(object=json)
        profile_profile_record = self.select_multi_tuple_by_id(
            id_column_value=profile_profile_id)
        logger.end(
            object={"profile_profile_record": str(profile_profile_record)})
        return profile_profile_record
