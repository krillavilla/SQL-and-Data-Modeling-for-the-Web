from models import db, Venue, Artist, Show
from flask import Flask


def check_data():
    venues = Venue.query.all()
    artists = Artist.query.all()
    shows = Show.query.all()

    print(f'Venues: {venues}')
    print(f'Artists: {artists}')
    print(f'Shows: {shows}')


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/fyyur'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        check_data()
