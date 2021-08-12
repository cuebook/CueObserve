import pytest
from django_celery_beat.models import CrontabSchedule
from django.urls import reverse
from conftest import populate_seed_data
from anomaly.models import CustomSchedule as Schedule
from users.models import CustomUser

@pytest.fixture()
def setup_user(db):
    """sets up a user to be used for login"""
    user = CustomUser.objects.create_superuser("admin@domain.com", "admin")
    user.status = "Active"
    user.is_active = True
    user.name = "Sachin"
    user.save()

@pytest.mark.django_db(transaction=True)
def test_schedules(setup_user, client, populate_seed_data, mocker):
    client.login(email="admin@domain.com", password="admin")
    # Create schedule test
    path = reverse('scheduleView')
    data = {'name': 'Schedule at 3 AM ',
             'crontab': '0 3 * * *',
             'timezone':'Asia/Kolkata' }
    response = client.post(path, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data['data']
    scheduleId = response.data["data"]
    crontabId = Schedule.objects.get(id= scheduleId).cronSchedule_id

    # Update schedule test
    path = reverse('scheduleView')
    data = {'id': scheduleId,
             'name': 'Schedule at 4 AM ',
             'crontab': '0 4 * * *',
             'timezone': 'Asia/Kolkata'}
    response = client.put(path, data=data, content_type="application/json")
    assert response.status_code == 200
    assert Schedule.objects.get(id=scheduleId).name == "Schedule at 4 AM "

    # Get schedule test
    path = reverse('scheduleView')
    response = client.get(path)
    assert response.status_code == 200
    assert response.data["data"]

    # Get single schedule test
    path = reverse("getSingleSchedule", kwargs={"scheduleId": scheduleId})
    response = client.get(path)
    assert response.status_code == 200
    assert response.data["data"]
    assert response.data["data"][0]["name"] == "Schedule at 4 AM "

    # Delete schedule test
    path = reverse("getSingleSchedule", kwargs={"scheduleId": scheduleId})
    response = client.delete(path)
    assert response.status_code == 200
    assert Schedule.objects.filter(id=scheduleId).count() == 0
    assert CrontabSchedule.objects.filter(id=crontabId).count() == 0