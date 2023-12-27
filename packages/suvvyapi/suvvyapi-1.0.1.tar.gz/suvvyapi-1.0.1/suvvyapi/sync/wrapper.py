from typing import Literal

import deprecation
import httpx

from suvvyapi.exceptions.api import (
    HistoryNotFoundError,
    HistoryStoppedError,
    HistoryTooLongError,
    InternalAPIError,
    InvalidAPITokenError,
    MessageLimitExceededError,
    NegativeBalanceError,
    UnknownAPIError,
)
from suvvyapi.models.history import ChatHistory, Message
from suvvyapi.models.responses import Prediction


class SuvvyAPIWrapper:
    @deprecation.deprecated(
        deprecated_in="1.0.0",
        removed_in="2.0.0",
        details="Use the Suvvy() class instead",
    )
    def __init__(
        self,
        token: str,
        base_url: str = "https://api.suvvy.ai/",
        check_connection: bool = True,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
    ):
        self.token = token
        self.base_url = base_url.lstrip("/")
        self.placeholders = placeholders or {}
        self.custom_log_info = custom_log_info or {}

        if check_connection:
            self._make_request("GET", "/api/check")

    def _make_request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        path: str,
        body: dict | None = None,
    ) -> httpx.Response:
        headers = {"Authorization": f"bearer {self.token}"}
        with httpx.Client(headers=headers, base_url=self.base_url, timeout=300) as c:
            response = c.request(method=method, url=path, json=body)
            if response.status_code == 401:
                raise InvalidAPITokenError("API Token is invalid.")
            if response.status_code == 402:
                raise NegativeBalanceError.from_detail(response.json()["detail"])
            if response.status_code == 500:
                raise InternalAPIError(
                    "Internal API error occurred. Contact suvvy.ai support."
                )
            return response

    def get_history(self, unique_id: str) -> ChatHistory:
        response = self._make_request(
            method="GET", path=f"/api/v1/history?unique_id={unique_id}"
        )
        json = response.json()
        history = ChatHistory(**json)
        return history

    def reset_history(self, unique_id: str) -> None:
        self._make_request(method="PUT", path=f"/api/v1/history?unique_id={unique_id}")

    def add_message(
        self,
        message: Message | list[Message],
        unique_id: str,
        pass_ai_as_employee: bool = True,
    ) -> None:
        if not isinstance(message, list):
            message = [message]

        _ms = []
        for m in message:
            _ms.append(m.model_dump())

        message = _ms

        body = {"messages": message, "pass_ai_as_employee": pass_ai_as_employee}
        self._make_request(
            method="POST",
            path=f"/api/v1/history/message?unique_id={unique_id}",
            body=body,
        )

    def predict_from_history(
        self,
        unique_id: str,
        placeholders: dict | None = None,
        auto_insert_ai: bool = True,
        custom_log_info: dict | None = None,
        raise_if_dialog_stopped: bool = False,
    ) -> Prediction:
        placeholders = placeholders or {}
        custom_log_info = custom_log_info or {}

        custom_log_info = dict(**self.custom_log_info, **custom_log_info)
        placeholders = dict(**self.placeholders, **placeholders)

        body = {
            "placeholders": placeholders,
            "custom_log_info": custom_log_info,
            "auto_insert_ai": auto_insert_ai,
        }
        response = self._make_request(
            method="POST",
            path=f"/api/v1/history/predict?unique_id={unique_id}",
            body=body,
        )
        match response.status_code:
            case 202:
                if raise_if_dialog_stopped:
                    raise HistoryStoppedError("History is marked as stopped")
                else:
                    prediction = Prediction()
                    return prediction
            case 404:
                raise HistoryNotFoundError()
            case 413:
                json = response.json()
                detail = json["detail"]
                if detail.startswith("Maximum token limit"):
                    raise HistoryTooLongError("History is too long to process")
                else:
                    raise MessageLimitExceededError(
                        "Message limit for that instance is exceeded"
                    )
            case 200:
                pass
            case _:
                raise UnknownAPIError(
                    f"We don't know what happened. Status code is {response.status_code}"
                )

        json = response.json()
        prediction = Prediction(**json)
        return prediction

    def predict(
        self,
        message: Message | list[Message],
        unique_id: str,
        pass_ai_as_employee: bool = True,
        placeholders: dict | None = None,
        auto_insert_ai: bool = True,
        custom_log_info: dict | None = None,
        raise_if_dialog_stopped: bool = False,
    ) -> Prediction:
        placeholders = placeholders or {}
        custom_log_info = custom_log_info or {}

        if not isinstance(message, list):
            message = [message]

        _ms = []
        for m in message:
            _ms.append(m.model_dump())

        message = _ms

        custom_log_info = dict(**self.custom_log_info, **custom_log_info)
        placeholders = dict(**self.placeholders, **placeholders)

        body = {
            "messages": message,
            "pass_ai_as_employee": pass_ai_as_employee,
            "placeholders": placeholders,
            "custom_log_info": custom_log_info,
            "auto_insert_ai": auto_insert_ai,
        }

        response = self._make_request(
            method="POST",
            path=f"/api/v1/history/message/predict?unique_id={unique_id}",
            body=body,
        )
        match response.status_code:
            case 202:
                if raise_if_dialog_stopped:
                    raise HistoryStoppedError("History is marked as stopped")
                else:
                    prediction = Prediction()
                    return prediction
            case 404:
                raise HistoryNotFoundError()
            case 413:
                json = response.json()
                detail = json["detail"]
                if detail.startswith("Maximum token limit"):
                    raise HistoryTooLongError("History is too long to process")
                else:
                    raise MessageLimitExceededError(
                        "Message limit for that instance is exceeded"
                    )
            case 200:
                pass
            case _:
                raise UnknownAPIError(
                    f"We don't know what happened. Status code is {response.status_code}"
                )

        json = response.json()
        prediction = Prediction(**json)
        return prediction
