import asyncio

from nanosip import Options, SIPAuthCreds, TransactionProcessor

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    # auth_creds = SIPAuthCreds(
    #     username="doorbell",
    #     password="p5g9BaCrJM"
    # )

    # inv = Invite(
    #     uri_from="sip:doorbell@192.168.178.1",
    #     uri_to="sip:+491726335344@192.168.178.1",
    #     uri_via="192.168.178.1",
    #     auth_creds=auth_creds,
    # )

    auth_creds = SIPAuthCreds(username="2983576e0", password="_i2STGhVG6VFW")

    inv = Options(
        uri_from="sip:2983576e0@sipgate.de",
        # uri_to="sip:+491726335344@sipgate.de",
        uri_to="sip:notexists@sipgate.de",
        uri_via="sipgate.de",
        auth_creds=auth_creds,
    )

    try:
        tp = TransactionProcessor(inv)
        result = asyncio.run(tp.run())
    except OSError as e:
        print("We got: " + str(e))

    print("Result: ")
    print(result)
    print("END")
