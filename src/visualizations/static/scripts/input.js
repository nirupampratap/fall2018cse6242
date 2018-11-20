cuisineList = ['Mexican', 'American (Traditional)', 'Pizza', 'American (New)',
   'Burgers', 'Italian', 'Chinese', 'Salad', 'Sports Bars', 'Seafood',
   'Japanese', 'Barbeque', 'Mediterranean', 'Sushi Bars', 'Asian Fusion',
   'Steakhouses', 'Greek', 'Tex-Mex', 'Thai', 'Vietnamese', 'Indian',
   'Middle Eastern', 'Southern', 'Latin American', 'Hawaiian', 'Korean',
   'French', 'Caribbean', 'Pakistani', 'Ramen', 'New Mexican Cuisine',
   'Modern European', 'Spanish', 'African', 'Cantonese', 'Persian/Iranian',
   'Filipino', 'Cuban', 'Mongolian', 'Lebanese', 'Polish', 'Taiwanese',
   'German', 'Turkish', 'Ethiopian', 'Brazilian', 'Afghan'];



d3.select("#cuisines").selectAll("option")
	.data(cuisineList).enter()
	.append("option")
	.attr("id", function(d,i){return i})
	.attr("value", function(d){return d})
	.text(function(d){return d});

d3.select("#submit")
	.on("click", getData);


var expanded = false;

function showCheckboxes() {
  var checkboxes = document.getElementById("checkboxes");
  if (!expanded) {
    checkboxes.style.display = "block";
    expanded = true;
  } else {
    checkboxes.style.display = "none";
    expanded = false;
  }
}

function getData(){

	d3.selectAll("svg").remove();

	var cuisines = $('#cuisines').val();

	
	$.ajax({
		url: '/zip',
		dataType: "json",
		data: JSON.stringify({
			"data": cuisines
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
	
}