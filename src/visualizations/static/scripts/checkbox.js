cuisineList = ["Pizza", "Chinese", "Indian"];

d3.select("#checkboxes").selectAll("input")
	.data(cuisineList).enter()
	.append("input")
	.attr("type", "checkbox")
	.attr("id", function(d,i){return i})
	.text(function(d){return d});




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