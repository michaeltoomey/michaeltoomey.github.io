Data dataSet = new Data("presElectionAndVoterDemographics.csv");  
ParallelCoordinates graph;

float widthBorder;
float heightBorder;

Dimension sortByDimension;
SelectionBox selectionBox;
Point selectionBoxInitial = new Point(0, 0);
Point selectionBoxFinal = new Point(0, 0);

void setup() {
  surface.setSize(1000, 1000);
  background(256, 256, 256);
  rectMode(CORNERS);


  dataSet.loadData();
  graph = new ParallelCoordinates(dataSet.dimensions, dataSet.data);
}

void draw() {
  background(255);
  widthBorder = (0.05 * width);
  heightBorder = (0.05 * height);
  
  colorMode(RGB);
  stroke(0);
  if(mouseX > width - 0.75 * widthBorder && mouseX < width - 0.25 * widthBorder
     && mouseY > height - 0.75 * heightBorder && mouseY < height - 0.25 * heightBorder){
     strokeWeight(3);
  }
  else{
    strokeWeight(0);
  }
  fill(195, 195, 195, 15);
  rect(width - 0.25 * widthBorder, height - 0.25 * heightBorder, width - 0.75 * widthBorder, height - 0.75 * heightBorder);
  fill(0, 0, 0);
  textAlign(CENTER, CENTER);
  text("Reset", width - 0.25 * widthBorder, height - 0.25 * heightBorder, width - 0.75 * widthBorder, height - 0.75 * heightBorder);
  
  if(mouseX > width - 0.75 * widthBorder && mouseX < width - 0.25 * widthBorder
     && mouseY > height - 0.75 * heightBorder && mouseY < height - 0.25 * heightBorder){
  }
  
  
  stroke(0, 0, 0);
  strokeWeight(1.5);
  fill(64, 104, 82, 50);
  rect(selectionBoxInitial.x, selectionBoxInitial.y, selectionBoxFinal.x, selectionBoxFinal.y);
  graph.drawGraph();
  selectionBox = new SelectionBox(dataSet.dimensions, dataSet.data);
}

void mousePressed() {
  graph.dimensionSort();
  graph.flipDimension();
  
  selectionBoxInitial = new Point(mouseX, mouseY);
  selectionBoxFinal = new Point(mouseX, mouseY);
  
  if(mouseX > width - 0.75 * widthBorder && mouseX < width - 0.25 * widthBorder
     && mouseY > height - 0.75 * heightBorder && mouseY < height - 0.25 * heightBorder){
    selectionBox.resetLineHighlights();
  }
}

void mouseDragged() {
  selectionBoxFinal.x = mouseX;
  selectionBoxFinal.y = mouseY;
}

void mouseReleased() {
  if(selectionBoxInitial.x != selectionBoxFinal.x &&
     selectionBoxInitial.y != selectionBoxFinal.y){
    selectionBox.highlightLines(selectionBoxInitial, selectionBoxFinal);
  }
  selectionBoxInitial = new Point(0, 0);
  selectionBoxFinal = new Point(0, 0);
}

class ConnectorLine {
  Point startPoint;
  Point endPoint;
  Dimension dimensionFrom;
  Dimension dimensionTo;
  float saturation = 240;
  
  ConnectorLine() {
  }
}

class Data {
  String dataPath;
  String[] colNames;
  Dimension[] dimensions;
  DataLine[] data;
  
  Data(String dataPath) {
    this.dataPath = dataPath;
  }

  void loadData() {
    Table table = loadTable(this.dataPath);
    int numRows = table.getRowCount();
    int numCols = table.getColumnCount();
    data = new DataLine[numRows - 1];
    colNames = new String[numCols - 1];
    dimensions = new Dimension[numCols - 1];
    float[] dimensionMins = new float[numCols - 1];
    float[] dimensionMaxes = new float[numCols - 1];
    for(int i = 0; i < dimensionMins.length; ++i) {
      dimensionMins[i] = Float.MAX_VALUE;
      dimensionMaxes[i] = -Float.MAX_VALUE;
    }

    //get column names located in first row
    for(int i = 1; i < numCols; ++i){
      colNames[i - 1] = table.getString(0, i);
      dimensions[i - 1] = new Dimension(table.getString(0, i));
    }
    
    sortByDimension = dimensions[0];
    
    //get row information
    for(int i = 0; i < data.length; ++i) {
      //initialize new data line containing row information
       data[i] = new DataLine(table.getString(i + 1, 0), dimensions);

      //get and store row information
      for(int j = 1; j < numCols; ++j) {
        float val = table.getFloat(i + 1, j);
        data[i].values[j - 1] = val;
        
        //find the max and min of each dimension
        dimensionMins[j - 1] = min(val, dimensionMins[j - 1]);
        dimensionMaxes[j - 1] = max(val, dimensionMaxes[j - 1]);
      }
      data[i].instantiateLines(dimensions);
    }

    //set dimension min and max values
    for(int i = 0; i < dimensions.length; ++i) {
      dimensions[i].min = dimensionMins[i];
      dimensions[i].max = dimensionMaxes[i];
    }
  } 
}

class DataLine {
  String name;
  Dimension[] dimensions;
  ConnectorLine[] lines;
  float[] values;
  float saturation = 240;
  float opacity = 255;
  float lineWeight = 1.5;
  
  DataLine(String name, Dimension[] dimensions) {
    this.name = name;
    this.dimensions = dimensions;
    lines = new ConnectorLine[dimensions.length - 1];
    values = new float[dimensions.length];
  }
  
  void instantiateLines(Dimension[] dimensions) {
    for(int i = 0; i < lines.length; ++i) {
      lines[i] = new ConnectorLine();
      lines[i].dimensionFrom = dimensions[i];
      lines[i].dimensionTo = dimensions[i + 1];
    } 
  }
  
  String toString() {
    String out = this.name + "\n";
    for(int i = 0; i < values.length; ++i) {
      out += dimensions[i] + ": " + values[i] + "\n";
    }
    return out;
  }
}

class Dimension {
  String name;
  float min;
  float max;
  Point minCoordinate;
  Point maxCoordinate;
  
  Dimension(String name) {
    this.name = name;
  }
  
  String toString() {
    return this.name;
  }
}

class ParallelCoordinates {
  Dimension[] dimensions;
  DataLine[] data;
  
  float graphWidth;
  float graphHeight;
  float dimensionBarWidthHalf;
  float barDistance;

  ParallelCoordinates(Dimension[] dimensions, DataLine[] data) {
    this.dimensions = dimensions;
    this.data = data;
  }
  
  //draws parallel coordinates
  void drawGraph() {
    graphWidth = width - 2 * widthBorder;
    graphHeight = height - 2 * heightBorder;
    
    dimensionBarWidthHalf = graphWidth / 150;
    barDistance = graphWidth / (dimensions.length - 1);

    int sortByDimensionIndex = -1;

    //build dimension bars
    for(int i = 0; i < dimensions.length; ++i) {
      //find positions of dimension bars
      Point minCoordinate = new Point (i * barDistance + widthBorder, heightBorder + graphHeight);
      Point maxCoordinate = new Point(i * barDistance + widthBorder, heightBorder);
      dimensions[i].minCoordinate = minCoordinate;
      dimensions[i].maxCoordinate = maxCoordinate;
      
      //draw dimension bars and check for hovering
      colorMode(RGB);
      stroke(0, 0, 0);
      strokeWeight(0);
      line(minCoordinate.x, minCoordinate.y, maxCoordinate.x, maxCoordinate.y);
      fill(195, 195, 195, 15);
      stroke(0);
      if(this.mouseOverDimension(dimensions[i])) {
        strokeWeight(3);
      }
      if(dimensions[i] == sortByDimension) {
        fill(64, 104, 82, 75);
      }
      rect(minCoordinate.x - dimensionBarWidthHalf, minCoordinate.y, maxCoordinate.x + dimensionBarWidthHalf, maxCoordinate.y);
      strokeWeight(0);
      
      //draw flip buttons
      if(this.mouseOverFlipButton(dimensions[i])) {
        strokeWeight(3);
      }
      fill(195, 195, 195, 15);
      rect(minCoordinate.x - dimensionBarWidthHalf, minCoordinate.y + 0.75 * heightBorder, maxCoordinate.x + dimensionBarWidthHalf, minCoordinate.y + 0.25 * heightBorder);
      
      if(sortByDimension == dimensions[i]) {
        sortByDimensionIndex = i;
      }
    }
        
    //draw lines connecting dimension bars
    for(int i = 0; i < data.length; ++i) {
      for(int j = 0; j < dimensions.length - 1; ++j) {
        //get start and end positions of connector lines
        float startPoint = map(data[i].values[j], dimensions[j].min, dimensions[j].max, graphHeight + heightBorder, heightBorder);
        float endPoint = map(data[i].values[j + 1], dimensions[j + 1].min, dimensions[j + 1].max, graphHeight + heightBorder, heightBorder);
         
        //store start and end positions of connector lines
        data[i].lines[j].startPoint = new Point(dimensions[j].minCoordinate.x, startPoint);
        data[i].lines[j].endPoint = new Point(dimensions[j + 1].minCoordinate.x, endPoint);
        
        //draw connector lines
        colorMode(HSB);
        stroke(map(data[i].values[sortByDimensionIndex], sortByDimension.min, sortByDimension.max, 360, 145), data[i].saturation, 100, data[i].opacity);
        strokeWeight(data[i].lineWeight);
        line(data[i].lines[j].startPoint.x, data[i].lines[j].startPoint.y, data[i].lines[j].endPoint.x, data[i].lines[j].endPoint.y);
      }
    }
    
    String textToDisplay = "";
    int numItems = 0;
    for(int i = 0; i < data.length; ++i) {
      numItems = this.mouseOverLine(data[i], textToDisplay);
    }
    this.toolTip(textToDisplay, numItems);

  }
  
  //change the dimension by which line color is sorted
  void dimensionSort() {
    for(int i = 0; i < dimensions.length; ++i) {
      if(this.mouseOverDimension(dimensions[i]) ) {
        sortByDimension = dimensions[i];
      }
    }
  }
  
  //check if mouse is hovering over dimension bar
  boolean mouseOverDimension(Dimension dimension) {
    if(mouseX > dimension.minCoordinate.x - dimensionBarWidthHalf && mouseX < dimension.maxCoordinate.x + dimensionBarWidthHalf &&
       mouseY < dimension.minCoordinate.y && mouseY > dimension.maxCoordinate.y) {
      return true;
    }
    return false;
  }
  
  //flip dimension
  void flipDimension() {
    for(int i = 0; i < dimensions.length; ++i) {
      if(this.mouseOverFlipButton(dimensions[i]) ) {
        float max = dimensions[i].max;
        dimensions[i].max = dimensions[i].min;
        dimensions[i].min = max;
      }
    }
  }
  
  //check if mouse is hovering over flip button
  boolean mouseOverFlipButton(Dimension dimension) {
    if(mouseX > dimension.minCoordinate.x - dimensionBarWidthHalf && mouseX < dimension.maxCoordinate.x + dimensionBarWidthHalf &&
       mouseY < heightBorder + graphHeight + 0.75 * heightBorder && mouseY > heightBorder + graphHeight + 0.25 * heightBorder) {
      return true;
    }
    return false;
  }
  
  int mouseOverLine(DataLine data, String textToDisplay) {
    int numItems = 0;
    data.lineWeight = 1.5;
    for(int i = 0; i < data.lines.length; ++i) {
      ConnectorLine connectorLine = data.lines[i];
      float lineSlope = connectorLine.startPoint.findSlope(connectorLine.endPoint);
      float intercept = connectorLine.startPoint.y - lineSlope * connectorLine.startPoint.x;
      
      float estimatedMouseY = mouseX * lineSlope + intercept;
      if(lineSlope == 0) {
        if(mouseX > connectorLine.startPoint.x && mouseX < connectorLine.endPoint.x
           && mouseY - 7 < connectorLine.startPoint.y && mouseY + 7 > connectorLine.startPoint.y) {
          data.lineWeight = 3.0;
          textToDisplay += data.toString() + "\n";
          numItems++;
        }
      }
      else if(mouseX > min(connectorLine.startPoint.x, connectorLine.endPoint.x) && mouseX < max(connectorLine.startPoint.x, connectorLine.endPoint.x)
              && estimatedMouseY > mouseY - 7 && estimatedMouseY < mouseY + 7) {
        data.lineWeight = 3.0;
        textToDisplay += data.toString() + "\n";
        numItems++;
      }
    }
    
    return numItems;
  }
  
  void toolTip(String textToDisplay, int numItems) {
    if(!(textToDisplay == "")){
      textAlign(BASELINE);
      float textHeight = (textDescent() + textAscent()) * numItems * (dimensions.length + 2);
      Point textStartPoint = new Point(mouseX + 25, mouseY + 25);
      Point textEndPoint = new Point(textStartPoint.x + textWidth(textToDisplay), textStartPoint.y + textHeight);
      colorMode(RGB);
      stroke(0, 0, 0);
      fill(245, 245, 245);
      if(textEndPoint.y > height && textEndPoint.x > width){
        rect(widthBorder + graphWidth, heightBorder + graphHeight, widthBorder + graphWidth - textWidth(textToDisplay), heightBorder + graphHeight - textHeight);
        fill(0);
        text(textToDisplay, widthBorder + graphWidth - textWidth(textToDisplay) + 2, heightBorder + graphHeight - textHeight + 13);
      }
      else if(textEndPoint.y > height) {
        rect(textStartPoint.x, heightBorder + graphHeight, textEndPoint.x, heightBorder + graphHeight - textHeight);
        fill(0);
        text(textToDisplay, textStartPoint.x + 2, heightBorder + graphHeight - textHeight + 13);
      }
      else if(textEndPoint.x > width) {
        rect(widthBorder + graphWidth, textStartPoint.y, widthBorder + graphWidth - textWidth(textToDisplay), textEndPoint.y);
        fill(0);
        text(textToDisplay, widthBorder + graphWidth - (textWidth(textToDisplay)) + 2, textStartPoint.y + 13);
      }
      else {
        rect(textStartPoint.x, textStartPoint.y, textEndPoint.x, textEndPoint.y);
        fill(0);
        text(textToDisplay, textStartPoint.x + 2, textStartPoint.y + 13);
      }

    }
  }
}

class Point {
  float x;
  float y;
  
  Point(float x, float y) {
    this.x = x;
    this.y = y;
  }
  
  float findSlope(Point nextPoint){
    return (this.y - nextPoint.y) / (this.x - nextPoint.x);
  }
  
  String toString() {
    return "(" + this.x + ", " + this.y + ")";
  }
}

class SelectionBox {
  Dimension[] dimensions;
  DataLine[] data;
  
  SelectionBox(Dimension[] dimensions, DataLine[] data) {
    this.dimensions = dimensions;
    this.data = data;
  }
  
  void highlightLines(Point initialPoint, Point finalPoint) {
    for(int i = 0; i < data.length; ++i) {
      data[i].saturation = 0;
      data[i].opacity = 63;
      for(int j = 0; j < data[i].lines.length; ++j) {
        ConnectorLine connectorLine = data[i].lines[j];
        float slope = connectorLine.startPoint.findSlope(connectorLine.endPoint);
        float intercept = connectorLine.startPoint.y - connectorLine.startPoint.x * slope;
        
        float topBoxLineIntersect = (min(initialPoint.y, finalPoint.y) - intercept) / slope;
        float bottomBoxLineIntersect = (max(initialPoint.y, finalPoint.y) - intercept) / slope;
        float leftBoxLineIntersect = min(initialPoint.x, finalPoint.x) * slope + intercept;
        float rightBoxLineIntersect = max(initialPoint.x, finalPoint.x) * slope + intercept;
        
        int lineIntersectCount = 0;
        if(topBoxLineIntersect > min(initialPoint.x, finalPoint.x)
           && topBoxLineIntersect < max(initialPoint.x, finalPoint.x)) {
          lineIntersectCount++;
        }
        if(bottomBoxLineIntersect > min(initialPoint.x, finalPoint.x)
           && bottomBoxLineIntersect < max(initialPoint.x, finalPoint.x)) {
           lineIntersectCount++;
        }
        if(leftBoxLineIntersect > min(initialPoint.y, finalPoint.y)
           && leftBoxLineIntersect < max(initialPoint.y, finalPoint.y)) {
          lineIntersectCount++;
        }
        if(rightBoxLineIntersect > min(initialPoint.y, finalPoint.y)
           && rightBoxLineIntersect < max(initialPoint.y, finalPoint.y)) {
          lineIntersectCount++;
        }

        if(lineIntersectCount % 2 == 0 && lineIntersectCount != 0){
          data[i].saturation = 240;
          data[i].opacity = 255;
        }

      }
    }
  }
  
  void resetLineHighlights() {
    for(int i = 0; i < data.length; ++i) {
      data[i].saturation = 240;
      data[i].opacity = 255;
    }
  }
}