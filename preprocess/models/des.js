var mongoose = require('./db.js'),
	Schema = mongoose.Schema;

var InfoSchema = new Schema({          
    tag: {type: String},
    content: {type: Array},
    total: {type: Number},
    salary: {type: Number},     
});


var Data = mongoose.model('desdata', InfoSchema, 'desdata');


function insert(obj){
	var data = new Data(obj);
	data.save(function(err, res){
		if(err) console.log('Error:' + err);
		else console.log('InesrtRes:' + res);
	})
}


function update(conditions, updateStr){
	var tmp;
	console.log('Update:', updateStr);
	if(updateStr.content) tmp = {$push, updateStr};
	else if(updateStr.total || updateStr.salary) tmp = {$inc, updateStr};
	console.log('Update: ', tmp);
	Data.update(conditions, tmp, function(err, res){
		if(err) console.log('Error:' + err);
		// else console.log(typeof res);
	})
}

function find(conditions){
	return Data.find(conditions).exec();
}


module.exports = {
	insert: insert,
	update: update,
	find: find
}