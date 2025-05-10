<template>
    <div ref="plotContainer" style="width: 100%; height: 600px;"></div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import Plotly from "plotly.js-dist";
  import { csvParse } from "d3";
  
  // ✅ Replace this with your actual token
  Plotly.setPlotConfig({
    mapboxAccessToken: "pk.eyJ1IjoiYXNtMzY2IiwiYSI6ImNtN2FvNnRkdDA2M3gycW9zamlqdXM3ZzkifQ.3969zxq_WRVsYBzsWaLwmA"
  });
  
  const plotContainer = ref(null);
  
  const pobColors = {
    "China": "#FFB3D9",
    "Italy": "#F07566",
    "Germany": "#FFAF7C",
    "Ireland": "#BCBFFE",
    "Russia": "#FED478",
    "Poland": "#FE7FA4",
    "Canada": "#B778FC",
    "Mexico": "#7F82FC",
    "France": "#C2EE98"
  };
  
  function hexToRgba(hex, alpha = 0.7) {
    const bigint = parseInt(hex.replace("#", ""), 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }
  
  async function loadCSV(file, year) {
    const response = await fetch(file);
    const text = await response.text();
  
    const data = csvParse(text);
    return data
      .map(row => {
        const PlaceOfBirth = row["Place of Birth"]?.trim();
        if (!pobColors[PlaceOfBirth]) return null;
  
        const lat = parseFloat(row["Latitude"]);
        const lon = parseFloat(row["Longitude"]);
        if (isNaN(lat) || isNaN(lon)) return null;
  
        return {
          PlaceOfBirth,
          Latitude: lat,
          Longitude: lon,
          Year: year
        };
      })
      .filter(Boolean);
  }
  
  onMounted(async () => {
    const [d1920, d1930, d1940] = await Promise.all([
      loadCSV("/graphs/1920_Census.csv", 1920),
      loadCSV("/graphs/1930_Census.csv", 1930),
      loadCSV("/graphs/1940_Census.csv", 1940)
    ]);
  
    const combinedData = [...d1920, ...d1930, ...d1940];
    const years = [1920, 1930, 1940];
  
    const frames = years.map(year => {
      const dataForYear = combinedData.filter(d => d.Year === year);
      const cleaned = dataForYear.filter(d => !isNaN(d.Latitude) && !isNaN(d.Longitude));
  
      return {
        name: String(year),
        data: [{
          type: "scattermapbox",
          lat: cleaned.map(d => d.Latitude),
          lon: cleaned.map(d => d.Longitude),
          text: cleaned.map(d => `${d.PlaceOfBirth}`),
          marker: {
            size: 6,
            color: cleaned.map(d => hexToRgba(pobColors[d.PlaceOfBirth] || "#888", 0.6)),
            opacity: 0.8
          },
          hoverinfo: "text"
        }]
      };
    });
  
    const layout = {
      title: "Place of Birth of Immigrants by Year",
      mapbox: {
        center: { lat: 42.44, lon: -76.5 },
        zoom: 13,
        style: "carto-positron" 
      },
      sliders: [{
        active: 0,
        steps: frames.map(f => ({
          label: f.name,
          method: "animate",
          args: [[f.name], {
            mode: "immediate",
            transition: { duration: 300 },
            frame: { duration: 800, redraw: true }
          }]
        }))
      }],
      updatemenus: [{
        type: "buttons",
        showactive: false,
        buttons: [{
          label: "Play",
          method: "animate",
          args: [null, {
            frame: { duration: 1000, redraw: false },
            transition: { duration: 500 },
            fromcurrent: true
          }]
        }]
      }],
      margin: { t: 50, b: 0 },
      hovermode: "closest"
    };
  
    Plotly.newPlot(plotContainer.value, frames[0].data, layout, {
        responsive: true
        }).then(() => {
        Plotly.addFrames(plotContainer.value, frames); 
    });

  });
  </script>
  