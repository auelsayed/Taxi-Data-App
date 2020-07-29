function draw(data) {
    var width = 960;
    var height = 500;

    var svg = d3.select("body").append("svg")
        .attr("width", height)
        .attr("height", width);


    var projection = d3.geoMercator()
        .fitSize([width, height], data)

    var path = d3.geoPath().projection(projection);

    svg.selectAll()
        .data([data["the_geom"]])
        .enter()
        .append("path")
        .attr("d", path);
}