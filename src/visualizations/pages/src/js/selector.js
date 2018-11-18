d3.csv("./data/cuisine.csv", function(data){
	var cuisine = ["Select you cuisine"]

	data.forEach(function(d){
		cuisine.push(d.cuisine);
	});

	var select = d3.select("#selector")
		.append('select')
		.attr('class', 'select')
		.attr('id', 'select1')


	var options = select.selectAll('option')
		.data(cuisine).enter()
		.append('option')
		.attr("value", function(d,i){return i})
		.text(function(d){return d});

	function onchange(){
		selectedValue = d3.select(this).property('value');
	};

	var price = ["Under $10", "$11-$30", "$31-$60", "Above $61"]

	var select2 = d3.select("#selector").append('select')
		.attr('class', 'select')
		.attr('id', 'select2')
		.on('change', change_range)
		.attr("transform", "translate(0,10000)");

	var options2 = select2.selectAll('option')
		.data(price).enter().append('option')
		.text(function(d){return d});

	function change_range(){
		selectValue = d3.select('select').property('value');
	}
});

