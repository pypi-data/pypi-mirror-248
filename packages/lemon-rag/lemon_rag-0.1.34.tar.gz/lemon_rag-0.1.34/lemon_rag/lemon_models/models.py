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
    account_to: Union[BackrefAccessor['InternalTransferTab'], ModelSelect['InternalTransferTab']]
    account_from: Union[BackrefAccessor['InternalTransferTab'], ModelSelect['InternalTransferTab']]

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

