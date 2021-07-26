class CheckoutPaymentStatusConstants:
    PROCESSING = "Processing"
    PAID = "Paid"
    FAILED = "Failed"

    LIST = (
        (PROCESSING, PROCESSING),
        (PAID, PAID),
        (FAILED, FAILED),
    )


class CheckoutStatusConstants:
    OPEN = "Open"
    CLOSED = "Closed"

    LIST = (
        (OPEN, OPEN),
        (CLOSED, CLOSED)
    )