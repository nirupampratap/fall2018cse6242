

var input_field = d3.select("#selector").append("input")
                    .attr('class', 'input').attr('id', 'restaurant_input')
                    .attr('type', 'text').attr('placeholder', 'input your business ID here')

var btn = d3.select('#selector').append('input').attr('type', 'button').attr('class','button').attr('value', 'submit').on('click', update);

input_field.on('keyup', auto_complete);

function update(){
    var ID = document.getElementById('restaurant_input').value;
    console.log(ID);
    return ID;
}

function auto_complete(){
    var curr_ID = document.getElementById('restaurant_input').value;
    
}

