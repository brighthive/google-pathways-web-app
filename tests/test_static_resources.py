def test_robots(client):
    resp = client.get("/robots.txt")

    assert resp.status_code == 200
    assert "Sitemap: http://0.0.0.0:8000/sitemap.xml" in str(resp.data)


def test_sitemap_with_two_programs(client, pathways_programs):
    resp = client.get("/sitemap.xml")

    assert resp.status_code == 200
    assert "<loc>http://0.0.0.0:8000/pathways?page=1</loc>" in str(resp.data)
    assert "<loc>http://0.0.0.0:8000/pathways?page=2</loc>" in str(resp.data)
