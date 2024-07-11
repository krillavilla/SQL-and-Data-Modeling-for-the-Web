from app import app
from models import db, Venue, Artist, Show
from datetime import datetime

def insert_sample_data():
    with app.app_context():
        # Create sample venues
        venue1 = Venue(
            name="The Musical Hop",
            city="San Francisco",
            state="CA",
            address="1015 Folsom Street",
            phone="123-123-1234",
            image_link="https://via.placeholder.com/150",
            facebook_link="https://www.facebook.com",
            genres="Jazz,Reggae,Swing,Classical,Folk",
            website="https://www.themusicalhop.com",
            seeking_talent=True,
            seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us."
        )

        venue2 = Venue(
            name="The Dueling Pianos Bar",
            city="New York",
            state="NY",
            address="335 Delancey Street",
            phone="123-123-1234",
            image_link="https://via.placeholder.com/150",
            facebook_link="https://www.facebook.com",
            genres="Classical,R&B,Hip-Hop",
            website="https://www.duelingpianos.com",
            seeking_talent=False
        )

        # Create sample artists
        artist1 = Artist(
            name="Guns N Petals",
            city="San Francisco",
            state="CA",
            phone="326-123-5000",
            genres="Rock n Roll",
            image_link="https://via.placeholder.com/150",
            facebook_link="https://www.facebook.com/GunsNPetals",
            website="https://www.gunsnpetalsband.com",
            seeking_venue=True,
            seeking_description="Looking for shows to perform at in the San Francisco Bay Area!"
        )

        artist2 = Artist(
            name="Matt Quevedo",
            city="New York",
            state="NY",
            phone="300-400-5000",
            genres="Jazz",
            image_link="https://via.placeholder.com/150",
            facebook_link="https://www.facebook.com/MattQuevedo",
            website="https://www.mattquevedo.com",
            seeking_venue=False
        )

        # Create sample shows
        show1 = Show(
            artist_id=1,
            venue_id=1,
            start_time=datetime.strptime('2019-05-21T21:30:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        )

        show2 = Show(
            artist_id=2,
            venue_id=2,
            start_time=datetime.strptime('2019-06-15T23:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        )

        # Insert data into the database
        db.session.add(venue1)
        db.session.add(venue2)
        db.session.add(artist1)
        db.session.add(artist2)
        db.session.add(show1)
        db.session.add(show2)

        db.session.commit()

if __name__ == "__main__":
    insert_sample_data()
