import aiohttp

from hacktegic._internal.config import ConfigManager
from hacktegic._internal.credentials import Credentials
from hacktegic.cloud.resources.scanprofiles import ScanProfile


class ScanProfilesAPIClient:
    def __init__(self, credentials: Credentials, config_manager: ConfigManager) -> None:
        self.credentials = credentials
        self.config_manager = config_manager

    async def create(self, scanprofile: dict) -> ScanProfile:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/general/projects/{project_id}/scan_profiles"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.post(url, headers=headers, json=scanprofile) as response:
                response.raise_for_status()

                try:
                    return ScanProfile(**(await response.json()))
                except aiohttp.ContentTypeError:
                    print("Non-JSON response:", await response.text())
                    raise

    async def list(self) -> list[ScanProfile]:
        async with aiohttp.ClientSession() as session:
            url = f'{self.config_manager.config["api_base_url"]}v1/general/projects/{self.config_manager.config["project_id"]}/scan_profiles'
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.get(url, headers=headers) as response:
                return [ScanProfile(**i) for i in (await response.json())]

    async def describe(self, scanprofile_id: str) -> ScanProfile:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/general/projects/{project_id}/scan_profiles/{scanprofile_id}"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.get(url, headers=headers) as response:
                json_data = await response.json()

                return ScanProfile(**json_data)

    async def update(self, scanprofile_id: str, scanprofile: dict) -> bool:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/general/projects/{project_id}/scan_profiles/{scanprofile_id}"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}

            async with session.put(url, headers=headers, json=scanprofile) as response:
                result = response.status == 200

            return result

    async def delete(self, scanprofile_id: str) -> bool:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/general/projects/{project_id}/scan_profiles/{scanprofile_id}"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.delete(url, headers=headers) as response:
                return response.status == 200
