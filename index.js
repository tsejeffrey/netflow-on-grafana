var express = require('express');
var bodyParser = require('body-parser');
var _ = require('lodash');
var app = express();
var timeserie = require('./series');
var table = require('./nf.json');
app.use(bodyParser.json());

app.get('/',function (req, res) {
        res.send('hello world')
})

var annotation = {
          name : "annotation name",
          enabled: true,
          datasource: "generic datasource",
          showLine: true,
}

var annotations = [
          { annotation: annotation, "title": "Donlad trump is kinda funny", "time": 1450754160000, text: "teeext", tags: "taaags" },
          { annotation: annotation, "title": "Wow he really won", "time": 1450754160000, text: "teeext", tags: "taaags" },
          { annotation: annotation, "title": "When is the next ", "time": 1450754160000, text: "teeext", tags: "taaags" }
];

function setCORSHeaders(res) {
          res.setHeader("Access-Control-Allow-Origin", "*");
          res.setHeader("Access-Control-Allow-Methods", "POST");
          res.setHeader("Access-Control-Allow-Headers", "accept, content-type");
}
app.all('/annotations', function(req, res) {
          setCORSHeaders(res);
          console.log(req.url);
          console.log(req.body);

          res.json(annotations);
          res.end();
});
app.all('/search', function(req, res){
          setCORSHeaders(res);
          var result = [];
          _.each(timeserie, function(ts) {
                      result.push(ts.target);
                    });

          res.json(result);
          res.end();
});

app.all('/query', function(req, res){
          setCORSHeaders(res);
          console.log(req.url);
          console.log(req.body);

          var tsResult = [];

          _.each(req.body.targets, function(target) {
                                                if (target.type === 'table') {
                                                        tsResult.push(table);
                                                } else {
                                                var k = _.filter(timeserie, function(t) {
                                                                console.log(t)
                                                                return t.target === target.target;
                                                              });
                                                _.each(k, function(kk) {
                                                                tsResult.push(kk)
                                                              });
                                                }
                    });
          console.log(tsResult)
          res.json(tsResult);
          res.end();
});

app.listen(4444);

console.log("Server is listening to port 4444");
