d3.json("/static/data/json/zipmap_romney.json", function(json) {
  data = json;
  counties.selectAll("path")
      .attr("class", quantize);
});