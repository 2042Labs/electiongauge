d3.json("https://s3.amazonaws.com/egauge/zipmap_obama.json", function(json) {
  data = json;
  counties.selectAll("path")
      .attr("class", quantize);
});