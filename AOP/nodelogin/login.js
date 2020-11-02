var mysql = require('mysql');
var express = require('express');
var session = require('express-session');
var bodyParser = require('body-parser');
var path = require('path');

// required for requests
var app = express();
app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Import jsface - required for OOP and AOP
var jsface = require("jsface"),
	Class = jsface.Class;
var pointcut = require("../node_modules/jsface/jsface.pointcut");
const { Console } = require('console');

// Make connection with the mySQL database
var connection = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: 'root',
	database: 'nodelogin'
});

// Create an User object 
var User = Class({
	constructor: function (username, password) {
		console.log("\n\n>>>>>>>>>>>>>>>>>> In constructor <<<<<<<<<<<<<<<<<<<<<<");
		console.log("Values username " + username + " and password " + password + " are set using constructor.")
		this.username = username;
		this.password = password;
	},

	// Getter/Setter username
	username: {
		get: function () {
			return this._username;
		},
		set: function (value) {
			this._username = value;
		}
	},

	// Getter/Setter password
	password: {
		get: function () {
			return this._password;
		},
		set: function (value) {
			this._password = value;
		}
	},

	// String method
	toString: function () {
		return this.username + "/" + this.password;
	}
});

// Executing AOP code - before and after
var advisor = {
	constructor: {
		before: function () {
			console.log("\n\n>>>>>>>>>>>>>>>>>>>>>> before <<<<<<<<<<<<<<<<<<<<<<<<<<");
			logger()
		},
		after: function () {
			console.log("\n\n>>>>>>>>>>>>>>>>>>>>>> after <<<<<<<<<<<<<<<<<<<<<<<<<<<");
			if (stopper_SQLi(this.username)) {
				console.log("User " + this.username + " tried a SQL Injection");
				this._username = null;
			}
		}
	},
};

// Pointcut - Here Our Code is merged with AOP
User = pointcut(User, advisor);


// :after function 
function stopper_SQLi(x) {
	var format = /[-'"$!%*#?&]/g;
	if (format.test(x)) {
		return true;
	} else {
		return false;
	}
}

// :before function
function logger() {
	console.log("New login attempt at " + new Date().toDateString() + ".")
	console.log("IP used for request: " + require("ip").address());
}


app.get('/', function (request, response) {
	response.sendFile(path.join(__dirname + '/login.html'));
});

app.post('/auth', function (request, response) {
	var newUser = new User(request.body.username, request.body.password);

	if (newUser.password && newUser.password) {
		connection.connect(function (err) {
			if (err) throw err;
			connection.query("SELECT * FROM accounts WHERE username = '" + newUser.username + "' AND password ='" + newUser.password + "'", function (err, result, fields) {
				if (err) throw err;

				if (Object.keys(result).length === 0) {
					response.send('\nLog in failed');
					console.log(result);
				}
				else {
					response.send('\nLog in successfully');
					console.log(result);
				}
				response.end();
			});
		});
	} else {
		response.send('Please enter username and Password!');
		response.end();
	}
});

app.listen(3000);
