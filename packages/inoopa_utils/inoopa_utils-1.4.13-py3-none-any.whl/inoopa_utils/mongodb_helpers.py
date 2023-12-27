import os
from dataclasses import asdict
from typing import Literal
from pymongo import MongoClient, UpdateOne

from inoopa_utils.custom_types.companies import Company, convert_dict_to_company
from inoopa_utils.custom_types.websites import CompanyWebsiteContent
from inoopa_utils.inoopa_logging import create_logger

class DbManagerMongo:
    """
    This class is used to manage the Mongo database (InfraV2).
    
    :param mongo_uri: The URI of the Mongo database to connect to.
    
    :method update_or_add_one_to_collection: Update or add a company or a website content to the database.
    :method add_or_update_many_to_collection: Update or add a list of companies or website contents to the database.
    :method find_one_from_collection: Get a company or a website content from the database.
    :method find_many_from_collection: Get a list of companies or website contents from the database.
    :method delete_one_from_collection: Delete a company or a website content from the database.
    """
    def __init__(self, mongo_uri: str = os.environ["MONGO_READWRITE_PROD_URI"]):
        self._loger = create_logger("INOOPA_UTILS.DB_MANAGER.MONGO")
        self._env = os.environ.get("ENV", "dev")

        _client = MongoClient(mongo_uri)
        _db = _client[self._env]

        self._company_collection = _db.get_collection("company")
        self._website_content_collection = _db.get_collection("website_content")


    def update_or_add_one_to_collection(self, data: Company | CompanyWebsiteContent) -> bool:
        """
        Update or add a company or a website content to the database.
        
        :param data: The company or website content to add or update.
        :return: True if the company or website was added, False if it was updated.
        """
        if isinstance(data, Company):
            self._company_collection.update_one(
                filter={"inoopa_id": data.inoopa_id},
                update={"$set": _prepare_entity_to_add(data)},
                upsert=True,
            )
            self._loger.info(f"Updated Company in collection {self._env} with ID: {data.inoopa_id}")
        elif isinstance(data, CompanyWebsiteContent):
            self._website_content_collection.update_one(
                filter={"url": data.url},
                update={"$set": _prepare_entity_to_add(data)},
                upsert=True,
            )
            self._loger.info(f"Updated WebsiteContent in collection {self._env} with url: {data.url}")
        else:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")

    def update_or_add_many_to_collection(self, data_list: list[Company | CompanyWebsiteContent]) -> None:
        """
        Update or add a list of companies or website contents to the database.
        
        :param data: The list of companies or website contents to add or update.
        """
        if all(isinstance(x, Company) for x in data_list):
            updates = [UpdateOne({"inoopa_id": x.inoopa_id}, {"$set": _prepare_entity_to_add(x)}, upsert=True) for x in data_list]
            query_result = self._company_collection.bulk_write(updates)
            self._loger.info(f"Updated: {query_result.modified_count} Companies in collection {self._env} with IDs: {[x.inoopa_id for x in data_list]}")
        elif all(isinstance(x, CompanyWebsiteContent) for x in data_list):
            updates = [UpdateOne({"url": x.url}, {"$set": _prepare_entity_to_add(x)}, upsert=True) for x in data_list]
            query_result = self._website_content_collection.bulk_write(updates)
            self._loger.info(f"Updated {query_result.modified_count} WebsiteContent in collection {self._env} with urls: {[x.url for x in data_list]}")
        else:
            raise TypeError(f"Can't update or add many data to mongo. Probably a mix of types in the list.")

    def find_one_from_collection(self, data: Company | CompanyWebsiteContent) -> Company | CompanyWebsiteContent | None:
        """
        Get a company or a website content from the database.
        
        :param index: The company or website index to get.
        :return: The company or website content if found, None otherwise.
        """
        if isinstance(data, Company):
            data_found = self._company_collection.find_one({"inoopa_id": data.inoopa_id})
            if data_found:
                self._loger.debug(f"Found data in database for company {data.inoopa_id}")
                return convert_dict_to_company(data_found)
        
        elif isinstance(data, CompanyWebsiteContent):
            data_found = self._website_content_collection.find_one({"url": data.url})
            if data_found:
                self._loger.debug(f"Found data in database for websitecontent {data.url}")
                return CompanyWebsiteContent(**data_found)
        else:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")

    def find_many_from_collection(self, data_list: list[Company | CompanyWebsiteContent]) -> list[Company | CompanyWebsiteContent] | None:
        """
        Get a list of companies or website contents from the database.

        :param data: The list of companies or website contents to get.
        :return: The list of companies or website contents if found, None otherwise.
        """
        if all(isinstance(x, Company) for x in data_list):
            all_ids = [x.inoopa_id for x in data_list]
            data_found = self._company_collection.find({"inoopa_id": {"$in": all_ids}})
            if data_found:
                self._loger.debug(f"Found data in database for companies {all_ids}")
                return [convert_dict_to_company(x) for x in data_found]
        elif all(isinstance(x, CompanyWebsiteContent) for x in data_list):
            all_ids = [x.url for x in data_list]
            data_found = self._website_content_collection.find({"url": {"$in": all_ids}})
            if data_found:
                self._loger.debug(f"Found data in database for websitecontent {all_ids}")
                return [CompanyWebsiteContent(**x) for x in data_found]
        else:
            raise TypeError(f"Can't update or add many data to mongo. Probably a mix of types in the list.")
        return None
        
    def find_one_company_from_id(self, id: str, id_type: Literal["company_number", "inoopa_id"] = "company_number") -> Company | None:
        """
        Get a list of companies from the database based on ids.
        
        :param id: company id to get.
        :return: The company if found, None otherwise.
        """
        
        if id_type == "company_number":
            data_found = self._company_collection.find_one({"company_number": id})
        elif id_type == "inoopa_id":
            data_found = self._company_collection.find_one({"inoopa_id": id})
        else:
            raise TypeError(f"id_type {id_type} is not supported. Use company_number or inoopa_id.")
        return convert_dict_to_company(data_found) if data_found else None

    def find_many_companies_from_id(self, ids = list[str], id_type: Literal["company_number", "inoopa_id"] = "company_number") -> list[Company] | None:
        """
        Get a list of companies from the database based on ids.
        
        :param ids: The list of companies ids to get.
        :return: The list of companies if found, None otherwise.
        """
        if type(ids) not in [list]:
            raise TypeError(f"You ids list is not a list. Type {type(ids)} is not supported.")
        
        if id_type == "company_number":
            data_found = self._company_collection.find({"company_number": {"$in": ids}})
        elif id_type == "inoopa_id":
            data_found = self._company_collection.find({"inoopa_id": {"$in": ids}})
        else:
            raise TypeError(f"id_type {id_type} is not supported. Use company_number or inoopa_id.")
        return [convert_dict_to_company(x) for x in data_found] if data_found else None

    def delete_one_from_collection(self, data: Company | CompanyWebsiteContent) -> None:
        """
        Delete a company or a website content from the database.
        
        :param data: The company or website content to delete.
        """
        
        if isinstance(data, Company):
            self._company_collection.delete_one({"inoopa_id": data.inoopa_id})
            self._loger.info(f"Deleted Company from collection {self._env} with ID: {data.inoopa_id}")
        
        elif isinstance(data, CompanyWebsiteContent):
            self._company_collection.delete_one({"url": data.url})
            self._loger.info(f"Deleted WebsiteContent from collection {self._env} with url: {data.url}")
        else:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")

    def delete_many_from_collection(self, data_list: list[Company | CompanyWebsiteContent]) -> None:
        """
        Delete a list of companies or website contents from the database.
        
        :param data: The list of companies or website contents to delete.
        """
        if all(isinstance(x, Company) for x in data_list):
            all_ids = [x.inoopa_id for x in data_list]
            self._company_collection.delete_many({"inoopa_id": {"$in": all_ids}})
            self._loger.info(f"Deleted Companies from collection {self._env} with IDs: {all_ids}")

        elif all(isinstance(x, CompanyWebsiteContent) for x in data_list):
            all_ids = [x.url for x in data_list]
            self._website_content_collection.delete_many({"url": {"$in": all_ids}})
            self._loger.info(f"Deleted WebsiteContent from collection {self._env} with url: {all_ids}")
        else:
            raise TypeError(f"Can't update or add many data to mongo. Probably a mix of types in the list.")


def _prepare_entity_to_add(data: Company | CompanyWebsiteContent) -> dict:
    """
    Prepare the entity to add to the database. Mainly remove _id field if None.
    
    :param data: The company or website content to add.
    """
    preapred_data = asdict(data)
    # This is to avoid sending None to mongo which will raise an error while keeping the _id field if it exists
    if preapred_data.get("_id") is None:
        del preapred_data["_id"]
    return preapred_data