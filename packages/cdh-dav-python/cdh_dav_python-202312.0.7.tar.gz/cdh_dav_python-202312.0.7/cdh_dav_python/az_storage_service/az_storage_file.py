from azure.storage.filedatalake import DataLakeServiceClient


class AzStorageFile:
    @staticmethod
    def get_file_size(
        account_url: str, credential, storage_container: str, file_path: str
    ):
        """
        Retrieves the size of a file in a Azure Data Lake Storage account.

        Args:
            account_url (str): The name of the Azure Storage account.
            account_key (str): The access key for the Azure Storage account.
            storage_container (str): The name of the file system in the Azure Data Lake Storage account.
            file_path (str): The path to the file in the file system.

        Returns:
            int: The size of the file in bytes.

        Raises:
            Exception: If there is an error retrieving the file properties.
        """
        service_client = DataLakeServiceClient(
            account_url=account_url,
            credential=credential,
        )
        file_system_client = service_client.get_file_system_client(storage_container)
        file_client = file_system_client.get_file_client(file_path)

        try:
            file_props = file_client.get_file_properties()
            return file_props.size  # Returns the size of the file in bytes
        except Exception as e:
            print(e)
            return None
