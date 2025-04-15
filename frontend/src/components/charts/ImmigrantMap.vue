<template>
    <div ref="mapContainer" style="width: 100%; height: 100%;"></div>
  </template>
  
<script setup>
import { ref, onMounted } from "vue";
import Plotly from "plotly.js-dist";

const mapContainer = ref(null);

async function loadCSV(file, year) {
const response = await fetch(file);
const text = await response.text();
const rows = text.trim().split("\n").slice(1); 

return rows
    .map(row => row.trim())
    .filter(row => row.length > 0)
    .map(row => {
    const parts = row.split(",");
    if (parts.length < 3) return null; 

    const [iso_alpha, Num_People, PlaceOfBirth] = parts;
    return {
        iso_alpha: iso_alpha?.trim(),
        Num_People: parseInt(Num_People?.trim()) || 0,
        "Place of Birth": PlaceOfBirth?.trim() || "Unknown",
        Year: year
    };
    })
    .filter(row => row !== null);
}


onMounted(async () => {
const [data1920, data1930, data1940] = await Promise.all([
    loadCSV("/graphs/1920_Census.csv", 1920),
    loadCSV("/graphs/1930_Census.csv", 1930),
    loadCSV("/graphs/1940_Census.csv", 1940)
]);

const combinedData = [...data1920, ...data1930, ...data1940];

const years = [1920, 1930, 1940];

const frames = years.map(year => {
    const dataForYear = combinedData.filter(d => d.Year === year);
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
        color: dataForYear.map(d => d["Place of Birth"]),
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
