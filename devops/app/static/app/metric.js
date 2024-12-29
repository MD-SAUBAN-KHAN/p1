const express = require('express');
const { MeterProvider } = require('@opentelemetry/sdk-metrics-base');
const { PrometheusExporter } = require('@opentelemetry/exporter-prometheus');

// Initialize Prometheus Exporter
const exporter = new PrometheusExporter(
  { startServer: true, port: 9090 }, // Ensure correct port is configured
  () => {
    console.log('Prometheus scrape endpoint: http://localhost:9464/metrics');
  }
);

// Set up MeterProvider and Metrics
const meterProvider = new MeterProvider();
meterProvider.addMetricReader(exporter);
const meter = meterProvider.getMeter('static-webpage');

// Create a Counter Metric
const pageVisitCounter = meter.createCounter('page_visits_total', {
  description: 'Total number of page visits',
});

// Initialize Express.js
const app = express();

// Serve Static Files
app.use(express.static('public')); // Assumes static files are in the 'public' directory
app.get('/metrics', (req, res) => {
  exporter.export((err, result) => {
    if (err) {
      res.status(500).send('Error exporting metrics');
      return;
    }
    res.set('Content-Type', result['content-type']);
    res.send(result.body);
  });
});

// Handle Page Visits
app.get('/', (req, res) => {
  pageVisitCounter.add(1); // Increment metric
  res.sendFile(__dirname + '/public/devops.html'); // Serve your HTML file
});

//Add additional endpoints to track other metrics if needed
//app.get('/about', (req, res) => {
 // pageVisitCounter.add(1);
 // res.send('About page'); // Example additional endpoint
//});

// Start the Web Server
const PORT = 8000;
app.listen(PORT, () => {
  console.log(`Static webpage running at http://localhost:${PORT}`);
});

