var mysql = require('mysql');
var express = require('express');
var session = require('express-session');
var bodyParser = require('body-parser');
var path = require('path');
const winston = require('winston');

// Import jsface - required for OOP and AOP
var jsface = require("jsface"),
	Class = jsface.Class;
var pointcut = require("../node_modules/jsface/jsface.pointcut");

//Custom logger
const customlogger = winston.createLogger({
	transports: [
		new winston.transports.Console(),
		new winston.transports.File({ filename: 'JuiceShop.log' })
	]
});

// Make connection with the mySQL database and create a pool for DB requests
let sqlCon = mysql.createPool({
	connectionLimit: 100,
	host: 'localhost',
	user: 'root',
	password: 'root',
	database: 'nodelogin'
});

// Required for requests
var app = express();
app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Create an User object 
var User = Class({
	constructor: function (username, password) {
		customlogger.log({
			level: 'info',
			timeStamp: new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
			ip: require("ip").address(),
			message: 'Using USER constructor'
		});
		customlogger.log({
			level: 'warn',
			timeStamp:  new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
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
				timeStamp: new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
				ip: require("ip").address(),
				message: "Before executing User constructor"
			});
			customlogger.log({
				level: 'warn',
				timeStamp:  new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
				ip: require("ip").address(),
				message: "New login attempt from " + require("ip").address() + " at " + new Date().toLocaleString() + "."
			});
		},
		after: function () {
			if (stopper_SQLi(this.username)) {
				let str = this.username;
				let result = str.match(/[a-zA-Z]{3,}/g);
				let result2 = str.match(/[^a-zA-Z]+/g);

				customlogger.log({
					level: 'info',
					timeStamp:  new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
					ip: require("ip").address(),
					message: "After executing User constructor"
				});

				customlogger.log({
					level: 'warn',
					timeStamp: new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
					ip: require("ip").address(),
					message: "User << " + result + " >> tried a SQL Injection with << " + result2 + " >> "
				});
				this._username = null;
			}
			else {
				customlogger.log({
					level: 'info',
					timeStamp: new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
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

//  Root Page
app.get('/', function (request, response) {
	response.sendFile(path.join(__dirname + '/login.html'));
});


// Auth Post Request
app.post('/auth', function (request, response) {
	var newUser = new User(request.body.username, request.body.password);

	if (newUser.password && newUser.password) {

		sqlCon.getConnection((err, connection) => {
			if (err) throw err;

			// If connection succeeds
			sqlCon.query("SELECT * FROM accounts WHERE username = '" + newUser.username + " ' AND password ='" + newUser.password + "'", (err, result, fields) => {
				if (err) throw err;

				if (Object.keys(result).length === 0) {
					response.send('\nLog in failed');
					customlogger.log({
						level: 'warn',
						timeStamp:  new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
						ip: require("ip").address(),
						message: "There was no Database leakage with result: " + JSON.stringify(result, undefined, 2)
					});
				}
				else {
					response.send('\nLog in successfully');
					customlogger.log({
						level: 'warn',
						timeStamp: new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
						ip: require("ip").address(),
						message: result
					});
				}
				connection.release();
			});
		});
	}

	// If login/pass fields empty
	else {
		response.send('Please enter username and Password!');
		response.end();
	}
});

// Port
app.listen(3000);
