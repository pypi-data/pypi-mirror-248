from pont.protocols.ssl import generate_certificate


def test_generate_certificate():
    cert = generate_certificate(512)  # Small key size for faster tests

    assert b"-----BEGIN CERTIFICATE-----" in cert
    assert b"-----END CERTIFICATE-----" in cert
    assert b"-----BEGIN RSA PRIVATE KEY-----" in cert
    assert b"-----END RSA PRIVATE KEY-----" in cert
