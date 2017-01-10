const tag_list = {
	'移动互联网': 'internet',
	'电子商务': 'commerce', 
	'金融': 'finance', 
	'企业服务': 'enterprise', 
	'教育': 'education', 
	'文化娱乐': 'entertain', 
	'游戏': 'game', 
	'O2O': 'o2o', 
	'硬件': 'hardware',
	'医疗健康': 'health', 
	'生活服务': 'lifeserve', 
	'广告营销': 'ad', 
	'旅游': 'tour', 
	'数据服务': 'dataserve', 
	'社交网络': 'social', 
	'分类信息': 'classify', 
	'信息安全': 'security', 
	'招聘': 'recruit', 
	'其他': 'other'
};


var lagouInfo = require('./schema.js');
var desData = require('./des.js');

lagouInfo.find({'cid': {$gte:22777, $lte:22780}}, function(res){
	console.log('resLen:', res.length);
	res.forEach(function(item, index){
		if(item.content.trim()){
			var tags = item.tag.trim().split(',');
			for(var i = 0; i < tags.length; i++){
				console.log('Tag:', tags[i]);
				desData.find({'tag': tags[i]}).then(function(res){
					if(res.length == 0){
						desData.insert({
							tag: tags[i],
							content: [item.content],
							total: 0,
							salary: 0
						})
					}else{
						desData.update({'tag': tags[i]}, {'content': item.content});
					}
				}).catch(function(err){
					console.log('Err:' + err);
				})

				// desData.find({'tag': tags[i]}, function(res){
				// 	console.log('Typeof', res instanceof Array);
				// 	if(res.length == 0){
				// 		desData.insert({
				// 			tag: tags[i],
				// 			content: [item.content],
				// 			total: 0,
				// 			salary: 0
				// 		})
				// 	}else{
				// 		desData.update({'tag': tags[i]}, {'content': item.content});
				// 	}
				// })
			}

			// desData.update({'tag': tags[i]}, {'total': item.total});

			// item.salary.forEach(function(sitem){
			// 	var num = parseInt(sitem.trim().split('-')[2]);
			// 	console.log('Salary: ', sitem, num);
			// 	desData.update({'tag': tags[i]}, {'salary': num});
			// })
		}
	})
})
