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
