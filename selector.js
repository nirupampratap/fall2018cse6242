
d3.csv("./data/cuisine.csv", function(data){
       var cuisine = []
       
       data.forEach(function(d){
                    cuisine.push(d.cuisine)
       })
       console.log(cuisine)
       var select = d3.select("#selector").append('select').attr('class', 'select').on('change', onchange)
       var options = select.selectAll('option').data(cuisine)
       .enter().append('option').text(function(d){return d})
       
       function onchange(){
       selectValue = d3.select('select').property('value')
       }
       
       var price = ["Under $10", "$11-$30", "$31-$60", "Above $61"]
       console.log(price)
       var select2 = d3.select("#selector").append('select').attr('class', 'select').on('change', change_range)
       .attr("transform", "translate(0,10000)")
       var options2 = select2.selectAll('option').data(price).enter().append('option').text(function(d){return d})
       function change_range(){
       selectValue = d3.select('select').property('value')
       }
});

