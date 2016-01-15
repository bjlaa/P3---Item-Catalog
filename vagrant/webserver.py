from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer 
import cgi

##Import CRUD Operations from Lesson 1 ##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

class webserverhandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>Hello!</body></html>"
				output += "<form method='POST' enctype='multipart/form-data' action='hello'> <h2>What would you like me to say?</h2><input name='message'type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>&#161Hola! <a href='/hello'>Back to hello</a></body></html>"
				output += "<form method='POST' enctype='multipart/form-data' action='hello'> <h2>What would you like me to say?</h2><input name='message'type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)

			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				print restaurants
				self.send_response(200)
				self.send_header('content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<body><html>"
				output += "<a href='/restaurants/new'>Make a New Restaurant Here</a><br />"
				for restaurant in restaurants:
					output += "</br>"
					output += restaurant.name
					output += "</br>"
					output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
					output += "</br>"
					output += "<a href='#'>Delete</a>"

				output += "</body></html>"
				self.wfile.write(output)

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<body><html>"
				output += "<h2>Add a new restaurant</h2>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<input name='newRestaurantName' type='text'/> <input type= 'submit' value='create'/>"
				output += "</body></html>"
				self.wfile.write(output)
				return
			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
				if myRestaurantQuery != []:
					self.send_response(200)
					self.send_header('content-type', 'text/html')
					self.end_headers()

					output = "<html><body>"
					output += "<h1>"
					output += myRestaurantQuery.name
					output += "</h1>"
					output += "<form method='POST' enctype='multipart/form-data' \
						action='/restaurant/%s/edit'>" % restaurantIDPath
					output += "<input name='newRestaurantName' type='text' placeholder='%s' />" % myRestaurantQuery.name
					output += "<input type='submit' value='Rename' />"
					output += "</form>"
					output += "</html></body"

					self.wfile.write(output)





		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('newRestaurantName')
				restaurantIDPath = self.path.split("/")[2]

				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery != []:
					myRestaurantQuery.name = messagecontent[0]
					session.add(myRestaurantQuery)
					session.commit()
					self.send_response(301)
					self.send_header('content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')

				# Create new Restaurant class
				newRestaurant = Restaurant( name = messagecontent[0])
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

				return

#			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
#			if ctype == 'multipart/form-data':
#				fields=cgi.parse_multipart(self.rfile, pdict)
#				messagecontent = fields.get('message')
#
#			output = ""
#			output += "<html><body>"
#			output += "<h2> Okay, how about this: </h2>"
#			output += "<h1> %s </h1>" % messagecontent[0]
#			output += "<form method='POST' enctype='multipart/form-data' action='hello'> <h2>What would you like me to say?</h2><input name='message'type='text' ><input type='submit' value='Submit'></form>"
#			output += "</body></html>"
#			self.wfile.write(output)

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverhandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()