var mongoose = require('./db.js'),
	Schema = mongoose.Schema;

var TestSchema = new Schema({
	name: {type: String},
	age: {type: Number}
})

var TestModel = mongoose.model('stream', TestSchema, 'stream');

var cache = [];
var co = require('co');
co(function*() {
	"use strict";
	const cursor = TestModel.find({}).cursor();
	for (let doc = yield cursor.next(); doc != null; doc = yield cursor.next()) {
		console.log(doc);
	}
});



// const tag_list = {
// 	'移动互联网': 'internet',
// 	'电子商务': 'commerce', 
// 	'金融': 'finance', 
// 	'企业服务': 'enterprise', 
// 	'教育': 'education', 
// 	'文化娱乐': 'entertain', 
// 	'游戏': 'game', 
// 	'O2O': 'o2o', 
// 	'硬件': 'hardware',
// 	'医疗健康': 'health', 
// 	'生活服务': 'lifeserve', 
// 	'广告营销': 'ad', 
// 	'旅游': 'tour', 
// 	'数据服务': 'dataserve', 
// 	'社交网络': 'social', 
// 	'分类信息': 'classify', 
// 	'信息安全': 'security', 
// 	'招聘': 'recruit', 
// 	'其他': 'other'
// };

