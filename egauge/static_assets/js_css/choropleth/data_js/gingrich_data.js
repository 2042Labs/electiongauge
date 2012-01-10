d3.json("/static/data/json/zipmap_gingrich.json", function(json) {
  data = json;
  counties.selectAll("path")
      .attr("class", quantize);
});