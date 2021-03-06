
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
@app.route('/restaurants/')
def showRestaurant():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', 
		restaurants=restaurants)

# Make a new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == "POST":
		newRestaurant = Restaurant(name = request.form["name"])
		session.add(newRestaurant)
		session.commit()
		flash("New Restaurant Created")
		return redirect(url_for('showRestaurant'))
	else:
		return render_template('newRestaurant.html')

# Edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == "POST":
		if request.form["name"]:
			editedRestaurant.name = request.form["name"]
		session.add(editedRestaurant)
		session.commit()    
		flash("Restaurant Successfully Edited")
		return redirect(url_for('showRestaurant'))
	return render_template('editRestaurant.html', restaurant_id=restaurant_id, editedRestaurant= editedRestaurant)

# Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurantDeleted = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == "POST":
		session.delete(restaurantDeleted)
		session.commit()
		flash("Restaurant Successfully Deleted")
		return redirect(url_for('showRestaurant'))
	else:
		return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurantDeleted=restaurantDeleted)


# Restaurant own page
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return render_template('menu.html', restaurant = restaurant, items=items)

# Make a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == "POST":
		newMenuItem = MenuItem(name = request.form["name"], 
			description = request.form["description"], 
			price= request.form["price"],
			restaurant_id=restaurant_id)
		session.add(newMenuItem)
		session.commit()
		flash("New Menu Item Created")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id=restaurant_id)

# Edit menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['description']:
			editedItem.description = request.form['description']
		session.add(editedItem)
		session.commit()
		flash("Menu Item Successfully Edited")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, editedItem=editedItem)


#Delete menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemDeleted = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(itemDeleted)
		session.commit()
		flash("Menu Item Successfully Deleted")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id, itemDeleted=itemDeleted))
	else:
		return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, itemDeleted=itemDeleted)

#API Endpoints

@app.route('/restaurants/JSON/')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(restaurants= [i.serialize for i in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantMenusJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def MenuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
	return jsonify(MenuItems = item.serialize)

if __name__ == '__main__':
	app.secret_key = 'secret'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
