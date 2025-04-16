<template>
    <div ref="mapContainer" style="width: 100%; height: 100%;"></div>
  </template>
  
<script setup>
import { ref, onMounted } from "vue";
import { csvParse } from "d3";
import Plotly from "plotly.js-dist";

const mapContainer = ref(null);

async function loadCSV(file) {
  const response = await fetch(file);
  const text = await response.text();

  const parsed = csvParse(text);
  return parsed.map(row => ({
    iso_alpha: row["iso_alpha"]?.trim(),
    Num_People: parseInt(row["Num_People"]) || 0,
    "Place of Birth": row["Place of Birth"]?.trim() || "Unknown",
    Year: row["Year"]
  }));
}


onMounted(async () => {
    const combinedData = await loadCSV("/graphs/POBCensusData.csv");


    const years = [1920, 1930, 1940];

    const frames = years.map(year => {
        const dataForYear = combinedData.filter(d => String(d.Year) === String(year));
        return {
            name: String(year),
            data: [{
                type: "scattergeo",
                locations: dataForYear.map(d => d.iso_alpha),
                locationmode: "ISO-3",
                text: dataForYear.map(d => d["Place of Birth"]),
                marker: {
                size: dataForYear.map(d => d.Num_People),
                sizemode: "area",
                sizeref: 2.0 * Math.max(...combinedData.map(d => d.Num_People)) / (50 ** 2),
                sizemin: 4,
                color: "rgba(200,0,0,0.6)",
                line: { color: "black", width: 0.5 }
                }
            }]
        };
    });

    const layout = {
        title: "Birthplaces of Immigrants Over Time",
        geo: {
            projection: { type: "natural earth" },
            showland: true,
            landcolor: "white",
            showocean: true,
            oceancolor: "lightsteelblue",
            showcoastlines: true,
            coastlinecolor: "black"
        },
        updatemenus: [{
            type: "buttons",
            showactive: false,
            buttons: [{
                label: "Play",
                method: "animate",
                args: [null, {
                frame: { duration: 1000, redraw: true },
                transition: { duration: 500 },
                fromcurrent: true
                }]
            }]
        }],
        sliders: [{
            active: 0,
            steps: frames.map(frame => ({
                label: frame.name,
                method: "animate",
                args: [[frame.name], {
                mode: "immediate",
                transition: { duration: 300 },
                frame: { duration: 800, redraw: true }
                }]
            }))
        }]
    };

    Plotly.newPlot(mapContainer.value, frames[0].data, layout).then(() => {
    Plotly.addFrames(mapContainer.value, frames);
    });
});
</script>
