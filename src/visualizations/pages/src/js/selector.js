
/*
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
 */


var price_range = ["Under $10", "$11-$30", "$31-$60", "Above $61"]
var select = d3.select("#selector").append('select').attr('class', 'select').attr('id', 'price_selector')

var options = select.selectAll('option').data(price_range)
.enter()
.append('option')
.text(function(d){return d})
.attr('value', function(d,i){
      /*return i;*/
      return d;
      })
/*
function change_range(){
    var res = d3.select('#price_selector').property('value');
    console.log(res);
    return res;
}
*/

var cuisine = ["Chinese", "Pizza", "Sandwitches"]
var input = d3.select("#selector").append('input').attr('class', 'input').attr('id', 'cuisine_input')
.attr('type', 'text').attr('placeholder', 'input cuisine here')
d3.select("#selector").append('input').attr('type', 'button').attr('class', 'button').attr('value', 'submit').on('click', update)

function update(){
    var price = document.getElementById('price_selector').value;
    var cur_cuisine = document.getElementById('cuisine_input').value;
    console.log(price)
    console.log(cuisine);
    d3.csv('./data/data.csv', function(error, data){
           if(error) throw error;
           header = d3.keys(data[0])
           console.log(header)
           dataset = []
           data.forEach(function(d){
                        temp = {
                            'zipcode':d['zipcode'],
                            'score': +d[cur_cuisine]
                        }
                        dataset.push(temp)
                        })
           console.log(dataset)
           dataset.sort(function(x,y){
                   return d3.descending(x.score, y.score)
                   })
           update_data(dataset)
           })
}



