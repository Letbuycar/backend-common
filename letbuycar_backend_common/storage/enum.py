from enum import Enum

class DOCS_TYPE(str, Enum):
    INVOICE = 'invoice'
    DUTY_RECEIPT = 'duty_receipt'
    CARGO_DOCS = 'cargo_docs'
    USER_DOCS = 'user_docs'
    PAYMENT = 'payment'
    CONTAINER = 'container'