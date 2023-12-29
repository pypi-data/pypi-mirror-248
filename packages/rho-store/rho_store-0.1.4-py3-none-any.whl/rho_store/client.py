import time

import pandas as pd

from .adapters import RhoApiGraphqlAdapter, UploadFileHttpAdapter
from .config import init_config


class RhoClient:
    def __init__(self, api_key: str):
        self._config = init_config()
        self._api_port = RhoApiGraphqlAdapter(
            base_url=self._config.API_URL,
            api_key=api_key
        )
        self._file_upload_port = UploadFileHttpAdapter()

    def get_table_url(self, table_id: str, workspace_id: str) -> str:
        return f"{self._config.CLIENT_URL}/tables/{table_id}?wid={workspace_id}"

    def store_df(self, data: pd.DataFrame) -> str:
        t1 = time.time()
        url, file_id = self._api_port.get_signed_url()
        t2 = time.time()
        self._file_upload_port.upload_dataframe(url, data)
        t3 = time.time()
        table = self._api_port.process_file(file_id)
        t4 = time.time()
        print("- Get url: ", t2 - t1)
        print("- Upload file: ", t3 - t2)
        print("- Process file: ", t4 - t3)
        print("Total time: ", t4 - t1)
        table_id = table["id"]
        workspace_id = table["workspaceId"]
        return self.get_table_url(table_id, workspace_id)

    def store_data(self, data: list[dict]) -> str:
        df = pd.DataFrame(data)
        return self.store_df(df)

    def get_df(self, table_id: str) -> pd.DataFrame:
        data = self.get_data(table_id)
        parsed_data = pd.DataFrame(data)
        if "_id" in parsed_data.columns:
            parsed_data.drop(columns=["_id"], inplace=True)
        return parsed_data

    def get_data(self, table_id: str) -> list[dict]:
        t1 = time.time()
        data = self._api_port.get_data(table_id)
        t2 = time.time()
        print("Got data in: ", t2 - t1)
        return data


__all__ = ["RhoClient"]
