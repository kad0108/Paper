## Mongoose

**Mongoose**是MongoDB的一个对象模型工具，是基于node-mongodb-native开发的MongoDB nodejs驱动，可以在异步的环境下执行。同时它也是针对MongoDB操作的一个对象模型库，封装了MongoDB对文档的的一些增删改查等常用方法，让NodeJS操作Mongodb数据库变得更加灵活简单。

* Schema ： 是mongoose里会用到的一种数据模式，可以理解为表结构的定义；每个schema会映射到mongodb中的一个collection，它不具备操作数据库的能力 
* Model ： 是由schema生成的模型，可以对数据库的操作 
* Entity ： 由Model创建的实体，他的操作也会影响数据库

它们之间的关系是Schema生成Model，Model创造Entity，Model和Entity都可对数据库操作造成影响，但Model比Entity更具操作性。Model对应collection,Entity对应docment。

```
//test
find({'cid': {$gte:22777, $lte:22780}})
```

#### mongoose的两种调用写法：

1. callback

```
//model.js
function find(conditions, callback){
  xxModel.find(conditions, function(err, res){
    callback(err, res);
  })
}
module.exports = {
  find: find
}
//operate.js
var Model = require('model.js');
Model.find({...}, function(err, res){
  //find result
})
```

2. promise


   ```
//model.js
function find(conditions){
  return xxModel.find(conditions).exec();
}
module.exports = {
  find: find
}
//operate.js
var Model = require('model.js');
Model.find({...}).then(function(res){
  //find result
}).catch(functon(err){
  //find error
})
   ```

## Async

```
npm install --save async
```
#### 流程控制

* series：任务串行执行，所有任务执行结果返回给callback

* waterfall：任务串行执行，每个任务执行结果作为参数传给下一个任务，callback拿到的是最后一个任务的执行结果

* parallel：任务并行执行，每个函数立即执行，callback中拿到的数据是任务声明顺序不是执行完成顺序。

## Problem
1. 报错```FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - process out of memory```

   数据集合大小只要127MB并没有超过NodeJS默认的内存限制512MB，不太理解为啥会内存不足：但是增加内存限制貌似解决了这个报错信息

   ```
   node --max_old_space_size=8192 --optimize_for_size --max_executable_size=4096 --stack_size=4096 yourfile.js
   ```

2. 报错```Error:MongoError: connection 0 to localhost:27017 timed out```

   修改ip后还报错```Error:MongoError: connection 0 to 127.0.0.1:27017 timed out```

   remove .lock file and repair the mongod之后还是报错。。。

   先把有问题的代码贴这儿，之后可能修改的找不到这一版了：

   ```
   var LagouInfo = require('./schema.js')
   var DesData = require('./des.js');
   var async = require('async');
   //test: find({'cid': {$gte:22777, $lte:22780}})
   LagouInfo.find({}, function(res){
   	res.forEach(function(item){
   		if(item.content.trim()){
   			var sumSalary = 0;
   			item.salary.forEach(function(sitem){
   				var num;
   				if(sitem.indexOf('-') == -1){
   					num = sitem.replace(/\D+/, '');
   				}else{
   					num = parseInt(sitem.trim().split('-')[1]);
   				}
   				// console.log(sitem, num);
   				sumSalary += num;
   			})
   			var tags = item.tag.trim().split(',');
   			tags.forEach(function(tag){
   				DesData.update({'tag': tag}, {$push: {'content': item.content}});
   				DesData.update({'tag': tag}, {$inc: {'total': item.total}});
   				DesData.update({'tag': tag}, {$inc:{'salary': sumSalary}});
   			})

   		}
   	})
   })
   ```

3. 考虑每次只取部分数据出来进行分析，使用mongoose的stream来处理

   自己测试了一下这个stream方法：

   ```
   var mongoose = require('./db.js'),
   	Schema = mongoose.Schema;

   var TestSchema = new Schema({
   	name: {type: String},
   	age: {type: Number}
   })

   var TestModel = mongoose.model('stream', TestSchema, 'stream');

   var stream = TestModel.find({}).stream(), cache = [];

   stream.on('stream', function(item){
   	cache.push(item);
   	if(cache.length == 2){
   		//pause reading mongo
   		stream.pause();
   		process.nextTick(function(){
   			doSth(cache, function(){
   				cache = [];
   				// continue reading ,fetch next mongo record
   				stream.resume();
   			});
   		});
   	}
   });
   stream.on('end', function(){
   	console.log('query ended');
   });
   stream.on('close', function(){
   	console.log('query closed');
   });

   function doSth(records, callback){
   	console.log(records);
   	process.nextTick(function(){
   		callback();
   	})
   }
   ```

   报错```Mongoose: Query.prototype.stream() is deprecated in mongoose >= 4.5.0, use Query.prototype.cursor() instead```

4. **Mongoose在v4.5.0之前支持的查询是流接口，流处理是一次处理一个结果文档，避免查询结果太大不能适应内存。在v4.5.0之后Mongoose弃用流API，引入新的查询方法cursor，cursor是个对象可以遍历查询结果，MongoDB NodeJS驱动程序find查询操作返回一个cursor而不是一堆文档。**

   **CursorAPI最重要的是next方法，它获取查询匹配的下一个文档，next方法返回一个promise，可以使用co+for来遍历cursor。**

   查看[cursor文档](http://mongoosejs.com/docs/api.html#query_Query-cursor)遇到ES6的知识点Generator和co模块: 为解决callback多层嵌套的问题，提出promise链式调用，为解决then语义不明提出Generator通过yield命令交出函数的执行权用于异步操作暂停。

5. 报错```Error:MongoError: Resulting document after update is larger than 16777216```

   MongoDB限制了每个文档（BSON Object）的大小不能超过16MB，超过大小的文件可使用GridFS存储。不过还是改变一下存储的信息，将content改为cid存储。

## Reference

[循环+异步的问题](http://blog.csdn.net/fangjian1204/article/details/50585073)

[Async流程控制](https://cnodejs.org/topic/54acfbb5ce87bace2444cbfb)

[读取大量数据遍历操作](https://cnodejs.org/topic/51508570604b3d512113f1b3)

[Cursors in Mongoose 4.5](http://thecodebarbarian.com/cursors-in-mongoose-45.html)

[ES6 Generator yield co](http://es6.ruanyifeng.com/#docs/async)