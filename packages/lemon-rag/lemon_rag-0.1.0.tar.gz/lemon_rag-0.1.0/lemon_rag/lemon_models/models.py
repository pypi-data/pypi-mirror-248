from datetime import datetime
from typing import Union, TypeVar, Generic, Iterator, Optional, TypedDict
import peewee

CharField = Union[peewee.CharField, str]
DatetimeField = Union[peewee.DateTimeField, datetime]
TextField = Union[peewee.TextField, str]
IntegerField = Union[peewee.IntegerField, int]
BooleanField = Union[peewee.BooleanField, bool]
FloatField = Union[peewee.FloatField, float]
DoubleField = Union[peewee.DoubleField, float]
DateField = Union[peewee.DateField, str]
DateTimeField = Union[peewee.DateTimeField, str]
TimeField = Union[peewee.TimeField, str]
DecimalField = Union[peewee.DecimalField, float]
PrimaryKeyField = Union[peewee.PrimaryKeyField, int]

T = TypeVar('T')


class ModelSelect(peewee.ModelSelect, Generic[T]):
    def __iter__(self) -> Iterator[T]:
        pass

    def where(self, *expressions) -> 'ModelSelect[T]':
        pass

    def limit(self, value: Optional[int] = None) -> 'ModelSelect[T]':
        pass

    def offset(self, value: Optional[int] = None) -> 'ModelSelect[T]':
        pass


class BackrefAccessor(peewee.BackrefAccessor, Generic[T]):
    pass


class ModelUpdate(peewee.ModelUpdate, Generic[T]):
    def where(self, *expressions) -> 'ModelUpdate[T]':
        pass

    def execute(self, database=None) -> int:
        pass


class BaseModel(peewee.Model):
    id: PrimaryKeyField

class XFConfig(BaseModel):

    class __InnerFields(TypedDict):
        pass

    @classmethod
    def select(cls, *fields) -> ModelSelect['XFConfig']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['XFConfig']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'XFConfig':
        pass


class OPENAIConfig(BaseModel):
    api_key: CharField
    base_url: CharField

    class __InnerFields(TypedDict):
        api_key: str
        base_url: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['OPENAIConfig']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['OPENAIConfig']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'OPENAIConfig':
        pass


class VectorStoreConfig(BaseModel):
    uri: CharField
    token: CharField

    class __InnerFields(TypedDict):
        uri: str
        token: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['VectorStoreConfig']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['VectorStoreConfig']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'VectorStoreConfig':
        pass


class AuthUserTab(BaseModel):
    username: CharField
    password: CharField
    last_signin: DatetimeField
    nickname: CharField
    avatar: CharField
    user_quota: Union[BackrefAccessor['UserQuotaTab'], ModelSelect['UserQuotaTab']]
    file: Union[BackrefAccessor['FileUploadRecordTab'], ModelSelect['FileUploadRecordTab']]
    sessions: Union[BackrefAccessor['SessionTab'], ModelSelect['SessionTab']]
    back_sessions: Union[BackrefAccessor['SessionTab'], ModelSelect['SessionTab']]
    messages: Union[BackrefAccessor['MessageTab'], ModelSelect['MessageTab']]
    KnowledgeBaseTab: Union[BackrefAccessor['KnowledgeBaseTab'], ModelSelect['KnowledgeBaseTab']]

    class __InnerFields(TypedDict):
        username: str
        password: str
        last_signin: datetime
        nickname: str
        avatar: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['AuthUserTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['AuthUserTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'AuthUserTab':
        pass


class UserQuotaTab(BaseModel):
    request_per_min: IntegerField
    request_per_day: IntegerField
    request_per_month: IntegerField
    max_knowledge_files: IntegerField
    max_single_file_size: IntegerField
    max_total_knowledge_size: IntegerField
    auth_user: Union[peewee.ForeignKeyField, 'AuthUserTab']

    class __InnerFields(TypedDict):
        request_per_min: int
        request_per_day: int
        request_per_month: int
        max_knowledge_files: int
        max_single_file_size: int
        max_total_knowledge_size: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['UserQuotaTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['UserQuotaTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'UserQuotaTab':
        pass


class KnowledgeBaseFileTab(BaseModel):
    filename: CharField
    extension: CharField
    origin_filename: CharField
    file_size: IntegerField
    KnowledgeBaseTab: Union[peewee.ForeignKeyField, 'KnowledgeBaseTab']
    upload_records: Union[BackrefAccessor['FileUploadRecordTab'], ModelSelect['FileUploadRecordTab']]

    class __InnerFields(TypedDict):
        filename: str
        extension: str
        origin_filename: str
        file_size: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['KnowledgeBaseFileTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['KnowledgeBaseFileTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'KnowledgeBaseFileTab':
        pass


class FileUploadRecordTab(BaseModel):
    upload_time: DatetimeField
    file: Union[peewee.ForeignKeyField, 'KnowledgeBaseFileTab']
    uploader: Union[peewee.ForeignKeyField, 'AuthUserTab']

    class __InnerFields(TypedDict):
        upload_time: datetime

    @classmethod
    def select(cls, *fields) -> ModelSelect['FileUploadRecordTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['FileUploadRecordTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'FileUploadRecordTab':
        pass


class SessionTab(BaseModel):
    create_at: CharField
    topic: CharField
    last_msg_id: IntegerField
    last_msg_ts: IntegerField
    assistant_role: CharField
    title: CharField
    disabled_at: BooleanField
    user: Union[peewee.ForeignKeyField, 'AuthUserTab']
    friend: Union[peewee.ForeignKeyField, 'AuthUserTab']
    messages: Union[BackrefAccessor['MessageTab'], ModelSelect['MessageTab']]

    class __InnerFields(TypedDict):
        create_at: str
        topic: str
        last_msg_id: int
        last_msg_ts: int
        assistant_role: str
        title: str
        disabled_at: bool

    @classmethod
    def select(cls, *fields) -> ModelSelect['SessionTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['SessionTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'SessionTab':
        pass


class MessageTab(BaseModel):
    msg_id: IntegerField
    role: CharField
    is_system: CharField
    client_ts: IntegerField
    server_ts: IntegerField
    is_answer: BooleanField
    is_system: BooleanField
    support_retry: BooleanField
    support_rating: BooleanField
    content: CharField
    text: CharField
    context_text: CharField
    session: Union[peewee.ForeignKeyField, 'SessionTab']
    user: Union[peewee.ForeignKeyField, 'AuthUserTab']

    class __InnerFields(TypedDict):
        msg_id: int
        role: str
        is_system: str
        client_ts: int
        server_ts: int
        is_answer: bool
        is_system: bool
        support_retry: bool
        support_rating: bool
        content: str
        text: str
        context_text: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['MessageTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['MessageTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'MessageTab':
        pass


class KnowledgeBaseTab(BaseModel):
    AuthUserTab: Union[peewee.ForeignKeyField, 'AuthUserTab']
    KnowledgeBaseFileTab: Union[BackrefAccessor['KnowledgeBaseFileTab'], ModelSelect['KnowledgeBaseFileTab']]

    class __InnerFields(TypedDict):
        pass

    @classmethod
    def select(cls, *fields) -> ModelSelect['KnowledgeBaseTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['KnowledgeBaseTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'KnowledgeBaseTab':
        pass

