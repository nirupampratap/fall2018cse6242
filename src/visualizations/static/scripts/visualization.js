d3.select("#zipchart").append("div").text("SELECT A ZIPCODE").attr("class", "zipSelectMessage");
d3.select("#wordcloud").append("div").text("SELECT A ZIPCODE").attr("class", "zipSelectMessage");
d3.select("#zip-list").append("div").text("SELECT CUISINES").attr("class", "cuisineSelectMessage");

function updateData(data){
    console.log(data)
	d3.select("svg").remove();
	$(".cuisineSelectMessage").empty();
	d3.selectAll(".zipSelectMessage").text("SELECT A ZIPCODE");

	data = data.sort(function(a, b){return b.score - a.score}).slice(0, 8);

	var svg = d3.select("#zip-list")
		.append("svg")
		.attr("height", "300px")
		.attr("width", "100%");

	var list = svg.selectAll(".zip")
		.data(data).enter()
		.append("g")
		.attr("transform", function(d, i){return "translate(0," + ((i * 30) + 40) + ")"})
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
			zipInsights(d);
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
		.attr("rx", 5)
		.attr("ry", 5);

	var scores = list.append("rect")
		.attr("class", "score")
		.attr("fill", function(d) { return colorScale(d.score); })
		.attr("height", "20px")
		.attr("width", function(d) {return (5 + d.score * 0.70 + "%"); })
		.attr("x", 100)
		.attr("y", 5)
		.attr("rx", 5)
		.attr("ry", 5);

	list.append("text").text(function(d){return d.score + "%"})
		.attr("y", 20)
		.attr("x", "90%")
		.attr("font-size", "11");
};

function zipInsights(data){
	

	var width = 500,
		height = 250,
		marginLeft = 30;

	d3.csv("static/data/zipcode_attributes.csv", function(zipdata) {
	  	var zipcode = data.zipcode;
	  	var barchartData = {};
	  	zipdata.forEach(function(attribute){
	  		var attr = attribute[""];
	  		if (attribute[zipcode] != ""){
	  			barchartData[attr] = attribute[zipcode];
	  		}
	  	})

	  	barchartData = Object.entries(barchartData)
	  		.sort((a, b) => b[1] - a[1])
	  		.slice(0, 5)
	  		.reduce(function(acc, element){
		  		acc[element[0]] = element[1];
		  		return acc;
		  	}, {});

		// Chart
		d3.select(".chart").remove();
		$(".zipSelectMessage").empty();


		var svg = d3.select("#zipchart").append("svg")
			.attr("class", "chart")
			.attr("width", width)
			.attr("height", height)
			.append("g");

		height -= 30;
		
		var x = d3.scaleBand().rangeRound([0, width - 50]).padding(.05);

		var y = d3.scaleLinear().range([height, 0]);

		var xAxis = d3.axisBottom(x);

		var yAxis = d3.axisLeft(y).ticks(10);



		x.domain(Object.keys(barchartData));
		y.domain([0, d3.max(Object.values(barchartData))]);

		svg.selectAll("bar")
			.data(Object.entries(barchartData))
			.enter().append("rect")
			.attr("x", function(d) { return x(d[0]) + marginLeft; })
			.attr("width", x.bandwidth())
			.attr("y", function(d) { return y(d[1]); })
			.attr("height", function(d) { return height - y(d[1]); })
			.on("mouseover", function(){
				d3.select(this).attr("fill", "#D8D8D8");
			})
			.on("mouseout", function(){
				d3.select(this).attr("fill", "black");
			});

		svg.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(" + marginLeft + "," + height + ")")
			.call(xAxis)
			.selectAll("text")
			.style("text-anchor", "center")
			.style("font-weight", "bold")
			.attr("dx", "-.8em")
			.attr("dy", "-.55em")
			.attr("transform", function(d, i){var padding = i%2 == 1 ? "10" : "20"; return "translate(0," + padding + ")"});
			

		svg.append("g")
			.attr("transform", "translate(" + marginLeft + ",0)")
			.attr("class", "y axis")
			.call(yAxis)
			.append("text")
			.attr("transform", "rotate(-90)")
			.attr("y", 6)
			.attr("dy", ".71em")
			.style("text-anchor", "end")
			.text("Importance");
	});

	// Word cloud
	
	d3.select(".wordcloud").remove();
	var fill = d3v3.scale.category20();

	var word_entries = d3v3.entries(data.textReview);

	var xScale = d3v3.scale.linear()
		.domain([0, d3v3.max(word_entries, function(d) {
			return d.value;
		})
		])
		.range([10,100]);

	d3v3.layout.cloud().size([width, height])
		.timeInterval(20)
		.words(word_entries)
		.fontSize(function(d) { return xScale(+d.value); })
		.text(function(d) { return d.key; })
		.rotate(function() { return ~~(Math.random() * 2) * 90; })
		.font("Impact")
		.on("end", draw)
		.start();

	function draw(words) {
		d3v3.select("#wordcloud").append("svg")
			.attr("class", "wordcloud")
			.attr("width", width)
			.attr("height", height)
			.append("g")
			.attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
			.selectAll("text")
			.data(words)
			.enter().append("text")
			.style("font-size", function(d) { return xScale(d.value) + "px"; })
			.style("font-family", "Impact")
			.style("fill", function(d, i) { return fill(i); })
			.attr("text-anchor", "middle")
			.attr("transform", function(d) {
				return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
			})
			.text(function(d) { return d.key; });
	}

	d3v3.layout.cloud().stop();
};
