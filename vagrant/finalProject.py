from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# App's main page
@app.route('/')
@app.route('/restaurants')
def showRestaurant():
	return render_template('restaurants.html')

# Make a new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	return render_template('newRestaurant.html')

# Edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	return render_template('editRestaurant.html')

# Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	return render_template('deleteRestaurant.html')


# Restaurant own page
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	return render_template('menu.html')

# Make a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	return render_template('newMenuItem.html')

# Edit menu item
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	return render_template('editMenuItem.html')


#Delete menu item
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	return render_template('deleteMenuItem.html')


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
