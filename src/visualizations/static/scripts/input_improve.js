var selector = d3.select("#selector").append('select').attr('class', 'select').attr('id', 'business_id')
var business_id = ['Select buisiness id', '8NMf2dCmEGGKYR3SbMcnNA']

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
    d3.select("#selector").append("text").attr("id", "status").text("Processing ...")
    $.ajax({
           url: '/find_improve',
           dataType: "json",
           data: JSON.stringify({
                "data": business_id
           }),
           contentType: 'application/json;charset=UTF-8',
           type: 'POST',
           success: function(response){
                d3.select("#status").text("Done")
                //update_accordion(response);
                createWordcloud(response);
           },
           error: function(error){
                d3.select("#status").text("Error")
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

function createWordcloud(data){

    var textReview = {};
    var reviews = [];

    data = data.flat(2);
    data.forEach(function(element){
        element = element.split(" + ");
        if (element.length > 1){
            element.forEach(function(e){
                e = e.split("*");
                textReview[e[1].replace(/\"/g,"")] = +e[0];
            })
        } else {
            reviews.push(element.join(" + "))
        }
    })

    var width = 400,
        height = 300;

    var fill = d3v3.scale.category20();
    var word_entries = d3v3.entries(textReview);
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


    d3.select("#reviews").append("svg")
        .attr("height", "100%")
        .attr("width", "100%")
        .selectAll(".review")
        .data(reviews).enter()
        .append("text")
        .text(function(d){return d})
        .attr("y", function(d, i){ return 10 + i * 20});
}
