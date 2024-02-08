from flask import Flask
from models import db, Clients
from flask_login import LoginManager
from main import main as main_blueprint
from admin import admin as admin_blueprint
from client import client as client_blueprint


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    app.config['UPLOAD_FOLDER'] = 'static/prizes'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Clients.query.get(int(user_id))

    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(client_blueprint)
    return app


aaa = create_app()
with aaa.app_context():
    db.create_all()

aaa.run(debug=True)




'''
<label>Введите название приза:</label>
    <input class="form-control" type="text" name="name_prize" placeholder="{{prize[1]}}">


    <div class="form-group">
      <label for="exampleFormControlFile1">Загрузите изображение приза</label>
      <input type="file" class="form-control-file" name="file" id="exampleFormControlFile1">
    </div>


    <div class="form-group">
      <label for="exampleFormControlTextarea1">Введите описание приза:</label>
      <textarea class="form-control" name="desc_prize" id="exampleFormControlTextarea1" rows="4" placeholder="{{prize[2]}}"></textarea>
    </div>
    <button type="submit" name="save_new_prize" value="{{idd}}">Сохранить</button>
    
    
                        <button class="image-button knopka_with_price" type="submit"><img class="image"
                            src="static/images/Untitled Project (6).jpg"> </button>
'''