import os
import pickle
from typing import Any

import requests


class RemoteException(Exception):
    def __init__(self, error_type: str, error: str):
        super().__init__(error)
        self.error_type = error_type

    def __str__(self):
        return f"<{self.error_type}> {self.args[0]}"


class NoSubscriptionException(Exception):
    pass


class RemoteModel:
    base_url: str = "https://departing.ai"  # "http://localhost:80"
    api_key: str
    model: str

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model
        self._call_url = f"{self.base_url}/api/v1/model/{self.model}/__call__"
        self._upload_url = f"{self.base_url}/api/v1/model/{self.model}/file"
        self._session = requests.Session()
        self._session.headers.update(
            {
                "x-api-key": self.api_key,
            }
        )

    def upload(
        self,
        model: Any,
        *,
        description: str = "Auto-upload",
        public: bool = False,
    ) -> None:
        """
        Upload the given model to create or update a remote model.

        `model` parameter should be an onnx file path.
        TODO: Add support for `torch` and `transformers`.
        """
        assert description, "Description cannot be empty"
        if not isinstance(model, str) or not os.path.exists(model):
            raise NotImplementedError(
                "Only ONNX file paths are supported for now"
            )
        response = self._session.put(
            self._upload_url,
            files={
                "file": (os.path.basename(model), open(model, "rb")),
            },
            data={
                "description": description,
                "public": str(public).lower(),
            },
        )
        if response.status_code // 100 != 2:
            raise RemoteException(
                "ModelUploadFailed", response.content.decode("utf8")
            )

    def __call__(self, *args, **kwargs):
        params = pickle.dumps(
            {
                "args": args,
                "kwargs": kwargs,
            }
        )
        response = self._session.post(self._call_url, data=params)
        if response.status_code == 402:
            raise NoSubscriptionException(
                "You don't have an active subscription. Please, check the website."
            )
        if response.status_code // 100 == 2:
            return pickle.loads(response.content)
        try:
            error = pickle.loads(response.content)
            raise RemoteException(error["error_type"], error["error"])
        except pickle.UnpicklingError:
            raise RemoteException("UnknownResponse", response.content)
