d3.json("../../data/json/zipmap_obama.json", function(json) {
  data = json;
  counties.selectAll("path")
      .attr("class", quantize);
});