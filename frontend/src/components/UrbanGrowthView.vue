<template>
    <NavBar />
    <div class="filter-container">
        <div class="tab-header">
            <button
            class="tab-button"
            :class="{ active: activeTab === 'Vacant Lots' }"
            @click="changeTab('Vacant Lots')"
            >
            Vacant Lots
            </button>
            <button
            class="tab-button"
            :class="{ active: activeTab === 'All Lots' }"
            @click="changeTab('All Lots')"
            >
            All Lots
            </button>
        </div>
    </div>
    <div id="map" style="height: 100vh; width: 100%">
        <div class="legend">
            <h4>Zoning Legend</h4>
            <ul>
            <li><span style="background: #1f77b4"></span> Residential</li>
            <li><span style="background: #ff7f0e"></span> Business</li>
            <li><span style="background: #2ca02c"></span> Industrial</li>
            <li><span style="background: #9467bd"></span> Government</li>
            <li><span style="background: #d62728"></span> Mixed Use</li>
            <li><span style="background: #8c564b"></span> Southwest</li>
            <li><span style="background: #7f7f7f"></span> Not Zoned</li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import L from 'leaflet';
import { fetchVacantLots, fetchLots } from '@/services/fetch';
import NavBar from "@/components/NavBar.vue";

const map = ref(null);
const activeTab = ref("Vacant Lots"); // Default tab
const layerGroup = ref(null);

const zoningColorMap = {
    Residential: '#1f77b4',
    Business: '#ff7f0e',
    Industrial: '#2ca02c',
    Government: '#9467bd',
    'Mixed Use': '#d62728',
    Southwest: '#8c564b',
    'Not Zoned': '#7f7f7f'
};

onMounted(async () => {
    map.value = L.map('map').setView([42.443, -76.501], 13);

    L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        attribution: '&copy; OpenStreetMap contributors',
        subdomains:['mt0','mt1','mt2','mt3']
    }).addTo(map.value);
    plotVacantLots()
    
});

function changeTab(tab) {
    layerGroup.value?.clearLayers();

    if(tab == "Vacant Lots") {
        activeTab.value = "Vacant Lots"
        plotVacantLots();
        return;
    }
    activeTab.value = "All Lots"
    plotLots()
    layerGroup.value = L.layerGroup().addTo(map.value);
}

async function plotVacantLots() {
    const data = await fetchVacantLots();
    data.forEach(feature => {
        if (feature.geometry && feature.geometry.coordinates) {
        const coords = feature.geometry.coordinates[0].map((pt) => [pt[1], pt[0]]);
        const zoning = feature.ZoningCategory || 'Not Zoned';
        const fillColor = zoningColorMap[zoning] || '#7f7f7f';

        const polygon = L.polygon(coords, {
            color: 'black',
            weight: 1,
            fillColor: fillColor,
            fillOpacity: 0.5
        }).addTo(map.value);
        if (layerGroup.value) {
            layerGroup.value.addLayer(polygon);
        }


        polygon.bindPopup(
            `<strong>ID:</strong> ${feature.OBJECTID}<br>
            <strong>Zoning:</strong> ${feature.ZoningCategory}<br>
            <strong>Value Per Acre:</strong> $${Math.round(feature.ValuePerAcre).toLocaleString()}`
        );
        }
    });
}

async function plotLots() {
    const data = await fetchLots();
    data.forEach(feature => {
        if (feature.geometry && feature.geometry.coordinates) {
        const coords = feature.geometry.coordinates[0].map((pt) => [pt[1], pt[0]]);
        const zoning = feature.ZoningCategory || 'Not Zoned';
        const fillColor = zoningColorMap[zoning] || '#7f7f7f';

        const polygon = L.polygon(coords, {
            color: 'black',
            weight: 1,
            fillColor: fillColor,
            fillOpacity: 0.5
        }).addTo(map.value);
        layerGroup.value?.addLayer(polygon)

        polygon.bindPopup(
            `<strong>ID:</strong> ${feature.OBJECTID}<br>
            <strong>Zoning:</strong> ${feature.ZoningCategory}<br>
            <strong>Value Per Acre:</strong> $${Math.round(feature.ValuePerAcre).toLocaleString()}`
        );
        }
    });
}

</script>

<style scoped>
#map {
height: 100vh;
width: 100%;
}

/* 🔵 LEGEND STYLING */
.legend {
  position: absolute;
  bottom: 30px;
  left: 30px;
  padding: 10px 15px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  color: #444;
  z-index: 1000;
  line-height: 1.5;
}

.legend h4 {
  margin: 0 0 8px;
  font-size: 0.95rem;
  color: #333;
}

.legend ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.legend ul li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  color: #444;
  margin-bottom: 4px;
}

.legend ul li span {
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 1px solid #ddd;
}

/* FILTER BUTTON */
.filter-container {
  position: absolute;
  top: 100px;
  left: 20px;
  z-index: 1000;
  width: 300px;
  background: rgba(21, 19, 102, 0.2); 
  backdrop-filter: blur(8px); 
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(12px);
  border-radius: 14px;
  padding: 20px;
  width: 320px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  text-align: center;
}

.filter-title {
  font-size: 1.6rem;
  color: #333;
  font-weight: bold;
  margin-bottom: 12px;
}


/* Tab Navigation */
.tab-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.tab-button {
  flex: 1;
  padding: 10px;
  font-weight: bold;
  border: none;
  background: rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  color: black;
  border-radius: 8px 8px 0 0;
}

.tab-button.active {
  background: #507cb6;
  color: white;
}

/* Tab Content */
.tab-content {
  background: white;
  color: black;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

</style>
  