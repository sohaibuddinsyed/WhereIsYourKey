    # privateKey = rsa.PrivateKey.load_pkcs1(privateKeyPem)
    # message = json.dumps(body_json["data"]).encode()
    # hash = SHA256.new(message)
    # # signature = rsa.sign(message, privkey, 'SHA-1')

    # privateKey = RSA.import_key(privateKeyPem)
    # signer = PKCS115_SigScheme(privateKey)
    # signature = signer.sign(hash)
    # print("Signature:", binascii.hexlify(signature))
    
    # base64Text = base64.b64encode(bytes.fromhex(data)).decode()
    # text = rsa.decrypt(base64.b64decode(base64Text.encode()), publicKey)

    logger.info(body_json)

        # publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(publicKeyPem)

    publicKeyPem = (
        "-----BEGIN PUBLIC KEY-----\n"
        + "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALg0ZH7ghM5aHOydm1ev+tn42OZxZoFx\n"
        + "z/VJNC4Px7SBbFJEFc9ADn49dWWNJo0h4K6JsW1Em172qZ9KetLT/sMCAwEAAQ==\n"
        + "-----END PUBLIC KEY-----\n"
    )

    privateKeyPem = (
        "-----BEGIN PRIVATE KEY-----\n"
        + "MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAuDRkfuCEzloc7J2b\n"
        + "V6/62fjY5nFmgXHP9Uk0Lg/HtIFsUkQVz0AOfj11ZY0mjSHgromxbUSbXvapn0p6\n"
        + "0tP+wwIDAQABAkEAmOEi5wqALqMrjlXgL46mq3GU0u0bHiPPbMwsum3uWSgIuZ6J\n"
        + "pRS7yz92nsOIovNo1NcFQXrgFVF2QOl8Gq5uQQIhANwBldKMUp4DWksJffmZhy87\n"
        + "rrYXBAsRQEFw3+MYsIdVAiEA1ldZQ/W1q/iht2ohly07OdzixBkkNDRT0M6ENeLU\n"
        + "PbcCIHQhmhZT3+Bs4KKvVgIFGqjCFk0kBQxahNKGZIgZpkUpAiA2njOE+cu9crHi\n"
        + "xwygNUpuSDcQuUdcdikVgEp4YMCsqQIhALECDFqXtDp61ubDJp4lPGQvnR4nl0+6\n"
        + "uWpRS8960kGz\n"
        + "-----END PRIVATE KEY-----\n"
    )
