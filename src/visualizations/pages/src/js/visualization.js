var zip = [];

d3.csv("./data/data.csv", function(data) {

	data.forEach(e => e.score = Math.floor(Math.random() * 100));

	// data.sort(function(a,b){return b.score - a.score});

	var svg = d3.select("#zip-list")
			.append("svg")
			.attr("height", "400px")
			.attr("width", "100%")

	var list = svg.selectAll(".zip")
			.data(data).enter()
			.append("g")
			.attr("transform", function(d, i){return "translate(0," + i * 30 + ")"})
			.on("mouseover", function(){
				d3.select(this).style("cursor", "pointer");
				d3.select(this).attr("opacity", 0.3);
			})
	        .on("mouseout", function(){
	        	d3.select(this).style("cursor", "default");
	        	d3.select(this).attr("opacity", 1);
	        })
	        .on("click", function(d){
	        	var map = new google.maps.Map(document.getElementById('map'), {
	        		zoom: 10,
	        		center: {lat: 33.753, lng: -84.386}
	        	});
	        	var geocoder = new google.maps.Geocoder();
        		geocodeAddress(geocoder, map, d.zipcode);
        	});

	list.append("rect")
		.attr("class", "zip-container")
		.attr("height", "30px")
		.attr("width", "100%");

	var zipcode = list.append("text")
			.text(function(d){return d.zipcode})
			.attr("y", 20)
			.attr("x", 10)
	
	var colors = ["#ff0000","#ff4000","#ff8000","#ffbf00","#ffff00","#bfff00","#80ff00","#40ff00"];

	var colorScale = d3.scaleQuantile()
					.domain([0, 90, d3.max(data, function(d){return d.score})])
					.range(colors);

	var bars = list.append("rect")
			.attr("class", "bar")
			.attr("fill", "#E8E8E8")
			.attr("height", "20px")
			.attr("width", "75%")
			.attr("x", 100)
			.attr("y", 5)
			.attr("rx", 10)
			.attr("ry", 10);

	

	var scores = list.append("rect")
			.attr("class", "score")
			.attr("fill", function(d) { return colorScale(d.score); })
			.attr("height", "20px")
			.attr("width", function(d) { return d.score * 0.75 + "%"; })
			.attr("x", 100)
			.attr("y", 5)
			.attr("rx", 10)
			.attr("ry", 10);
});