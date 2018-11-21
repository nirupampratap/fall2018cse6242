cuisineList = [{'Mexican' : 0, 'American (Traditional)': 0, 'Pizza': 0, 'American (New)': 0, 'Burgers': 0, 'Italian': 0, 
'Chinese': 0, 'Salad': 0, 'Sports Bars': 0, 'Seafood': 0, 'Japanese': 0, 'Barbeque': 0, 'Mediterranean': 0, 
'Sushi Bars': 0, 'Asian Fusion': 0, 'Steakhouses': 0, 'Greek': 0, 'Tex-Mex': 0, 'Thai': 0, 'Vietnamese': 0, 
'Indian': 0, 'Middle Eastern': 0, 'Southern': 0, 'Latin American': 0, 'Hawaiian': 0, 'Korean': 0, 'French': 0, 
'Caribbean': 0, 'Pakistani': 0, 'Ramen': 0, 'New Mexican Cuisine': 0, 'Modern European': 0, 'Spanish': 0, 
'African': 0, 'Cantonese': 0, 'Persian/Iranian': 0, 'Filipino': 0, 'Cuban': 0, 'Mongolian': 0, 'Lebanese': 0, 
'Polish': 0, 'Taiwanese': 0, 'German': 0, 'Turkish': 0, 'Ethiopian': 0,'Brazilian': 0, 'Afghan': 0}];



d3.select("#cuisines").selectAll("option")
	.data(Object.keys(cuisineList[0])).enter()
	.append("option")
	.attr("id", function(d,i){return i})
	.attr("value", function(d){return d})
	.text(function(d){return d});

d3.select("#submit")
	.on("click", getData);

function getData(){

	d3.selectAll("svg").remove();

	var cuisines = $('#cuisines').val();
	cuisines.forEach(function(cuisine){
		cuisineList[0][cuisine] = 1;
	});
	
	$.ajax({
		url: '/zip',
		dataType: "json",
		data: JSON.stringify({
			"data": cuisineList
		}),
		contentType: 'application/json;charset=UTF-8',
		type: 'POST',
		success: function(response){
			updateData(response);
		},
		error: function(error){
			console.log(error);
		}
	});

	Object.keys(cuisineList[0]).forEach(function(element){
		cuisineList[0][element] = 0;
	});
	
}
