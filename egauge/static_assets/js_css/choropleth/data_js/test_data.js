d3.json("/static/data/json/zipmap_test.json", function(json) {
  data = json;
  counties.selectAll("path")
      .attr("class", quantize);
});