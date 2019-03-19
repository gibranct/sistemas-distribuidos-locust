from locust import HttpLocust, TaskSet


def login(l):
    response = l.client.post("/wp-json/jwt-auth/v1/token",
                             json={"username": "gibran@edu.unifor.br", "password": "123456"})
    print('Response: ', response)
    return response.json()["token"]


def logout(l):
    l.client.get("/wp-login.php?loggedout=true")


def save_image(l):
    image = open('2.jpg', 'rb')
    header = {
        "Authorization": "Bearer " + l.token,
        "Content-Disposition": "form-data; filename='filename.jpg'"
    }
    response = l.client.post('/wp-json/wp/v2/media/',
                             files={"file": image}, headers=header)
    return response.json()['id']


def create_post(l):
    header = {
        "Authorization": "Bearer " + l.token
    }
    file = open('text.rtf', 'r')
    content = " ".join(file.readlines())
    data = {
        "title": "Um titulo novo",
        "content": content,
        "featured_media": l.image_id,
        "status": "publish"
    }
    response = l.client.post("/wp-json/wp/v2/posts", data=data, headers=header)
    print(response.json())


class UserBehavior(TaskSet):

    def on_start(self):
        self.token = login(self)
        self.image_id = save_image(self)
        create_post(self)

    # def on_stop(self):
        # logout(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
