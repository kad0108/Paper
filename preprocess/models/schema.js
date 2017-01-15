var mongoose = require('./db.js'),
	Schema = mongoose.Schema;

var LagouSchema = new Schema({
	name: {type: String},
	cid: {type: Number},
	process: {type: String},
	content: {type: String},
	url: {type: String},
	tag: {type: String},
	total: {type: Number},
	salary: {type: Array}
});


var Lagou = mongoose.model('lagou', LagouSchema, 'lagou');

function update(conditions, update){
	Lagou.update(conditions, update, function(err, res){
		if(err) console.log('Error:' + err);
		else console.log('Res:' + res);
	})
}

function del(conditions){
	Lagou.remove(conditions, function(err, res){
		if(err) console.log('Error:' + err);
		else console.log('Res:' + res);
	})
}

function find(conditions, callback){
	Lagou.find(conditions, function(err, res){
		if(err) console.log('Error:' + err);
		else callback(res);
	})
}

module.exports = Lagou;