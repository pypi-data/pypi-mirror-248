// Initialize an empty list to store clicked data points
var clickedDataPoints = [];

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onDataFromPython(event) {
  var myPlot = document.getElementById("plot");

  const data = event.detail;

  spec = JSON.parse(data.args.spec);
  console.log(spec);

  Plotly.newPlot(myPlot, spec);

  // on event, append clicked data points with x, y, and name (curve)
  myPlot.on("plotly_click", (eventData) => {
    const clickedPoints = eventData.points.map((p) => {
      return {
        x: p.x,
        y: p.y,
        name: p.data.name // Include the name of the trace (curve)
      };
    });

    // Append the clicked data points to the list
    clickedDataPoints.push(...clickedPoints);

    // Send the list of all clicked data points to Python
    Streamlit.setComponentValue(clickedDataPoints);
  });

  // Render iframe with the plot height
  Streamlit.setFrameHeight(document.documentElement.clientHeight);
}

// Render the component whenever Python sends a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onDataFromPython);

// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady();

