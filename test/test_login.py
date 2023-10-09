def test_index(client):
    response = client.get("/login")
    assert b"<title>Halaman Login</title>" in response.data
