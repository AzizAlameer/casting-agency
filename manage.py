from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db, Actor, Movie

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    Movie(title='Gladiator', release_date='2000-05-06').insert()
    Movie(title='The Warriors',
          release_date='1979-02-09').insert()

    Actor(name='Vin Diesel', age=54, gender='male').insert()
    Actor(name='Brad Pitt', age=57, gender='male').insert()


if __name__ == '__main__':
    manager.run()
