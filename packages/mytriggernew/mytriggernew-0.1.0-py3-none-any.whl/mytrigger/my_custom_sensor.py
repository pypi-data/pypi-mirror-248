from datetime import datetime, timedelta
from airflow import DAG

import asyncio
from airflow.models import BaseOperator
from typing import List, Dict, AsyncIterator, Any, Tuple
from airflow.providers.google.cloud.triggers.gcs import GCSPrefixBlobTrigger
from datetime import timedelta
from airflow.triggers.base import BaseTrigger, TriggerEvent
from aiohttp import ClientSession
class MultiGCSPrefixBlobTrigger(BaseTrigger):
    def __init__(
            self,
            locations: List[Dict[str, str]],
            poke_interval: float,
            google_cloud_conn_id: str,
            hook_params: dict,
    ):

        print("inside INIT MultiGCSPrefixBlobTrigger")
        # print(f"location {locations}")
        super().__init__(poke_interval=poke_interval)
        self.locations = locations
        self.poke_interval=poke_interval
        self.google_cloud_conn_id=google_cloud_conn_id
        self.hook_params=hook_params
        print(f"location {locations}")


    async def run(self) -> AsyncIterator[TriggerEvent]:
        try:
            hook = self._get_async_hook()
            status_dict = {}

            for location in self.locations:
                path = location["bucket"] + "/" + location["prefix"]
                status_dict[path] = True

            while True:
                for location in self.locations:

                    path = location["bucket"] + "/" + location["prefix"]
                    res = await self._list_blobs_with_prefix(
                        hook=hook, bucket_name=location["bucket"], prefix=location["prefix"]
                    )
                    if not res:
                        self.log.info(
                            "No matching blobs found in bucket %s with prefix %s",
                            location["bucket"] ,
                            location["prefix"],
                        )
                        status_dict[path] = False
                    self.log.info(status_dict)

                if all(status_dict.values()):
                    self.log.debug("inside found all files")
                    yield TriggerEvent(
                        {"status": "success", "message": "All files found", "matches": res}
                    )

                await asyncio.sleep(self.poke_interval)
        except Exception as e:
            yield TriggerEvent({"status": "error", "message": str(e)})



    async def _list_blobs_with_prefix(self, hook, bucket_name: str, prefix: str):
        self.log.info(f"looking for {bucket_name} {prefix}")
        async with ClientSession() as session:
            client = await hook.get_storage_client(session)
            bucket = client.get_bucket(bucket_name)
            object_response = await bucket.list_blobs(prefix=prefix)
            return object_response

    def serialize(self):
        return (
            "mytrigger.test..MultiGCSPrefixBlobTrigger",
            {
                "locations": self.locations,
                "poke_interval": self.poke_interval,
                "google_cloud_conn_id": self.google_cloud_conn_id,
                "hook_params": self.hook_params,
            },
        )
