d3.json("../../data/json/zipmap_gingrich.json", function(json) {
  data = json;
  counties.selectAll("path")
      .attr("class", quantize);
});