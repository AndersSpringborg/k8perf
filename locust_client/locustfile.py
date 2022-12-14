from locust import HttpUser, task, between

class LocustUser(HttpUser):
    wait_time = between(0.1, 0.2)

    @task
    def test(self):
        self.client.get("/")