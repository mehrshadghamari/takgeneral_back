import json
import typing

from suds.client import Client



class ZarinPal:

    ZARRINPAL_STATUS_CODE = {
        -1: {
            "FA": "اطلاعات ارسال شده ناقص است",
            "EN": "Information submitted is incomplete",
        },
        -2: {
            "FA": "آی پی و يا مرچنت كد پذيرنده صحيح نيست",
            "EN": "Merchant ID or Acceptor IP is not correct",
        },
        -3: {
            "FA": "بر اساس محدودیت های شاپرک حداقل میزان پرداخت باید بالای ۱۰۰ تومان باشد",
            "EN": "Amount should be above 100 Toman",
        },
        -4: {
            "FA": "سطح تاييد پذيرنده پايين تر از سطح نقره اي است",
            "EN": "Approved level of Acceptor is Lower than the silver",
        },
        -9: {
            "FA": "خطای اعتبار سنجی",
            "EN": "Validation error",
        },
        -10: {
            "FA": "ای پی و يا مرچنت كد پذيرنده صحيح نيست",
            "EN": "Terminal is not valid, please check merchant_id or ip address",
        },
        -11: {
            "FA": "مرچنت کد فعال نیست لطفا با تیم پشتیبانی ما تماس بگیرید",
            "EN": "Terminal is not active, please contact our support team",
        },
        -12: {
            "FA": "تلاش بیش از حد در یک بازه زمانی کوتاه",
            "EN": "To many attempts, please try again later",
        },
        -15: {
            "FA": "ترمینال شما به حالت تعلیق در آمده با تیم پشتیبانی تماس بگیرید",
            "EN": "Terminal user is suspend : (please contact our support team)",
        },
        -16: {
            "FA": "سطح تاييد پذيرنده پايين تر از سطح نقره اي است",
            "EN": "Terminal user level is not valid : ( please contact our support team)",
        },
        -17: {
            "FA": "محدودیت پذیرنده در سطح آبی",
            "EN": "Terminal user level is not valid : ( please contact our support team)",
        },
        -21: {
            "FA": "هيچ نوع عمليات مالي براي اين تراكنش يافت نشد",
            "EN": "Financial operations for this transaction was not found",
        },
        -22: {
            "FA": "تراكنش نا موفق مي باشد",
            "EN": "Transaction is unsuccessful",
        },
        -33: {
            "FA": "درصد های وارد شده درست نیست",
            "EN": "Wages floating is not valid",
        },
        -34: {
            "FA": "مبلغ از کل تراکنش بیشتر است",
            "EN": "Wages is not valid, Total wages(fixed) has been overload max amount",
        },
        -35: {
            "FA": "تعداد افراد دریافت کننده تسهیم بیش از حد مجاز است",
            "EN": "Wages is not valid, Total wages(floating) has been reached the limit in max parts",
        },
        -40: {
            "FA": "اجازه دسترسي به متد مربوطه وجود ندارد",
            "EN": "There is no access to the method",
        },
        -50: {
            "FA": "مبلغ پرداخت شده با مقدار مبلغ در وریفای متفاوت است",
            "EN": "Session is not valid, amounts values is not the same",
        },
        -51: {
            "FA": "پرداخت ناموفق",
            "EN": "Session is not valid, session is not active paid try",
        },
        -52: {
            "FA": "خطای غیر منتظره با پشتیبانی تماس بگیرید",
            "EN": "Oops!!, please contact our support team",
        },
        -53: {
            "FA": "اتوریتی برای این مرچنت کد نیست",
            "EN": "Session is not this merchant_id session",
        },
        -54: {
            "FA": "اتوریتی نامعتبر است",
            "EN": "Invalid authority",
        },
        100: {
            "FA": "عملیات با موفقیت انجام شد",
            "EN": "Transaction success",
        },
        101: {
            "FA": "این عملیات قبلا انجام شده است",
            "EN": "Transaction submitted",
        },
    }

    SANDBOX = settings.DEBUG
    WSDL = settings.ZARINPAL["SANDBOX_WSDL"] if SANDBOX else settings.ZARINPAL["WSDL"]
    WEB_GATEWAY = settings.ZARINPAL["SANDBOX_WEB_GATEWAY"] if SANDBOX else settings.ZARINPAL["WEB_GATEWAY"]

    def __init__(self, amount, detail, email, phone_number, callback):

        self.amount = amount
        self.detail = detail
        self.email = email
        self.phone_number = phone_number
        self.callback = callback
        self.authority = None
        self.is_paid = None

        self.payment_request_status = None
        self.payment_validation_status = None

    def pay(self):
        zarin_client = Client(self.WSDL)
        result = zarin_client.service.PaymentRequest(settings.ZARINPAL["MERCHANT_ID"], self.amount, self.detail, self.email, self.phone_number, self.callback)

        self.authority = result.Authority
        self.__status_handler(result.Status)

        return self.WEB_GATEWAY + result.Authority, result.Authority

    @classmethod
    def payment_validation(cls, authority: str, amount, exception=False):
        zarin_client = Client(cls.WSDL)
        result = zarin_client.service.PaymentVerificationWithExtra(settings.ZARINPAL["MERCHANT_ID"], authority, amount)

        status_msg = cls.__status_handler(result.Status, exception)

        is_paid = "OK" if result.Status in [100, 101] else "NOK"
        if result.ExtraDetail:
            extra_detail = json.loads(result.ExtraDetail)
            card_pan_mask = extra_detail["Transaction"]["CardPanMask"]
        else:
            card_pan_mask = None

        return is_paid, result.RefID, status_msg, card_pan_mask

    @classmethod
    def __status_handler(cls, status_code: int, exception=True):
        msg = cls.ZARRINPAL_STATUS_CODE.get(status_code, "zarinpal status code not found")
        if status_code < 0 and exception:
            raise Exception(msg)
        else:
            return msg





# first api :

# zp = ZarinPal(
#     amount=payment.amount,
#     detail=purchase.description,
#     email=settings.ZARINPAL["EMAIL"],
#     phone_number=purchase.user,
#     callback=settings.CALLBACK_URL,
# )

# url, authority = zp.pay()



# second api (call back) :

# payment_status = request.args["Status"]
# payment_authority = request.args["Authority"]

# payment = Payment.get_or_none(Payment.authority == payment_authority)
# purchase = payment.purchase

# if payment:
#     payment_status, ref_id, msg, card_pan_mask = ZarinPal.payment_validation(amount=payment.amount, authority=payment_authority)
# else:
#     payment_status = "NOK"