var data; // loaded asynchronously

var path = d3.geo.path();

var svg = d3.select("#chart")
  .append("svg");

var counties = svg.append("g")
    .attr("id", "counties")
    .attr("class", "RdBu");

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
  return "q" + Math.min(8, ~~(data[d.id]+4 * 9 / 12)) + "-9";
}
