from datetime import datetime
from decimal import Decimal
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
DecimalField = Union[peewee.DecimalField, Decimal]
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
    last_signin: IntegerField
    nickname: CharField
    avatar: CharField
    create_time: IntegerField
    user_quota: Union[BackrefAccessor['UserQuotaTab'], ModelSelect['UserQuotaTab']]
    file: Union[BackrefAccessor['FileUploadRecordTab'], ModelSelect['FileUploadRecordTab']]
    sessions: Union[BackrefAccessor['SessionTab'], ModelSelect['SessionTab']]
    back_sessions: Union[BackrefAccessor['SessionTab'], ModelSelect['SessionTab']]
    messages: Union[BackrefAccessor['MessageTab'], ModelSelect['MessageTab']]
    KnowledgeBaseTab: Union[BackrefAccessor['KnowledgeBaseTab'], ModelSelect['KnowledgeBaseTab']]
    tokens: Union[BackrefAccessor['AppAuthTokenTab'], ModelSelect['AppAuthTokenTab']]

    class __InnerFields(TypedDict):
        username: str
        password: str
        last_signin: int
        nickname: str
        avatar: str
        create_time: int

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
    MessageSummarizationTab: Union[BackrefAccessor['MessageSummarizationTab'], ModelSelect['MessageSummarizationTab']]

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
    is_system_msg: BooleanField
    support_retry: BooleanField
    support_rating: BooleanField
    content: CharField
    text: CharField
    context_text: CharField
    session: Union[peewee.ForeignKeyField, 'SessionTab']
    user: Union[peewee.ForeignKeyField, 'AuthUserTab']
    MessageSummarizationTab: Union[peewee.ForeignKeyField, 'MessageSummarizationTab']

    class __InnerFields(TypedDict):
        msg_id: int
        role: str
        is_system: str
        client_ts: int
        server_ts: int
        is_answer: bool
        is_system_msg: bool
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


class DevModuleTab(BaseModel):
    name: CharField
    version: CharField
    registry: CharField

    class __InnerFields(TypedDict):
        name: str
        version: str
        registry: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['DevModuleTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['DevModuleTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'DevModuleTab':
        pass


class AppAuthTokenTab(BaseModel):
    create_at: IntegerField
    expire_at: IntegerField
    token: CharField
    comment: CharField
    user: Union[peewee.ForeignKeyField, 'AuthUserTab']

    class __InnerFields(TypedDict):
        create_at: int
        expire_at: int
        token: str
        comment: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['AppAuthTokenTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['AppAuthTokenTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'AppAuthTokenTab':
        pass


class MessageSummarizationTab(BaseModel):
    from_msg_id: IntegerField
    to_msg_id: IntegerField
    summarization: CharField
    msg_count: IntegerField
    SessionTab: Union[peewee.ForeignKeyField, 'SessionTab']
    MessageTab: Union[BackrefAccessor['MessageTab'], ModelSelect['MessageTab']]

    class __InnerFields(TypedDict):
        from_msg_id: int
        to_msg_id: int
        summarization: str
        msg_count: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['MessageSummarizationTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['MessageSummarizationTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'MessageSummarizationTab':
        pass


class TransactionTab(BaseModel):
    voucher_number: CharField
    type: CharField
    item: CharField
    description: CharField
    amount: DecimalField
    notes: CharField
    date: IntegerField
    Accounts: Union[peewee.ForeignKeyField, 'AccountTab']
    ProjectTab: Union[peewee.ForeignKeyField, 'ProjectTab']

    class __InnerFields(TypedDict):
        voucher_number: str
        type: str
        item: str
        description: str
        amount: Decimal
        notes: str
        date: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['TransactionTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['TransactionTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'TransactionTab':
        pass


class AccountTab(BaseModel):
    account_name: CharField
    account_balance: DecimalField
    create_date: IntegerField
    Transactions: Union[BackrefAccessor['TransactionTab'], ModelSelect['TransactionTab']]
    out_flow: Union[BackrefAccessor['InternalTransferTab'], ModelSelect['InternalTransferTab']]
    in_flow: Union[BackrefAccessor['InternalTransferTab'], ModelSelect['InternalTransferTab']]

    class __InnerFields(TypedDict):
        account_name: str
        account_balance: Decimal
        create_date: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['AccountTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['AccountTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'AccountTab':
        pass


class InternalTransferTab(BaseModel):
    amount: DecimalField
    description: CharField
    date: IntegerField
    AccountTab: Union[peewee.ForeignKeyField, 'AccountTab']
    AccountTab: Union[peewee.ForeignKeyField, 'AccountTab']

    class __InnerFields(TypedDict):
        amount: Decimal
        description: str
        date: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['InternalTransferTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['InternalTransferTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'InternalTransferTab':
        pass


class ReceivablePayableTab(BaseModel):
    description: CharField
    type: CharField
    handler: CharField
    product_name: CharField
    specification: CharField
    quantity: DecimalField
    unit_price: DecimalField
    nodes: CharField
    date: IntegerField
    ProjectTab: Union[peewee.ForeignKeyField, 'ProjectTab']

    class __InnerFields(TypedDict):
        description: str
        type: str
        handler: str
        product_name: str
        specification: str
        quantity: Decimal
        unit_price: Decimal
        nodes: str
        date: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['ReceivablePayableTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['ReceivablePayableTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'ReceivablePayableTab':
        pass


class RepaymentItemTab(BaseModel):
    repayment_name: CharField
    amount: DecimalField
    EmployeeLoans: Union[peewee.ForeignKeyField, 'EmployeeLoanTab']

    class __InnerFields(TypedDict):
        repayment_name: str
        amount: Decimal

    @classmethod
    def select(cls, *fields) -> ModelSelect['RepaymentItemTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['RepaymentItemTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'RepaymentItemTab':
        pass


class EmployeeLoanTab(BaseModel):
    description: CharField
    amount: DecimalField
    adjustment_amount: DecimalField
    date: IntegerField
    Employees: Union[peewee.ForeignKeyField, 'EmployeeTab']
    ExpenseItems: Union[BackrefAccessor['RepaymentItemTab'], ModelSelect['RepaymentItemTab']]

    class __InnerFields(TypedDict):
        description: str
        amount: Decimal
        adjustment_amount: Decimal
        date: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['EmployeeLoanTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['EmployeeLoanTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'EmployeeLoanTab':
        pass


class EmployeeTab(BaseModel):
    name: CharField
    age: IntegerField
    gender: CharField
    ProjectTab: Union[peewee.ForeignKeyField, 'ProjectTab']
    EmployeeLoans: Union[BackrefAccessor['EmployeeLoanTab'], ModelSelect['EmployeeLoanTab']]
    SalaryTab: Union[BackrefAccessor['SalaryTab'], ModelSelect['SalaryTab']]

    class __InnerFields(TypedDict):
        name: str
        age: int
        gender: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['EmployeeTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['EmployeeTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'EmployeeTab':
        pass


class SupplierTab(BaseModel):
    name: CharField
    contact_name: CharField
    contact_phone: CharField
    ProjectTab: Union[peewee.ForeignKeyField, 'ProjectTab']

    class __InnerFields(TypedDict):
        name: str
        contact_name: str
        contact_phone: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['SupplierTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['SupplierTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'SupplierTab':
        pass


class CustomerTab(BaseModel):
    name: CharField
    contact_name: CharField
    contact_phone: CharField
    ProjectTab: Union[peewee.ForeignKeyField, 'ProjectTab']

    class __InnerFields(TypedDict):
        name: str
        contact_name: str
        contact_phone: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['CustomerTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['CustomerTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'CustomerTab':
        pass


class ProjectTab(BaseModel):
    name: CharField
    start_date: IntegerField
    end_date: IntegerField
    EmployeeTab: Union[BackrefAccessor['EmployeeTab'], ModelSelect['EmployeeTab']]
    SupplierTab: Union[BackrefAccessor['SupplierTab'], ModelSelect['SupplierTab']]
    CustomerTab: Union[BackrefAccessor['CustomerTab'], ModelSelect['CustomerTab']]
    ContractTab: Union[BackrefAccessor['ContractTab'], ModelSelect['ContractTab']]
    TransactionTab: Union[BackrefAccessor['TransactionTab'], ModelSelect['TransactionTab']]
    ReceivablePayableTab: Union[BackrefAccessor['ReceivablePayableTab'], ModelSelect['ReceivablePayableTab']]

    class __InnerFields(TypedDict):
        name: str
        start_date: int
        end_date: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['ProjectTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['ProjectTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'ProjectTab':
        pass


class ContractTab(BaseModel):
    number: CharField
    name: CharField
    type: CharField
    amount: DecimalField
    adjustment_amount: DecimalField
    date: IntegerField
    start_date: IntegerField
    end_date: IntegerField
    ProjectTab: Union[peewee.ForeignKeyField, 'ProjectTab']
    InvoiceTab: Union[BackrefAccessor['InvoiceTab'], ModelSelect['InvoiceTab']]

    class __InnerFields(TypedDict):
        number: str
        name: str
        type: str
        amount: Decimal
        adjustment_amount: Decimal
        date: int
        start_date: int
        end_date: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['ContractTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['ContractTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'ContractTab':
        pass


class InvoiceTab(BaseModel):
    amount: DecimalField
    tax_rate: DecimalField
    type: CharField
    number: CharField
    code: CharField
    content: CharField
    date: IntegerField
    invoice_date: DatetimeField
    nodes: CharField
    ContractTab: Union[peewee.ForeignKeyField, 'ContractTab']

    class __InnerFields(TypedDict):
        amount: Decimal
        tax_rate: Decimal
        type: str
        number: str
        code: str
        content: str
        date: int
        invoice_date: datetime
        nodes: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['InvoiceTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['InvoiceTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'InvoiceTab':
        pass


class SalaryTab(BaseModel):
    year: IntegerField
    month: IntegerField
    attendance_days: IntegerField
    basic_salary: DecimalField
    overtime_pay: DecimalField
    attendance_bonus: DecimalField
    subsidy: DecimalField
    bonus: DecimalField
    leave_deduction: DecimalField
    other_deductions: DecimalField
    EmployeeTab: Union[peewee.ForeignKeyField, 'EmployeeTab']

    class __InnerFields(TypedDict):
        year: int
        month: int
        attendance_days: int
        basic_salary: Decimal
        overtime_pay: Decimal
        attendance_bonus: Decimal
        subsidy: Decimal
        bonus: Decimal
        leave_deduction: Decimal
        other_deductions: Decimal

    @classmethod
    def select(cls, *fields) -> ModelSelect['SalaryTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['SalaryTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'SalaryTab':
        pass

