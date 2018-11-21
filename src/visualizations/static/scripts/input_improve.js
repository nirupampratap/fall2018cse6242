var selector = d3.select("#selector").append('select').attr('class', 'select').attr('id', 'business_id')
var business_id = ['qerwerwer', '123123']

var options = selector.selectAll('option').data(business_id).enter().append('option').text(function(d){return d;})
.on('change', onchange)


var submit = d3.select("#selector")
            .append('input')
            .attr('type', 'button')
            .attr('class', 'button')
            .attr('value', 'submit')
            .on('click', update)

d3.selectAll(".accordion").on('click', expand)

function update(){
    var business_id = document.getElementById('business_id').value;
    console.log(business_id);
    
    $.ajax({
           url: '/find_improve',
           dataType: "json",
           data: JSON.stringify({
                "data": business_id
           }),
           contentType: 'application/json;charset=UTF-8',
           type: 'POST',
           success: function(response){
                update_accordion(response)
           },
           error: function(error){
                console.log(error)
           }
    })
}

function expand(){
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if(panel.style.display ==="block"){
        panel.style.display = "none";
    }
    else{
        panel.style.display = "block";
    }
}

function update_accordion(data){
    console.log(data.length);
    var i = 0;
    var length = 0;
    if(data.length > 5){
        length = 5;
    }
    else{
        length = data.length;
    }
    for(i = 0; i < length; i++){
        var accordion_id = "accordion_" + (i+1)
        console.log(accordion_id);
        var accordion = d3.select("#" + accordion_id).text(data[i]['attribute'] + '          ' + data[i]['importance'] + '          ' + data[i]['percentage'])
        var paragraph = d3.selectAll("#paragraph_in_" + (i+1)).remove();
        var rest_length = data[i]['restaurants'].length
        var j = 0;
        for(j = 0; j < rest_length; j++){
            d3.select("#panel_in_" + (i+1)).append('p').attr('id', 'paragraph_in_' + (i+1)).text(data[i]['restaurants'][j]['name'] + ' ' + data[i]['restaurants'][j]['location'] + ' ' + data[i]['restaurants'][j]['ratings'] + ' ' + data[i]['restaurants'][j]['price'])
        }
    }
}
