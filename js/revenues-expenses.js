var datafiles = [];
//datafiles.push("FY15-16__FY16-17.csv");
datafiles.push("FY14-15__FY15-16.csv");

var years = []
datafiles.forEach(function(datafile){
  years = years.concat(datafile.slice(0,-4).split("__"));
})
console.log(years);
years.reverse();

d3.select("#fy.form-control").selectAll('option')
  .data(years)
  .enter()
  .append('option')
      .attr('value', function(d){ return d; })
      .property('selected', function(d,i){ return i == 0;})
      .text(function(d){return d;})
      ;
d3.select("#fy.form-control")
  .on('change', drawFlow);

// run once to initially populate the chart
drawFlow();

function drawFlow(){
  years.reverse();
  var fy = d3.select("#fy.form-control").node().value,//FY16-17 or FY15-16
      fy_i = years.indexOf(fy),//index of fy
      file_i = Math.floor(fy_i / 2),// index of fy div 2.... why??? returns 0
      //file_i = Math.floor(fy_i / 3),
      filename = datafiles[file_i];
  console.log(filename);
  years.reverse();

  d3.csv("/data/" + filename, function(error, data){
      if (error) {
          console.log('error', error);
          return false;
      }
      var final_data = data_wrangle(data, fy);
      do_with_budget(final_data);
  });
}// function drawFlow
