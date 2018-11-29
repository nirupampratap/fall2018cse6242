d3.select("#zipchart").append("div").text("SELECT A ZIPCODE").attr("class", "zipSelectMessage");
d3.select("#demographic").append("div").text("SELECT A ZIPCODE").attr("class", "zipSelectMessage");
d3.select("#zip-list").append("div").text("SELECT CUISINES").attr("class", "cuisineSelectMessage");

function updateData(data){

    data = Object.values(data["zipcode"]).map(function(element, index){
    	return {
    		"zipcode":element,
    		"score": Object.values(data["ffall"])[index]
    	};
    });

	d3.select("svg").remove();
	$(".cuisineSelectMessage").empty();
	d3.selectAll(".zipSelectMessage").text("SELECT A ZIPCODE");

	data = data.sort(function(a, b){return b.score - a.score}).slice(0, 7);

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

	var maxScore = d3.max(data, function(d){return d.score});

	var colorScale = d3.scaleQuantile()
		.domain([0, maxScore])
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
		.attr("width", function(d) {return (5 + ((70/maxScore) * d.score) + "%"); })
		.attr("x", 100)
		.attr("y", 5)
		.attr("rx", 5)
		.attr("ry", 5);

	list.append("text").text(function(d){return d.score.toFixed(2)})
		.attr("y", 20)
		.attr("x", "85%")
		.attr("font-size", "11");
};

function zipInsights(data){
	
	var zipcode = data.zipcode;

	var width = 500,
		height = 250,
		marginLeft = 30;

	d3.csv("static/data/zipcode_attributes.csv", function(zipdata) {
	  	var barchartData = {};
	  	zipdata.forEach(function(attribute){
	  		var attr = attribute["Attributes"];
	  		if (attribute[zipcode] != ""){
	  			barchartData[attr] = attribute[zipcode];
	  		}
	  	})

	  	barchartData = Object.entries(barchartData)
	  		.sort((a, b) => b[1] - a[1])
	  		.slice(0, 6)
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
			.attr("transform", function(d, i){var padding = i%2 == 1 ? "12" : "24"; return "translate(0," + padding + ")"});
			

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



	d3.csv("static/data/phoenix.csv", function(demographicdata){
		demographicdata = demographicdata.filter(e => parseInt(e.zipcode) == parseInt(zipcode))[0];
		
		demodata = {}
		textdata = {}

		Object.keys(demographicdata).forEach(function(key){
			if (key.endsWith("pop") && !key.startsWith("total")){
				demodata[key] = demographicdata[key];
			} 
			if (key == "median_age" || key == "median_income" || key == "housing_units" || key == "total_pop"){
				textdata[key] = demographicdata[key];
			}
		});

		d3.selectAll(".demographic").remove();

		var svg = d3.select("#demographic").append("svg")
			.attr("class", "demographic")
			.attr("height", "250")
			.attr("max-width", "175")
			.append("g")
			

		svg.selectAll(".statistics")
			.data(Object.keys(textdata)).enter()
			.append("text")
			.attr("y", function(d, i){return 70 + i * 30})
			.attr("x", 30)
			.text(function(d){return d + ": " + textdata[d]});

		
		// set the dimensions and margins of the graph
		var width = 350,
			height = 250;

		// set the ranges
		var y = d3.scaleBand()
			.range([height, 0])
			.padding(0.1);

		var x = d3.scaleLinear()
			.range([0, width - 40]);

		// append the svg object to the body of the page
		// append a 'group' element to 'svg'
		// moves the 'group' element to the top left margin

		var shift = 90

		var svg = d3.select("#demographic").append("svg")
			.attr("class", "demographic")
			.attr("width", width + shift)
			.attr("height", height + 30)
			.append("g")
			.attr("transform", "translate(" + shift + ",0)");

		// Scale the range of the data in the domains

		x.domain([0, d3.max(Object.values(demodata).map(e => +e).sort())]);
		y.domain(Object.keys(demodata));
		//y.domain([0, d3.max(data, function(d) { return d.sales; })]);

		// append the rectangles for the bar chart
		svg.selectAll(".bar")
		  .data(Object.keys(demodata))
		  .enter().append("rect")
		  .attr("class", "bar")
	      .attr("width", function(d) { return x(demodata[d]); } )
	      .attr("y", function(d) { return y(d); })
	      .attr("height", y.bandwidth());

		// add the x Axis
		svg.append("g")
		  .attr("transform", "translate(0," + height + ")")
		  .call(d3.axisBottom(x).ticks(5));

		// add the y Axis
		svg.append("g")
		  .call(d3.axisLeft(y));
		

	});
};
