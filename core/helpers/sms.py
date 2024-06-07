from kavenegar import KavenegarAPI


def send_sms(template: str, recipient: str, token: dict):
    """Send an OTP (One-Time Password) SMS message using the Kavenegar service.

    Args:
        recipient (str): The recipient's phone number.
        otp_code (str): The OTP code to be sent.

    Returns:
        bool: True if the OTP message was successfully sent, False otherwise.
    """
    api = KavenegarAPI(
        apikey="3333684B417362704A574638466C744375346668715034302B496D7154344A305677425A505878324F6B6F3D"
    )

    params = {"receptor": recipient, "template": template, **token}
    try:
        api.verify_lookup(params)
    except Exception as e:
        raise Exception(f"Kavenegar: Error sending OTP message: {e}")

    return True
