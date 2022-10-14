import json
import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    def __init__(self, parent):
        super(QuickstartUser, self).__init__(parent)
        self.token = "Token 990251c217da75dce50dc72faae9afa638a3dc08"

    wait_time = between(1, 2)


    @task
    def get_user_subs(self):
        self.client.get(url="/profiles/get_user_subscribers/1/", headers={"authorization": self.token})
    @task
    def get_user_subscriptions(self):
        self.client.get(url="/profiles/get_user_subscriptions/1/", headers={"authorization": self.token})
    @task
    def get_user_subscriptions(self):
        self.client.get(url="/profiles/get_user_subscriptions/1/", headers={"authorization": self.token})
    @task
    def get_all_posts(self):
        self.client.get(url="/posts/get_my_posts/", headers={"authorization": self.token})
    @task
    def get_all_posts_filtered(self):
        self.client.get(url="/posts/get_my_posts/?title=demo", headers={"authorization": self.token})
        
    