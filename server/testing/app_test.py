import pytest
from app import app, db, Plant

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_plant(client):
    with app.app_context():
        plant = Plant(name="Aloe Vera")
        db.session.add(plant)
        db.session.commit()
        plant_id = plant.id

    resp = client.get(f'/plants/{plant_id}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == "Aloe Vera"
    assert data['is_in_stock'] is True

def test_get_plants(client):
    with app.app_context():
        plant1 = Plant(name="Aloe Vera")
        plant2 = Plant(name="Fern")
        db.session.add(plant1)
        db.session.add(plant2)
        db.session.commit()

    resp = client.get('/plants')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2
    assert data[0]['name'] == "Aloe Vera"
    assert data[1]['name'] == "Fern"

def test_create_plant(client):
    resp = client.post('/plants', json={'name': 'Cactus', 'image': 'cactus.jpg', 'price': 10.0})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['name'] == 'Cactus'
    assert data['price'] == 10.0

def test_update_plant(client):
    with app.app_context():
        plant = Plant(name="Fern")
        db.session.add(plant)
        db.session.commit()
        plant_id = plant.id

    resp = client.patch(f'/plants/{plant_id}', json={'is_in_stock': False})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['is_in_stock'] is False

def test_delete_plant(client):
    with app.app_context():
        plant = Plant(name="Cactus")
        db.session.add(plant)
        db.session.commit()
        plant_id = plant.id

    resp = client.delete(f'/plants/{plant_id}')
    assert resp.status_code == 204

    # Verify it's deleted
    resp = client.get(f'/plants/{plant_id}')
    assert resp.status_code == 404
