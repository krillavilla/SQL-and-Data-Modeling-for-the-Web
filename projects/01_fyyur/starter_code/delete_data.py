from app import app
from models import db, Venue, Artist, Show


def delete_data():
    with app.app_context():
        # Delete all shows
        Show.query.delete()
        db.session.commit()

        # Delete all artists
        Artist.query.delete()
        db.session.commit()

        # Delete all venues
        Venue.query.delete()
        db.session.commit()


if __name__ == "__main__":
    delete_data()
    print("All data deleted successfully.")
