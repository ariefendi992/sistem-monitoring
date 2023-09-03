from app import app

# from app.extensions import login_manager
# from app.models.user_model import UserModel

# @login_manager.user_loader
# def load_user(id):
#     return UserModel.query.get(int(id))


if __name__ == "__main__":
    app.run()
