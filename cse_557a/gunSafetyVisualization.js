//https://gist.github.com/dwtkns/c6945b98afe6cc2fc410#file-us-geojson
var fontFam = "helvetica";
var width = 480,
    height = 400;

var categories = ["All Laws", "Dealer Regulations", "Buyer Regulations", "Prohibitions for High-Risk Gun Possession", "Background Checks",
				  "Ammunition Regulations", "Possession Regulations", "Concealed Carry Permitting", "Assault Weapons and Large-Capacity Magazines",
				  "Child Access Prevention", "Gun Trafficking", "No Stand Your Ground", "Preemption", "No Immunity", "Domestic Violence"];

var mapSelection = "All Laws";

var projection = d3.geo.albersUsa()
    .scale(640)
    .translate([width / 2, height / 2]);

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select("#chart")
	.append("svg")
	.attr("width", width * 3)
	.attr("height", height + 100)

svg.append("text")
	.attr("y", 25)
	.attr("x", (width * 3) / 2)
	.attr("text-anchor", "middle")
	.text("Current Gun Death Rates, Laws, and Ownership by State")
	.attr("font-family", fontFam)
	.attr("font-weight", "bold")
	.attr("font-size", 20)

var svgDeaths = svg.append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("x", 0);

var svgLaws = svg.append("svg")
    .attr("width", width)
    .attr("height", height + 100)
    .attr("x", width);

svgLaws.append("text")
	.attr("y", 60)
	.attr("x", width / 2)
	.attr("text-anchor", "middle")
	.text("Number of Gun Laws")
	.attr("font-family", fontFam)
	.attr("font-weight", "bold")

var svgOwners = svg.append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("x", width * 2);

var lawsTooltip = d3.select("body").append("div")   
    .attr("id", "lawstooltip")               
    .style("opacity", 0);

var deathsTooltip = d3.select("body").append("div")   
    .attr("class", "deathstooltip")               
    .style("opacity", 0);

var gunsTooltip = d3.select("body").append("div")   
    .attr("class", "gunstooltip")               
    .style("opacity", 0);

loadData();

function loadData() {
	queue()
	    .defer(d3.json, "us-states.geojson")
	    .defer(d3.json, "gunLawsByState.json")
	    .await(ready);
}

function ready(error, us_geojson, gunLawsByState) {
	var us = us_geojson;
	var gunLaws = gunLawsByState;

	var maxLaws = getMax(gunLaws, us, "numLaws");
	var minLaws = getMin(gunLaws, us, "numLaws");

	var maxDeathRate = getMax(gunLaws, us, "deathRate");
	var minDeathRate = getMin(gunLaws, us, "deathRate");

	var maxOwners = getMax(gunLaws, us, "rateRegisteredGuns");
	var minOwners = getMin(gunLaws, us, "rateRegisteredGuns");
	
	svgLaws.append("g")
	  .selectAll("path")
	    .data(us.features)
	  	.enter()
	  	.append("path")
	    .attr("d", path)
	    .style("fill", function(d){
			var state = d["properties"]["name"];
	    	if(state in gunLaws){
	    		if(mapSelection == "All Laws") {
					return d3.hsl(240, 0.65, interpolate(gunLaws[state]["numLaws"], minLaws, maxLaws, 0.9, 0.3))
		    	}

		    	lawTypeCount = 0;
	    		for(var key in gunLaws[state]["laws"]) {
	    			console.log(gunLaws[state]["laws"][key]["category"]);
	    			if(mapSelection == gunLaws[state]["laws"][key]["category"]){
	    				lawTypeCount += 1;
	    			}
	    		}
	    		console.log(lawTypeCount);
				return d3.hsl(240, 0.65, interpolate(lawTypeCount, minLaws, maxLaws, 0.9, 0.3))
	    	}
	    	return d3.hsl(0, 1, 1)

	    })
	    .on("mouseover", function(d){
			d3.select(this)
		    	.style("fill", function(){
			    	var state = d["properties"]["name"];
			    	if(state in gunLaws){
			    		if(mapSelection == "All Laws") {
							return d3.hsl(240, 0.95, interpolate(gunLaws[state]["numLaws"], minLaws, maxLaws, 0.9, 0.3))
				    	}

				    	lawTypeCount = 0;
			    		for(var key in gunLaws[state]["laws"]) {
			    			if(mapSelection == gunLaws[state]["laws"][key]["category"]){
			    				lawTypeCount += 1;
			    			}
			    		}
						return d3.hsl(240, 0.95, interpolate(lawTypeCount, minLaws, maxLaws, 0.9, 0.3))
	    			}
	    			return d3.hsl(0, 1, 1)
		    	})
		    	.style("stroke", "black")
		    	.style("stroke-width", "1")
		    	.style("cursor", "pointer")
	    })
	    .on("click", function(d) {
			var state = d["properties"]["name"];
	    	lawsTooltip.style("visibility", "visible")
	    		.html(function() {
					var state = d["properties"]["name"];
					var text = "";
			    	if(state in gunLaws){
			    		if(mapSelection == "All Laws") {
		    				text += "<font size=4px><strong>" + state + ": " + gunLaws[state]["numLaws"] + " Laws" + "</strong></font>" + "</br></br>";

		    				for(var key in gunLaws[state]["laws"]){
		    					text += "<font size=2px><strong>" + gunLaws[state]["laws"][key]["category"] + "</strong></font>" + "</br>" + gunLaws[state]["laws"][key]["description"]+ "</br></br>";
		    				}
		    				return text
				    	}

				    	lawTypeCount = 0;
				    	var lawsText = "";
			    		for(var key in gunLaws[state]["laws"]) {
			    			if(mapSelection == gunLaws[state]["laws"][key]["category"]){
			    				lawTypeCount += 1;
			    				lawsText += "<font size=2px><strong>" + gunLaws[state]["laws"][key]["category"] + "</strong></font>" + "</br>" + gunLaws[state]["laws"][key]["description"]+ "</br></br>";
			    			}
			    		}
			    		text += "<font size=4px><strong>" + state + ": " + lawTypeCount + " " + mapSelection + " Laws" + "</strong></font>" + "</br></br>" + lawsText;
			    		return text;
			    	}


		    		var text = "<font size=4px><strong>" + state + ": " + gunLaws[state]["numLaws"] + " Laws" + "</strong></font>" + "</br></br>";

		    		for(var key in gunLaws[state]["laws"]){
		    			text += "<font size=2px><strong>" + gunLaws[state]["laws"][key]["category"] + "</strong></font>" + "</br>" + gunLaws[state]["laws"][key]["description"]+ "</br></br>";
		    		}
		    		return text
	    		})
				.style("left", (d3.event.pageX) + "px")     
                .style("top", (d3.event.pageY) + "px")
                .style("opacity", .9);
	    })
	    .on("mouseout", function(d){
			var state = d["properties"]["name"];

			//tooltip.style("visibility", "hidden"); 

	    	d3.select(this)
		    	.style("fill", function(d){
					var state = d["properties"]["name"];
			    	if(state in gunLaws){
			    		if(mapSelection == "All Laws") {
							return d3.hsl(240, 0.65, interpolate(gunLaws[state]["numLaws"], minLaws, maxLaws, 0.9, 0.3))
				    	}

				    	lawTypeCount = 0;
			    		for(var key in gunLaws[state]["laws"]) {
			    			if(mapSelection == gunLaws[state]["laws"][key]["category"]){
			    				lawTypeCount += 1;
			    			}
			    		}
			    		console.log(lawTypeCount);
						return d3.hsl(240, 0.65, interpolate(lawTypeCount, minLaws, maxLaws, 0.9, 0.3))
			    	}
			    	return d3.hsl(0, 1, 1)
		    	})
				.style("stroke-width", "0")
	    });

	var buttonsSelectAll = svgLaws.selectAll("rect")
		.data(categories);

	var buttonsEnter = buttonsSelectAll.enter()
		.append("g")
		.attr("transform", function(d) {
			var x = 0;
			var y = height - 50;
			var dist = width / (categories.length / 3);
			for(var i = 0; i < categories.length; i++){
				if(categories[i] == d){
					x = dist * (i % 5);

					if(i > 4 && i < 10){
						y = height - 25;
					}
					else if(i >= 10){
						y = height;
					}
				}
			}
			return "translate(" + x + "," + y + ")";
		})
		.on("click", function(d){
			updateData(d);
		});

	var buttonsBoxes = buttonsEnter.append("rect")
		.attr("width", 75)
		.attr("height", 20)
		.attr("rx", 6)
		.attr("ry", 6)
		.attr("fill", d3.hsl(160, 0.4, 0.60))
		.on("mouseover", function(){
			d3.select(this)
				.style("stroke", "black")
				.style("stroke-width", "1")
		})
		.on("mouseout", function(){
			d3.select(this)
				.style("stroke-width", "0")
		});

	var buttonsLabels = buttonsEnter.append("text")
		.html(function(d){
			if(d == "Concealed Carry Permitting"){
				return "Concealed Carry";
			}
			else if(d == "Assault Weapons and Large-Capacity Magazines") {
				return "Assault Weaps/Big Mags";
			}
			else if(d == "Prohibitions for High-Risk Gun Possession") {
				return "High-Risk Possession";
			}
			return d;
		})
		.attr("x", 75 / 2)
		.attr("font-size", 6)
		.attr("font-family", fontFam)
		.attr("text-anchor", "middle")
		.attr("dy", 12.5)
		.attr("font-weight", "bold")


	svgDeaths.append("g")
	  .selectAll("path")
	    .data(us.features)
	  	.enter()
	  	.append("path")
	    .attr("d", path)
	    .style("fill", function(d){
	    	if(d["properties"]["name"] in gunLaws){
				return d3.hsl(240, 0.65, interpolate(gunLaws[d["properties"]["name"]]["deathRate"], minDeathRate, maxDeathRate, 0.9, 0.3))
		    }
		    else{
		    	return d3.hsl(0, 1, 1)
		    }
	    })
	    .on("mouseover", function(d) {
			var state = d["properties"]["name"];

	    	deathsTooltip.style("visibility", "visible")
	    		.html(function(){
		    		var text = "<font size=4px><strong>" + state + "</strong></font>" + "</br>" + gunLaws[state]["deathRate"] + " Gun Deaths Per 100,000 People";

		    		return text
	    		})
				.style("left", (d3.event.pageX + 3) + "px")     
                .style("top", (d3.event.pageY + 3) + "px")
                .style("opacity", .9)

	    	d3.select(this)
		    	.style("fill", function(d){
			    	if(state in gunLaws){
						return d3.hsl(240, 0.95, interpolate(gunLaws[state]["deathRate"], minDeathRate, maxDeathRate, 0.9, 0.3))
				    }
				    else{
				    	return d3.hsl(0, 1, 1)
				    }
		    	})
		    	.style("stroke", "black")
		    	.style("stroke-width", "1")
	    })
	    .on("mouseout", function(){
	    	deathsTooltip.style("visibility", "hidden");

	    	d3.select(this)
		    	.style("fill", function(d){
			    	if(d["properties"]["name"] in gunLaws){
						return d3.hsl(240, 0.65, interpolate(gunLaws[d["properties"]["name"]]["deathRate"], minDeathRate, maxDeathRate, 0.9, 0.3))
				    }
				    else{
				    	return d3.hsl(0, 1, 1)
				    }
		    	})
				.style("stroke-width", "0")
	    });

	svgDeaths.append("text")
		.attr("y", 60)
		.attr("x", width / 2)
		.attr("text-anchor", "middle")
		.text("Gun Death Rate by State")
		.attr("font-family", fontFam)
		.attr("font-weight", "bold")

	svgOwners.append("g")
	  .selectAll("path")
	    .data(us.features)
	  	.enter()
	  	.append("path")
	    .attr("d", path)
	    .style("fill", function(d){
	    	if(d["properties"]["name"] in gunLaws){
				return d3.hsl(240, 0.65, interpolate(gunLaws[d["properties"]["name"]]["rateRegisteredGuns"], minOwners, maxOwners, 0.9, 0.1))
		    }
		    else{
		    	return d3.hsl(0, 1, 1)
		    }
	    })
	    .on("mouseover", function(d) {
	    	var state = d["properties"]["name"];

	    	gunsTooltip.style("visibility", "visible")
	    		.html(function(){
		    		var text = "<font size=4px><strong>" + state + "</strong></font>" + "</br>" + (Math.round(gunLaws[state]["rateRegisteredGuns"])) + " Guns Per 100,000 People";

		    		return text
	    		})
				.style("left", (d3.event.pageX + 3) + "px")     
                .style("top", (d3.event.pageY + 3) + "px")
                .style("opacity", .9) 

	    	d3.select(this)
		    	.style("fill", function(d){
			    	if(d["properties"]["name"] in gunLaws){
						return d3.hsl(240, 0.95, interpolate(gunLaws[d["properties"]["name"]]["rateRegisteredGuns"], minOwners, maxOwners, 0.9, 0.3))
				    }
				    else{
				    	return d3.hsl(0, 1, 1)
				    }
		    	})
		    	.style("stroke", "black")
		    	.style("stroke-width", "1")
	    })
	    .on("mouseout", function(){
	    	gunsTooltip.style("visibility", "hidden");

	    	d3.select(this)
		    	.style("fill", function(d){
			    	if(d["properties"]["name"] in gunLaws){
						return d3.hsl(240, 0.65, interpolate(gunLaws[d["properties"]["name"]]["rateRegisteredGuns"], minOwners, maxOwners, 0.9, 0.3))
				    }
				    else{
				    	return d3.hsl(0, 1, 1)
				    }
		    	})
				.style("stroke-width", "0")
	    });

	svgOwners.append("text")
		.attr("y", 60)
		.attr("x", width / 2)
		.attr("text-anchor", "middle")
		.text("Gun Ownership Rate by State")
		.attr("font-family", fontFam)
		.attr("font-weight", "bold")

}

function updateData(dataSelection){
	svgLaws.selectAll("*").remove();
	mapSelection = dataSelection;
	svgLaws.append("text")
		.attr("y", 50)
		.attr("x", width / 2)
		.attr("text-anchor", "middle")
		.text(function() {
			if(dataSelection == "All Laws"){
				return "Number of Gun Laws";
			}
			return dataSelection + " Laws Count";
		})
		.attr("font-family", fontFam)
		.attr("font-weight", "bold")
	loadData();
}

function interpolate(val, inRangeMin, inRangeMax, outRangeMin, outRangeMax){
	return ((val - inRangeMin) * (outRangeMax - outRangeMin)) / (inRangeMax - inRangeMin) + outRangeMin;
}

function getMax(data, attribute){
	max = Number.MIN_SAFE_INTEGER;
	for(var key in data){
		if(data[key][attribute] > max){
			max = data[key][attribute];
		}
	}
	return max;
}

function getMin(data, attribute){
	min = Number.MAX_SAFE_INTEGER;
	for(var key in data){
		if(data[key][attribute] < min){
			min = data[key][attribute];
		}
	}
	return min;
}


function getMax(data, us_geojson, attribute) {
		var max = Number.MIN_SAFE_INTEGER;
		if(mapSelection == "All Laws" || attribute == "deathRate" || attribute == "rateRegisteredGuns"){
			for(var key in data){
				if(data[key][attribute] > max){
					max = data[key][attribute];
				}
			}
			return max;
		}

		for(var i = 0; i < us_geojson["features"].length; i++){
			var state = us_geojson["features"][i]["properties"]["name"];
			var lawCount = 0;
			for(var key in data[state]["laws"]) {
				if(mapSelection == data[state]["laws"][key]["category"]){
					lawCount++;
				}
			}

			if(lawCount > max){
				max = lawCount;
			}
		}
		return max;
	}

function getMin(data, us_geojson, attribute) {
		var min = Number.MAX_SAFE_INTEGER;
		if(mapSelection == "All Laws" || attribute == "deathRate" || attribute == "rateRegisteredGuns"){
			for(var key in data){
				if(data[key][attribute] < min){
					min = data[key][attribute];
				}
			}
			return min;
		}
		for(var i = 0; i < us_geojson["features"].length; i++){
			var state = us_geojson["features"][i]["properties"]["name"];
			var lawCount = 0;
			for(var key in data[state]["laws"]) {
				if(mapSelection == data[state]["laws"][key]["category"]){
					lawCount++;
				}
			}

			if(lawCount < min){
				min = lawCount;
			}
		}
		return min;
	}