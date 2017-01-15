const tag_list = [
    '移动互联网','电子商务','金融',
    '企业服务','教育','文化娱乐',
    '游戏','O2O','硬件',
    '医疗健康','生活服务','广告营销',
    '旅游','数据服务','社交网络',
    '分类信息','信息安全','招聘','其他'
];

var desData = require('./des.js');

var async = require('async');

async.map(tag_list, function(tag, callback){
    desData.insert({
        tag: tag,
        content: [],
        total: 0,
        salary: 0
    }, callback)
}, function(err, res){
    console.log('InsertTag Success');
})