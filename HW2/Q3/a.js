d3.dsv(",", "boardgame_ratings.csv", function(d) {
    return {
        date: new Date(Date.parse(d.date) + 8.64e+7),
        CatanCount: parseInt(d['Catan=count']),
        CatanRank: parseInt(d['Catan=rank']),
        DomCount: parseInt(d['Dominion=count']),
        DomRank: parseInt(d['Dominion=rank']),
        CodeCount: parseInt(d['Codenames=count']),
        CodeRank: parseInt(d['Codenames=rank']),
        TerraCount: parseInt(d['Terraforming Mars=count']),
        TerraRank: parseInt(d['Terraforming Mars=rank']),
        GloomCount: parseInt(d['Gloomhaven=count']),
        GloomRank: parseInt(d['Gloomhaven=rank']),
        MTGCount: parseInt(d['Magic: The Gathering=count']),
        MTGRank: parseInt(d['Magic: The Gathering=rank']),
        DixitCount: parseInt(d['Dixit=count']),
        DixitRank: parseInt(d['Dixit=rank']),
        MonopolyCount: parseInt(d['Monopoly=count']),
        MonopolyRank: parseInt(d['Monopoly=rank']),
        
    }
}).then(function(data) {

letter = 'a'

colorScale = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]

var maxVal = data[45].CatanCount
fields = ['Catan', 'Dom', 'Code', 'Terra', 'Gloom', 'MTG', 'Dixit', 'Monopoly']
imfuckingdumb = ['Catan', 'Dominion', 'Codenames', 'Terraforming Mars', 'Gloomhaven', 'Magic: The Gathering', 'Dixit', 'Monopoly']

const timeFormat = "%b %y"

// 2. Use the margin convention practice 
var margin = {top: 100, right: 300, bottom: 100, left: 100}
  , width = window.innerWidth - margin.left - margin.right // Use the window's width 
  , height = window.innerHeight - margin.top - margin.bottom; // Use the window's height

// 5. X scale will use the index of our data
var xScale = d3.scaleTime()
    .domain([data[0].date, data[45].date]) // input
    .range([0, width]) // output 

// 6. Y scale will use the randomly generate number 
var yScale = d3.scaleLinear()
    .domain([0, maxVal]) // input 
    .range([height, 0]); // output 

// 1. Add the SVG to the page and employ #2
var root = d3.select("body").append("svg")
    .attr('id', 'svg-' + letter)
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)

root.append('text')
    .attr('id', 'title-' + letter)
    .attr('text-anchor', 'middle')
    .attr('dx', margin.left + width/2)
    .attr('dy', margin.top/2)
    .attr("font-weight", 'bold')
    .attr('font-size', '30px')
    .text('Number of Ratings 2016-2020')

var svg = root.append("g")
    .attr('id', 'plot-' + letter)
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// 3. Call the x axis in a group tag
xstuff = svg.append("g")
    .attr("id", "x-axis-" + letter)
    .attr("transform", "translate(0," + height + ")")

xstuff.call(d3.axisBottom(xScale).tickFormat(d3.timeFormat(timeFormat))); // Create an axis component with d3.axisBottom

xstuff.append('text')
    .attr("fill", "black")          
    .attr('text-anchor', 'middle')
    .attr('dx', width/2)
    .attr('dy', 40)
    .attr('font-size', '14px')
    .text('Month')

// 4. Call the y axis in a group tag
ystuff = svg.append("g")
    .attr("id", "y-axis-" + letter)

ystuff.call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

ystuff.append('text')
    .attr("fill", "black")          
    .attr('text-anchor', 'middle')
    .attr('font-size', '14px')
    .attr('transform', 'translate(-60, ' + height/2 + ') rotate(-90)')
    .text('Num of Ratings')

// 9. Append the path, bind the data, and call the line generator 
plot = svg.append("g")
    .attr('id', 'lines-' + letter);

for (let i = 0; i < fields.length; i++) {
    yTemp = 0
    plot.append('path')
    .datum(data) 
    .attr("class", "line") 
    .style('stroke', colorScale[i])
    .attr("d", d3.line()
        .x(function(d) { return xScale(d.date); })
        .y(function(d) { 
            yTemp = yScale(d[fields[i] + 'Count'])
            return yTemp; 
        }) 
        .curve(d3.curveMonotoneX))
    plot.append('text')
        .attr('dx', width + 5)
        .attr('dy', function(d) { 
            return yTemp + 5;
        })
        .style('fill', colorScale[i])
        .text(imfuckingdumb[i])

}

}
)