from app import app
from app.extensions import login_manager
from app.models.user_model import UserModel

# import ngrok, logging

# logging.basicConfig(level=logging.INFO)
# tunnel = ngrok.werkzeug_develop()


@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


# with app.test_request_context():
#     print(url_for("login.masuk"))


if __name__ == "__main__":
    app.run()
