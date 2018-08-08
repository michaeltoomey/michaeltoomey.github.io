var files = [];
var conditions_to_use = [];
png64 = '';
var cy;
var layout;
var layoutOptions = {'Circle': {
								'name': 'circle',
								'avoidOverlap': true,
								'equidistant': true,
								},
			 		 'Concentric': {
			 						'name': 'concentric',
			 						'minNodeSpacing': 50,
			 						'equidistant': true
			 					}
					};

function initialize(fileName) {
	$.getJSON(fileName, function(data) {
		for(var genotype in data) {
			var genotype_formatted = genotype;
			$('#checkboxes').append('<button class=\'checkHeader\' onclick=toggleExpand(' + genotype_formatted + ')>' + genotype + '</button>');
			$('#checkboxes').append('<div class=\'contentHidden\' id=\'' + genotype_formatted + '\'></div>');
			for(var networkName in data[genotype]['files']) {
				$('#' + genotype_formatted).append('<br><label><input type=\'checkbox\' class=\'checkBox\' onchange=\'updateNetworks(this)\' value=\'' + data[genotype]['files'][networkName] + '\'>' + networkName + '</label>');
			}
			$('#' + genotype_formatted).append('<br><br>');

			for(var cond in data[genotype]['conds']) {
				conditions_to_use.push(data[genotype]['conds'][cond]['name']);
			}
		}

		conditions_to_use = removeDuplicates(conditions_to_use);
		$('#options').append('<button class=\'checkHeader\' onclick=toggleExpand(conditions)>Conditions To Display</button>');
		$('#options').append('<div class=\'contentHidden\' id=\'conditions\'></div>');
		for(var cond in conditions_to_use){
			$('#conditions').append('<br><label><input type=\'checkbox\' class=\'checkBox\' onchange=\'updateEdges(this)\' value=\'' + conditions_to_use[cond] + '\' checked>' + conditions_to_use[cond] + '</label>');
		}
		$('#conditions').append('<br><br>');

		$('#options').append('<button class=\'checkHeader\' onclick=toggleExpand(lay)>Layout</button>');
		$('#options').append('<div class=\'contentHidden\' id=\'lay\'></div>');
		$('#lay').append('<select id=\'select_layout\' onchange=updateLayout(this)>');
		for(var key in layoutOptions) {
			if(key === 'Circle') {
				$('#select_layout').append('<option value=\'' + key + '\' selected=\'selected\'>' + key + '</option>');
				layout = layoutOptions['Circle'];
			}
			else 
				$('#select_layout').append('<option value=\'' + key + '\'>' + key + '</option>');
		}
		$('#lay').append('<br><br>');
	});
}

function removeDuplicates(arr) {
	let unique_array = Array.from(new Set(arr));
	return unique_array;
}

function toggleExpand(elem) {
	var d = document.getElementById(elem.id);
	if(d.className === 'contentHidden'){
		d.className = 'contentShown';
	}
	else{
		d.className = 'contentHidden';
	}
}

function updateLayout(elem) {
	layout = layoutOptions[elem.options[elem.selectedIndex].value];
	graphAndFormatNetworks();
}

function updateNetworks(checkbox) {
	if(checkbox.checked) {
		files.push(checkbox.value);
	}
	else if(files.includes(checkbox.value)) {
		files.splice(files.indexOf(checkbox.value), 1);
	}
	graphAndFormatNetworks();
}

function updateEdges(checkbox){
	if(checkbox.checked) {
		conditions_to_use.push(checkbox.value);
	}
	else if(conditions_to_use.includes(checkbox.value)) {
		conditions_to_use.splice(conditions_to_use.indexOf(checkbox.value), 1);
	}
	graphAndFormatNetworks();
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
	graphAndFormatNetworks();
}

function downloadImage() {
	png64 = cy.png({full: true, scale: 2});
	if(png64 === 'data:,') {
		alert('Image too large!');
		download.href = null;
	}
	else {
		var download = document.getElementById('downloadImage');
		download.href = png64;
		download.download = 'network.png';
	}
}

function downloadGeneFile() {
	nodes = cy.nodes();
	ids = [];
	for(var i = 0; i < nodes.length; i++) {
		ids.push(nodes[i]['_private']['data']['id']);
	}

	var csvContent = "data:text/csv;charset=utf-8,";
	ids.forEach(function(item){
   		csvContent += item + "\n";
	}); 

	var encodedUri = encodeURI(csvContent);
	var download = document.getElementById('downloadList');
	download.href = csvContent;
	download.download = 'gene_list.csv'
}

function edgeColorFunction(cond){
	if(cond == 'HighGluc') {
		return '#24B556';
	}
	else if(cond == 'LowGluc') {
		return '#E63946';
	}
	else if(cond == 'Galactose.plusLys') {
		return '#073B4C';
	}
	else if(cond == 'Galactose.minusLys') {
		return '#FFD166';
	}
	else if(cond == 'Gal') {
		return '#3DA5D9';
	}
	return 'black';
}
 
function graphAndFormatNetworks() {
	var data = [];
	for(var fileName of files) {
		$.ajax({
			dataType: 'json',
			url: fileName,
			async: false,
			success: function(d) {
				data.push(d);
			}
		});
	}
	
	cy = cytoscape({
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
					'border-width': 3,
						'background-color': function(ele) {
							metab = ele.data('metabolism');
							if(metab == 'proGrowth') {
								return '#FFFF3A';
							}
							else if(metab == 'proResp') {
								return '#81F4E1';
							}
							else if(metab == 'proRespproGrowth') {
								return '#81F4E1';
							}
							else return 'white';
						},
						'border-color': function(ele) {return (ele.data('metabolism') === 'proRespproGrowth') ? '#FFFF3A' : 'black';},
					'width': '74px',
					'height': '74px',
				}
			},
			{
				selector: 'edge',
				style: {
					'curve-style': 'bezier',
		          	'width': function(ele) {return Math.min(Math.max(Math.abs(Math.round(ele.data('lfc') * 3)), 1), 12) + 'px';},
		          	'line-color': function(ele) {return edgeColorFunction(ele.data('condition'))},
		          	'line-style': function(ele) {return (ele.data('direct') === "1") ? 'solid' : 'dashed';},
		          	'target-arrow-shape': function(ele) {return (ele.data('lfc') < 0 ? 'triangle' : 'tee');},
		          	'target-arrow-color': function(ele) {return edgeColorFunction(ele.data('condition'))},
		          	'opacity': function(ele) {return conditions_to_use.includes(ele.data('condition')) ? 1 : 0;},
		          	'control-point-step-size': 50
				}
			}
		],
		layout: layout
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