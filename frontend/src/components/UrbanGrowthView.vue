<template>
    <NavBar />
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p class="loading-text">{{ loadingMessage }}</p>
    </div>
    <div class="filter-container">
        <!-- <div class="tab-header">
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
         -->
            <div class="tab-content">
                <!-- Explore Ithaca Tab -->
                <RadioGroup v-model="activeFilter">
                    <RadioGroupLabel class="filter-title">Bureaucratic Mode</RadioGroupLabel>
                    <div class="radio-options">
                        <RadioGroupOption 
                            as="template" 
                            v-for="option in filterOptions" 
                            :key="option.value" 
                            :value="option.value" 
                            v-slot="{ checked }"
                        >
                            <button 
                            class="filter-button"
                            :class="{ active: checked }"
                            @click="option.action"
                            >
                            <span class="filter-label">{{ option.label }}</span>
                            <span v-if="checked" class="checkmark">
                                <svg class="icon" viewBox="0 0 24 24" fill="none">
                                <circle cx="12" cy="12" r="12" fill="white" fill-opacity="0.2"/>
                                <path d="M7 13l3 3 7-7" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </span>
                            </button>
                        </RadioGroupOption>
                    </div>
                </RadioGroup>
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
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from "@headlessui/vue";

const map = ref(null); // Holds map
const activeFilter = ref(""); // Default tab
const layerGroup = ref(null); // Holds Layers 
const isLoading = ref(true); // Add loading state
const loadingMessage = ref("Loading zoning data...");


/**
 * Define Colors for Zoning Map
 */
const zoningColorMap = {
    Residential: '#1f77b4',
    Business: '#ff7f0e',
    Industrial: '#2ca02c',
    Government: '#9467bd',
    'Mixed Use': '#d62728',
    Southwest: '#8c564b',
    'Not Zoned': '#7f7f7f'
};

/**
 * Lifecycle Hook for calling Zoning Data
 */
onMounted(async () => {
    
    map.value = L.map('map').setView([42.443, -76.501], 13);

    L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        attribution: '&copy; OpenStreetMap contributors',
        subdomains:['mt0','mt1','mt2','mt3']
    }).addTo(map.value);
    plotVacantLots()
    activeFilter.value = "vacant"
});


/**
 * Define Options For Filter
 */
 const filterOptions = [
    { value: "vacant", label: "Plot Vacant Lots", action: plotVacantLots },
    { value: "all", label: "Plot All Parcels", action: plotLots },
    { value: "flood", label: "Flood Zones", action: plotFloodMap },
];


/**
 * Plots Vacant Lots
 */
async function plotVacantLots() {
    if(activeFilter.value == "vacant") {
        activeFilter.value = ""
        layerGroup.value.clearLayers();
        return;
    }
    isLoading.value = true;
    if (layerGroup.value) {
        layerGroup.value.clearLayers();
    } else {
        layerGroup.value = L.layerGroup().addTo(map.value);
    }
    
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
            })

            polygon.bindPopup(
                `<strong>ID:</strong> ${feature.OBJECTID}<br>
                <strong>Zoning:</strong> ${feature.ZoningCategory}<br>
                <strong>Value Per Acre:</strong> $${Math.round(feature.ValuePerAcre).toLocaleString()}`
            );
            layerGroup.value.addLayer(polygon);
        }
    });

    isLoading.value = false;
}

/**
 * Plots All Ithaca Lots
 */
async function plotLots() {
    if(activeFilter.value == "all") {
        activeFilter.value = ""
        layerGroup.value.clearLayers();
        return;
    }
    isLoading.value = true;
    if (layerGroup.value) {
        layerGroup.value.clearLayers();
    } else {
        layerGroup.value = L.layerGroup().addTo(map.value);
    }

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
            })
            
            polygon.bindPopup(
                `<strong>ID:</strong> ${feature.OBJECTID}<br>
                <strong>Zoning:</strong> ${feature.ZoningCategory}<br>
                <strong>Value Per Acre:</strong> $${Math.round(feature.ValuePerAcre).toLocaleString()}`
            );
            layerGroup.value.addLayer(polygon);
        }
    });

    isLoading.value = false;
}

/**
 * Loading Flood Map
 */
async function plotFloodMap() {
    if(activeFilter.value == "flood") {
        activeFilter.value = ""
        layerGroup.value?.clearLayers();
        return;
    }
    isLoading.value = true;
    try {
        const response = await fetch("/maps/Flood_Zones.geojson");
        const geojson = await response.json();

        const floodLayer = L.geoJSON(geojson, {
        style: {
            color: '#0077b6',
            fillColor: '#00b4d8',
            fillOpacity: 0.3,
            weight: 1
        },
        onEachFeature: (feature, layer) => {
            layer.bindPopup(`Flood Zone: ${feature.properties?.ZONE || "Unknown"}`);
        }
        });
        layerGroup.value?.addLayer(floodLayer)
        floodLayer.addTo(map.value);
    } catch (error) {
        console.error("Failed to load flood zones:", error);
    }
    isLoading.value = false;
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
  