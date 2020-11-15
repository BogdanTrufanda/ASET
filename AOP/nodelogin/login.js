var mysql = require('mysql');
var express = require('express');
var session = require('express-session');
var bodyParser = require('body-parser');
var path = require('path');

//logger
const winston = require('winston');
const levels = {
	error: 0,
	warn: 1,
	info: 2,
	http: 3,
	verbose: 4,
	debug: 5,
	silly: 6
};



const customlogger = winston.createLogger({
	transports: [
		new winston.transports.Console(),
		new winston.transports.File({ filename: 'JuiceShop.log' })
	]
});

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
const { Console, timeStamp } = require('console');

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
		customlogger.log({
			level: 'info',
			timeStamp: new Date().toDateString(),
			ip: require("ip").address(),
			message: 'Using USER constructor'
		});
		customlogger.log({
			level: 'warn',
			timeStamp: new Date().toDateString(),
			ip: require("ip").address(),
			message: "Values username << " + username + " >> and password << " + password + " >> are set using constructor."
		});

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
			customlogger.log({
				level: 'info',
				timeStamp: new Date().toDateString(),
				ip: require("ip").address(),
				message: 'Before executing User constructor'
			});
			customlogger.log({
				level: 'warn',
				timeStamp: new Date().toDateString(),
				ip: require("ip").address(),
				message: "New login attempt at " + new Date().toDateString() + ". IP used for request: " + require("ip").address()
			});


		},
		after: function () {
			if (stopper_SQLi(this.username)) {
				let str = this.username;
				let result = str.match(/[a-zA-Z]{3,}/g);
				let result2 = str.match(/[^a-zA-Z]+/g);

				customlogger.log({
					level: 'info',
					timeStamp: new Date().toDateString(),
					ip: require("ip").address(),
					message: 'After executing User constructor'
				});

				customlogger.log({
					level: 'warn',
					timeStamp: new Date().toDateString(),
					ip: require("ip").address(),
					message: "User << " + result + " >> tried a SQL Injection with << " + result2 + " >> "
				});
				this._username = null;
			}
			else {
				customlogger.log({
					level: 'info',
					timeStamp: new Date().toDateString(),
					ip: require("ip").address(),
					message: "User << " + this.username + " >> tried a clear authentication"
				});
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

app.get('/', function (request, response) {
	response.sendFile(path.join(__dirname + '/login.html'));
});

app.post('/auth', function (request, response) {
	var newUser = new User(request.body.username, request.body.password);

	if (newUser.password && newUser.password) {
		connection.connect(function (err) {
			if (err) throw err;
			connection.query("SELECT * FROM accounts WHERE username = '" + newUser.username + " ' AND password ='" + newUser.password + "'", function (err, result, fields) {
				if (err) throw err;

				if (Object.keys(result).length === 0) {
					response.send('\nLog in failed');
					customlogger.log({
						level: 'warn',
						timeStamp: new Date().toDateString(),
						ip: require("ip").address(),
						message: "There was no Database leakage"
					});
				}
				else {
					response.send('\nLog in successfully');
					customlogger.log({
						level: 'warn',
						timeStamp: new Date().toDateString(),
						ip: require("ip").address(),
						message: result
					});
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
