var selector = d3.select("#selector").append('select').attr('class', 'select').attr('id', 'business_id')
var business_id = ['Select buisiness id', "_c3ixq9jYKxhLUB0czi0ug", "cKRMmytHxaSt8F0SMEzKqg", "8vA1d9_w4hBjOcrM7mNWFg", "sh69ApUyPhAltAMpv5vX3w", "bVl0_l6sCwjADKRLGxsXAw"]

var options = selector.selectAll('option').data(business_id).enter().append('option').text(function(d){return d;})
.on('change', onchange)


var submit = d3.select("#selector")
            .append('input')
            .attr('type', 'button')
            .attr('class', 'button')
            .attr('value', 'Submit')
            .on('click', update)

d3.selectAll(".accordion").on('click', expand);

function update(){
    var business_id = document.getElementById('business_id').value;
    d3.select("#status").remove();
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
                d3.select("#status").remove();
                d3.select("#selector").append("text").attr("id", "status").text("Done");
                createWordcloud(response);
           },
           error: function(error){
                d3.select("#status").remove()
                d3.select("#selector").append("text").attr("id", "status").text("Error");
                console.log(error)
           }
    });
    
    $.ajax({
           url: '/similar',
           dataType: "json",
           data: JSON.stringify({
                "data": business_id
           }),
           contentType: 'application/json;charset=UTF-8',
           type: 'POST',
           success: function(response){
                d3.select("#status").remove()
                d3.select("#selector").append("text").attr("id", "status").text("Done");
                update_accordion(response);
           },
           error: function(error){
                d3.select("#status").remove()
                d3.select("#selector").append("text").attr("id", "status").text("Error");
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
        var accordion = d3.select("#" + accordion_id).style("visibility", "visible").text(data[i]['attributes'] + '          : Importance score = ' + data[i]['percentage'])
        columns = ['name', 'location', 'rating', 'review_count', 'url']
        d3.selectAll('#row' + (i+1)).remove()
        var rows = d3.select("#table" + (i+1)).data(data[i]['restaurants']).append('tr').attr('id', 'row' + (i+1))
        var cells = rows.selectAll('#row' + (i+1))
        .data(function (row) {
              return columns.map(function (column) {
                                 return {column: column, value: row[column]};
                                 });
              })
        .enter()
        .append('td')
        .text(function (d) {
              console.log('d.value')
              return d.value;
              });
        
    }
    for (i = length; i < 5; i++){
        var accordion_id = "accordion_" + (i+1)
        var accordion = d3.select("#" + accordion_id).style("visibility", "hidden");
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

    reviews = reviews.filter(e => e.length < 100 && e.length > 1).slice(0, 6);

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
        d3.select("#wordcloud").select("svg").remove();
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

    d3.select("#reviews").select("svg").remove();
    d3.select("#reviews").append("svg")
        .attr("height", 300)
        .attr("width", 600)
        .selectAll(".review")
        .data(reviews).enter()
        .append("text")
        .text(function(d){return d})
        .attr("y", function(d, i){ return 50 + i * 40});
}
