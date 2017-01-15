var mongoose = require('./db.js'),
	Schema = mongoose.Schema;

var InfoSchema = new Schema({          
    tag: {type: String},
    content: {type: Array},
    total: {type: Number},
    salary: {type: Number},     
});


var Data = mongoose.model('desdata', InfoSchema, 'desdata');


function insert(obj, callback){
	var data = new Data(obj);
	data.save(function(err, res){
		if(err) console.log('Error:' + err);
		else callback(null, res);
	})
}


function update(conditions, updateStr){
	Data.update(conditions, updateStr, function(err, res){
		if(err) console.log('Error:' + err);
		else console.log('Update Success');
		// else callback(null, res);
	})
}

function find(conditions, callback){
	Data.find(conditions, function(err, res){
		if(err) console.log('Error:' + err);
		else callback(res);
	})
	// return Data.find(conditions).exec();
}


module.exports = {
	insert: insert,
	update: update,
	find: find
}