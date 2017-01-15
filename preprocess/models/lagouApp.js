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

var DesModel = require('./des.js');

var co = require('co');

co(function*() {
	"use strict";
	const cursor = Lagou.find({}).cursor();
	for (let doc = yield cursor.next(); doc != null; doc = yield cursor.next()) {
		// console.log(doc);
		if(doc.content.trim() && doc.content.trim() != '该公司尚未添加公司介绍'){
			var sumSalary = 0;
			doc.salary.forEach(function(sitem){
				var num;
				if(sitem.indexOf('-') == -1) num = parseInt(sitem);
				else num = parseInt(sitem.trim().split('-')[1]);
				// console.log(sitem, num);
				sumSalary += num;
			});
			var tags = doc.tag.trim().split(',');
			tags.forEach(function(tag){
				DesModel.update({'tag': tag}, {$push: {'content': doc.cid}});
				DesModel.update({'tag': tag}, {$inc: {'total': doc.total}});
				DesModel.update({'tag': tag}, {$inc:{'salary': sumSalary}});
			})
		}
	}
	console.log('Finished');
});
