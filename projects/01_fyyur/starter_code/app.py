# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from datetime import datetime
from logging import Formatter, FileHandler

import babel
import dateutil.parser
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment

from forms import *
from models import db, Venue, Artist, Show

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/fyyur'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    venue_data = db.session.query(Venue.city, Venue.state).distinct().all()
    data = []
    for venue in venue_data:
        venues = db.session.query(Venue).filter(Venue.city == venue.city, Venue.state == venue.state).all()
        venue_data = []
        for venue in venues:
            venue_data.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": db.session.query(Show).filter(Show.venue_id == Venue.id,
                                                                    Show.start_time > datetime.now()).count()
            })
        data.append({
            "city": venue.city,
            "state": venue.state,
            "venues": venue_data
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    search = f"%{search_term}%"
    venues = Venue.query.filter(Venue.name.ilike(search)).all()
    data = []
    for venue in venues:
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": 0
        })
    response = {
        "count": len(venues),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue_data = db.session.query(Venue).filter(Venue.id == venue_id).all()
    data = []
    for venue in venue_data:
        data = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": [],
            "upcoming_shows": [],
            "past_shows_count": 0,
            "upcoming_shows_count": 0,
        }
        shows = db.session.query(Show).filter(Show.venue_id == venue_id).all()
        for show in shows:
            artist = db.session.query(Artist).filter(Artist.id == show.artist_id).first()
            show_data = {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": str(show.start_time)
            }
            if show.start_time < datetime.now():
                data['past_shows'].append(show_data)
                data['past_shows_count'] += 1
            else:
                data['upcoming_shows'].append(show_data)
                data['upcoming_shows_count'] += 1

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        # Capture form data
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        genres = request.form.get('genres')
        website = request.form.get('website')
        facebook_link = request.form.get('facebook_link')
        image_link = request.form.get('image_link')
        seeking_talent = True if 'seeking_talent' in request.form else False
        seeking_description = request.form.get('seeking_description')

        # Create new venue object
        new_venue = Venue(name=name, city=city, state=state, address=address,
                          phone=phone, genres=genres, website=website, facebook_link=facebook_link,
                          image_link=image_link, seeking_talent=seeking_talent,
                          seeking_description=seeking_description)

        # Add new venue to the database
        db.session.add(new_venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash(f"Error Occurred: {e}")
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash(f'An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venue = Venue.query.get(venue_id)
        if venue:
            db.session.delete(venue)
            db.session.commit()
            flash('Venue was successfully deleted!')
        else:
            flash('Venue not found!')
    except Exception as e:
        db.session.rollback()
        flash(f"Error Occurred: {e}")
        flash(f"An error occurred. Venue could not be deleted.")
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    artists = Artist.query.all()
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    search = f"%{search_term}%"
    artist_results = Artist.query.filter(Artist.name.ilike(search)).all()

    data = []
    for artist in artist_results:
        data.append({
            "id": artist.id,
            "name": artist.name,
        })

    response = {
        "count": len(artist_results),
        "data": data
    }

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()

    # Prepare artist data if the artist exists
    if artist:
        data = {
            "id": artist.id,
            "name": artist.name,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "genres": artist.genres,
            "image_link": artist.image_link,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description
        }
    else:
        # Return None if the artist does not exist
        flash('Artist not found!')
        return redirect(url_for('index'))

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)

    # Check if the artist exists
    if not artist:
        flash('Artist not found!')
        return redirect(url_for('index'))

    # Populate the form with the artist data
    form = ArtistForm(obj=artist)

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    if artist:
        try:
            artist.name = request.form.get('name')
            artist.city = request.form.get('city')
            artist.state = request.form.get('state')
            artist.phone = request.form.get('phone')
            artist.genres = request.form.get('genres')
            artist.image_link = request.form.get('image_link')
            artist.facebook_link = request.form.get('facebook_link')
            artist.seeking_venue = True if 'seeking_venue' in request.form else False
            artist.seeking_description = request.form.get('seeking_description')

            db.session.commit()
            flash('Artist ' + request.form['name'] + ' was successfully updated!')
        except Exception as e:
            db.session.rollback()
            flash(f"Error Occurred: {e}")
            flash(f'An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
        finally:
            db.session.close()
    else:
        flash('Artist not found!')

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    # Query the database for the venue with the given ID
    venue = Venue.query.get(venue_id)

    # Check if the venue exists
    if not venue:
        flash('Venue not found!')
        return redirect(url_for('index'))

    # Create an instance of the VenueForm and populate it with the venue data
    form = VenueForm(obj=venue)

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    if venue:
        try:
            venue.name = request.form.get('name')
            venue.city = request.form.get('city')
            venue.state = request.form.get('state')
            venue.address = request.form.get('address')
            venue.phone = request.form.get('phone')
            venue.genres = request.form.get('genres')
            venue.website = request.form.get('website')
            venue.facebook_link = request.form.get('facebook_link')
            venue.image_link = request.form.get('image_link')
            venue.seeking_talent = True if 'seeking_talent' in request.form else False
            venue.seeking_description = request.form.get('seeking_description')

            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully updated!')
        except Exception as e:
            db.session.commit()
            flash(f"Error Occurred: {e}")
            flash(f'An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
        finally:
            db.session.close()
    else:
        flash('Venue not found!')

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        genres = request.form.get('genres')
        facebook_link = request.form.get('facebook_link')
        image_link = request.form.get('image_link')
        website = request.form.get('website')
        seeking_venue = True if 'seeking_venue' in request.form else False
        seeking_description = request.form.get('seeking_description')

        # Create an Artist record
        new_artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres,
                            facebook_link=facebook_link, image_link=image_link, website=website,
                            seeking_venue=seeking_venue, seeking_description=seeking_description)

        # Insert the new artist record into the database
        db.session.add(new_artist)
        db.session.commit()

        # Flash a success message
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash(f"Error Occurred: {e}")
        # Flash an error message
        flash(f"An error occurred. Artist {request.form['name']} could not be listed.")
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = []
    for show in shows:
        data.append({
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    try:
        artist_id = request.form.get('artist_id')
        venue_id = request.form.get('venue_id')
        start_time = request.form.get('start_time')

        # Validate artist_id and venue_id to ensure they are integers
        try:
            artist_id = int(artist_id)
            venue_id = int(venue_id)
        except ValueError:
            flash("Artist ID and Venue ID must be valid integers.")
            return redirect(url_for('index'))

        # Create a new show record
        new_show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)

        # Insert the new show record into the database
        db.session.add(new_show)
        db.session.commit()

        # Flash a success message
        flash('Show was successfully listed!')
    except Exception as e:
        # Rollback the session if an error occurs
        db.session.rollback()
        # Flash an error message
        flash(f"Error Occurred: {e}")
        flash("An error occurred. Show could not be listed.")
    finally:
        # Close the session
        db.session.close()

    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
