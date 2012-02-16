var data; // loaded asynchronously
var candidate; // candidate's slug
var cand_url; // candidate's data url

var path = d3.geo.path();

var svg = d3.select("#chart")
    .append("svg");

var counties = svg.append("g")
    .attr("id", "counties")
    .attr("class", "OrRd");

var states = svg.append("g")
    .attr("id", "states");

d3.json("/static/data/d3/us-counties.json", function(json) {
    counties.selectAll("path")
        .data(json.features)
        .enter().append("path")
        .attr("class", data ? quantize : null)
        .attr("d", path);
});

d3.json("/static/data/d3/us-states.json", function(json) {
    states.selectAll("path")
        .data(json.features)
        .enter().append("path")
        .attr("d", path);
});


function quantize(d) {
  var q = Math.min(8, Math.round(Math.log(data[d.id])))
  q = q ? q : 0
  return "q" + q + "-9"
}

function loadjson(data_file) {
  d3.json(data_file, function(json) {
  data = json;
  counties.selectAll("path")
      .attr("class", quantize);
  });
}

$('a[data-toggle="tab"]').on('shown', function (e) {
  var cand_split = $(this).attr('href').split('#');
  // candidate results in ['','romney']
  candidate = cand_split[1]
  cand_url = '/static/data/json/zipmap_' + candidate + '.json'
  loadjson(cand_url);
});