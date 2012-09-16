var context= cubism.context()
    .step(1e4)
    .size(940);

d3.select("#chart").call(function(div) {
    div.append("div")
      .attr("class", "axis")
      .call(context.axis().orient("top"));
    
    div.selectAll(".horizon")
      .data([random(7)])
      .enter().append("div")
      .attr("class", "horizon")
      .call(context.horizon()
        .extent([15, 35])
        .height(120)
        .title("Temperature"));
    
    div.append("div")
      .attr("class", "rule")
      .call(context.rule());
});

context.on("focus", function(i) {
    d3.selectAll(".value").style("right", i== null ? null : context.size() - i + "px");
});

function random(x) {
    var value = 0,
    values = [],
    i=0,
    last;
    return context.metric(function(start, stop, step, callback) {
        start = +start, stop = +stop;
        if( isNaN(last)) last = start;
        while (last < stop) {
            last += step;
            value = Math.random()*20 + 15;
            values.push(value);
        }
        callback(null, values = values.slice((start - stop) / step));
    }, x);
}
