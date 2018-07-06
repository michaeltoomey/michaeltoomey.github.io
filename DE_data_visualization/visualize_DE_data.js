var files = [];

function showCheckboxes() {
	// var x = document.getElementById('checkboxes');
	// if(x.style.display === 'none') {
	// 	x.style.display = 'block';
	// }
	// else {
	// 	x.style.display = 'none';
	// }
}

function parseFileMetadata(fileName) {
	$.getJSON(fileName, function(data) {
		for(var genotype in data) {
			$('#checkboxes').append('<h2 class=\'checkHeader\' id=\'' + genotype + '\'>' + genotype + '</h2>')
			for(var networkName in data[genotype]) {
				$('#' + genotype).append('<br><input class=\'checkBox\' type=\'checkbox\' onchange=\'updateNetworks(this)\' value=\'' + data[genotype][networkName] + '\'>' + networkName + '</input>')
			}
		}
	});
}

function updateNetworks(checkbox) {
	if(checkbox.checked) {
		files.push(checkbox.value);
	}
	else if(files.includes(checkbox.value)) {
		files.splice(files.indexOf(checkbox.value), 1);
	}

	loadDifferentialExpressionNetwork(files);
}

function combineNetworks(networkArray) {
	if(networkArray.length == 1) {
		return networkArray[0];
	}
	
	combinedNetwork = {edges: [], nodes: []}
	for(var network of networkArray) {
		combinedNetwork['nodes'] = combinedNetwork['nodes'].concat(network['nodes']);
		combinedNetwork['edges'] = combinedNetwork['edges'].concat(network['edges']);
	}
	return combinedNetwork;
}

function resetView() {
	loadDifferentialExpressionNetwork(files);
}

function loadDifferentialExpressionNetwork(fileNames) {
	var data = [];
	for(var fileName of fileNames) {
		$.ajax({
			dataType: 'json',
			url: fileName,
			async: false,
			success: function(d) {
				data.push(d);
			}
		});
	}
	
	var cy = cytoscape({
		container: document.getElementById('cy'),
		elements: combineNetworks(data),
		style: [
			{
				selector: 'node',
				style: {
					'label': 'data(name)',
						'text-halign': 'center',
						'text-valign': 'center',
						'font-size': 13,
					'border-width': 5,
						'background-color': function(ele) {
							metab = ele.data('metabolism');
							if(metab == 'proGrowth') {
								return 'yellow';
							}
							else if(metab == 'proResp') {
								return 'cyan';
							}
							else if(metab == 'proRespproGrowth') {
								return 'cyan';
							}
							else return 'white';
						},
						'border-color': function(ele) {
							metab = ele.data('metabolism');
							if(metab == 'proRespproGrowth') {
								return 'yellow';
							}
							else return 'black';
						},
					'width': '75px',
					'height': '75px',
				}
			},
			{
				selector: 'edge',
				style: {
					'curve-style': 'bezier',
		          	'width': function(ele) {
		          		size = Math.abs(Math.round(ele.data('lfc') * 3));
		          		size = Math.max(size, 1);
		          		size = Math.min(size, 12);
		          		return size + 'px';
		          	},
		          	'line-color': function(ele){
		          		cond = ele.data('condition');
		          		if(cond == 'HighGluc') {
		          			return 'green';
		          		}
		          		else if(cond == 'LowGluc') {
		          			return 'red';
		          		}
		          		else if(cond == 'Galactose.plusLys') {
		          			return 'cyan';
		          		}
		          		else if(cond == 'Galactose.minusLys') {
		          			return 'blue';
		          		}
		          		return 'black';
		          	},
		          	'line-style': function(ele) {
		          		if(ele.data('direct') == "1") {
		          			return 'solid';
		          		}
		          		else return 'dashed';
		          	},
		          	'target-arrow-shape': function(ele) {
		          		return (ele.data('lfc') < 0 ? 'triangle' : 'tee');
		          	},
		          	'target-arrow-color': function(ele){
		          		cond = ele.data('condition');
		          		if(cond == 'HighGluc') {
		          			return 'green';
		          		}
		          		else if(cond == 'LowGluc') {
		          			return 'red';
		          		}
		          		else if(cond == 'Galactose.plusLys') {
		          			return 'cyan';
		          		}
		          		else if(cond == 'Galactose.minusLys') {
		          			return 'blue';
		          		}
		          		return 'black';
		          	}
				}
			}
		],
		layout: {
			'name': 'circle',
			'fit': false,
			'avoidOverlap': true,
			'avoidOverlapPadding': 20
		}
	});

	cy.on('mouseover', 'node', function(event) {
		var elemData = event.target._private.data;
		var sysName = elemData.id;
		var metab = function(data){
			if(data =='proGrowth') {
				return 'Growth';
			}
			else if(data =='proResp') {
				return 'Respiration';
			}
			else if(data =='proRespproGrowth') {
				return 'Respiration and Growth';
			}
			return 'No associated metabolic phenotype';
		}

		$('#cy').append('<div id=\'infobox\' class=\'tooltip\'><b>Systematic Name:</b> ' + sysName +'<br><b>Metabolic Phenotype:</b> ' + metab(elemData.metabolism) + '</div>')
		var d = document.getElementById('infobox');
		d.style.position = 'absolute';
		d.style.left = event.renderedPosition.x + 15 + 'px';
		d.style.top = event.renderedPosition.y + 15 + 'px';
	});

	cy.on('mouseout', 'node', function(event) {
		var d = document.getElementById('infobox');
		if(d != null) {
			d.parentNode.removeChild(d);
		}
	});

	cy.on('mouseover', 'edge', function(event) {
		var elemData = event.target._private.data;
		var interaction = elemData.source + ' ' + elemData.interaction + ' ' + elemData.target;
		var lfc = Math.round(elemData.lfc * 100) / 100;

		$('#cy').append('<div id=\'infobox\' class=\'tooltip\'><b>Interaction:</b> ' + interaction +'<br><b>LFC:</b> ' + Math.abs(lfc) + '<br><b>Condition:</b> ' + elemData.condition + '<br><b>Media:</b> ' + elemData.mediaSugar + '<br><b>Lysine:</b> ' + elemData.lysInMedia + '</div>');
		var d = document.getElementById('infobox');
		d.style.position = 'absolute';
		d.style.left = event.renderedPosition.x + 15 + 'px';
		d.style.top = event.renderedPosition.y + 15 + 'px';
	});
	cy.on('mouseout', 'edge', function(event) {
		var d = document.getElementById('infobox');
		if(d != null) {
			d.parentNode.removeChild(d);
		}
	});

	cy.fit();
}