from typing import List, Literal, Optional

from paddle_billing_client.models import LazyBaseModel as BaseModel
from paddle_billing_client.models import PaddleResponse


class SubscribedEvent(BaseModel):
    name: str
    description: str
    group: str
    available_versions: List[int]


class NotificationSettingBase(BaseModel):
    description: str
    destination: str
    subscribed_events: List[SubscribedEvent]
    type: Optional[Literal["email", "url"]]
    active: bool
    api_version: int
    include_sensitive_fields: bool


class NotificationSetting(NotificationSettingBase):
    id: str
    endpoint_secret_key: str


class NotificationSettingResponse(PaddleResponse):
    data: NotificationSetting


class NotificationSettingsResponse(PaddleResponse):
    data: List[NotificationSetting]


class NotificationSettingRequest(NotificationSettingBase):
    subscribed_events: List[str]
