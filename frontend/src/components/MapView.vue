<template>
  <NavBar />
  <div class="overflow-auto box-border m-0 p-0">
    <div class="filter-container">
      <RadioGroup v-model="activeFilter">
        <RadioGroupLabel class="filter-title">Explore Ithaca</RadioGroupLabel>
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

    <!-- Map Container -->
    <div class="relative flex z-[0] border-b-2 border-black overflow-hidden">
      <RentalSidebar class="rental-sidebar" @close="closePopup" @zoom="zoomToListing" :listing="selectedListing" v-if="isSidebarVisible" />

      <div id="map"></div>

       <!-- Loading Spinner -->
       <div v-if="isLoading" class="loading-overlay">
        <div class="spinner"></div>
        <p>Loading data...</p>
      </div>

      <!-- Legend -->
      <div class="legend">
        <h4>Price Difference Legend</h4>
        <ul>
          <li><span style="background: #006400;"></span> Very Underpriced</li>
          <li><span style="background: #008000;"></span> Underpriced</li>
          <li><span style="background: #32CD32;"></span> Slightly Underpriced</li>
          <li><span style="background: #90EE90;"></span> Barely Underpriced</li>
          <li><span style="background: #FFA07A;"></span> Barely Overpriced</li>
          <li><span style="background: #FF6347;"></span> Slightly Overpriced</li>
          <li><span style="background: #FF0000;"></span> Overpriced</li>
          <li><span style="background: #8B0000;"></span> Very Overpriced</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { fetchListings, fetchTopTenListings, fetchBottomTenListings, fetchClusters } from "@/services/fetch";
import NavBar from "@/components/NavBar.vue";
import RentalSidebar from "@/components/RentalSidebar.vue";
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from "@headlessui/vue";

const map = ref(null); // Holds the ref for the map
const isSidebarVisible = ref(false); // Toggle state for whether the Rental Sidebar is visible or not
const selectedListing = ref(null); // Holds the prop state for the selected listing to pass to RentalSidebar
const markers = ref([]); // Store all markers
const allListings = ref([]); // Store all listings
const topTenListings = ref([]); // Store top 10 listings
const bottomTenListings = ref([]); // Store bottom 10 listings
const clusteredListings = ref([]); // Store Clustered Listings
let activeFilter = ref(null); // Tracks which filter is selected
const isLoading = ref(true); // Add loading state

/**
 * Gets the color of the dot based on price
 * @param rent - Actual rent
 * @param predicted - Predicted rent
 */
function getColor(rent, predicted) {
    const percent_change = (predicted - rent) / rent;
    if (percent_change >= 0.15) return "#006400"; // Dark Green (Very Underpriced)
    if (percent_change >= 0.10) return "#008000"; // Green (Underpriced)
    if (percent_change >= 0.05) return "#32CD32";  // Lime Green (Slightly Underpriced)
    if (percent_change > 0) return "#90EE90";     // Light Green (Barely Underpriced)

    if (percent_change <= -0.15) return "#8B0000"; // Dark Red (Very Overpriced)
    if (percent_change <= -0.10) return "#FF0000"; // Red (Overpriced)
    if (percent_change <= -0.05) return "#FF6347";  // Tomato (Slightly Overpriced)
    if (percent_change < 0) return "#FFA07A";    // Light Salmon (Barely Overpriced)

    return "gray"; // Neutral (Fairly Priced)
}

/**
 * Add markers to the map
 */
function addMarkers(listings) {
    markers.value.forEach(marker => map.value.removeLayer(marker)); 
    markers.value = []; 

    listings.forEach(listing => {
        const color = getColor(listing.rentamount, listing.predictedrent);

        const marker = L.circleMarker([listing.latitude, listing.longitude], {
            color,
            fillColor: color,
            fillOpacity: 0.75,
            radius: 8,
        }).addTo(map.value);

        marker.on("click", () => {
            selectedListing.value = listing;
            isSidebarVisible.value = true;
        });

        markers.value.push(marker); 
    });
}

onMounted(async () => {
  try {
    map.value = L.map("map", {
          center: [42.455, -76.48],
          zoom: 14,
          maxZoom: 20,
      });

      L.tileLayer('https://tile.jawg.io/f67529a2-5ea7-4b7a-81a7-c5147a45b5f0/{z}/{x}/{y}{r}.png?access-token=pSUjHs1tEnhDqSIJpBV3miDFcODgE5a8MEyjIAmHPPMCZicbKrH3Z1O0mbhtTQTR', {
          attribution: '<a href="https://jawg.io" target="_blank">&copy; Jawg Maps</a> &copy; OpenStreetMap contributors',
          minZoom: 0,
          maxZoom: 22,
          accessToken: 'pSUjHs1tEnhDqSIJpBV3miDFcODgE5a8MEyjIAmHPPMCZicbKrH3Z1O0mbhtTQTR'
      }).addTo(map.value);

      allListings.value = await fetchListings();
      topTenListings.value = await fetchTopTenListings();
      bottomTenListings.value = await fetchBottomTenListings();
      clusteredListings.value = await fetchClusters();

      addMarkers(allListings.value); 
  }  catch (error) {
      console.error("Error loading data:", error);
    } finally {
      isLoading.value = false;
    }
});

/**
 * Toggle between all listings and top 10 listings
 */
 const showTopTenListings = () => {
    if (activeFilter.value === "topTen") {
        activeFilter.value = "";
        addMarkers(allListings.value);
    } else {
        switchFilter("topTen", topTenListings.value);
    }
};

/**
 * Toggle between all listings and bottom 10 listings
 */
 const showBottomTenListings = () => {
    if (activeFilter.value === "bottomTen") {
        activeFilter.value = "";
        addMarkers(allListings.value);
    } else {
        switchFilter("bottomTen", bottomTenListings.value);
    }
};

/**
 * Toggle between all listings and clusters
 */
 const showClusters = () => {
    if (activeFilter.value === "cluster") {
        activeFilter.value = "";
        addMarkers(allListings.value);
    } else {
        switchFilter("cluster");
        plotClustersOnMap();
    }
};

/**
 * Define Options For Filter
 */
const filterOptions = [
    { value: "topTen", label: "Best Bang For Your Buck", action: showTopTenListings },
    { value: "bottomTen", label: "Avoid These Listings", action: showBottomTenListings },
    { value: "cluster", label: "Natural Neighborhoods", action: showClusters },
];


/**
 * Handles switching between different filters without resetting to all markers
 */
 const switchFilter = (newFilter, newListings = null) => {
    markers.value.forEach(marker => map.value.removeLayer(marker)); 

    activeFilter.value = newFilter;

    if (newListings) {
        addMarkers(newListings);
    } else if (newFilter === "cluster") {
        plotClustersOnMap();
    }
};



/**
 * Plot Clusters on Leaflet Map
 */
 const plotClustersOnMap = () => {
  if (!map.value) return;
  markers.value.forEach(marker => map.value.removeLayer(marker)); 

  const clusterColors = [
    "#FF5733", // Vibrant Red-Orange
    "#33FF57", // Bright Green
    "#3357FF", // Strong Blue
    "#FF33A1", // Hot Pink
    "#F39C12", // Warm Orange-Yellow
    "#8E44AD", // Rich Purple
    "#1ABC9C", // Teal/Cyan
    "#E74C3C"  // Deep Red
  ];

  clusteredListings.value.forEach((listing) => {
    const clusterIndex = listing.hierarchal_cluster % clusterColors.length;
    const marker = L.circleMarker([listing.latitude, listing.longitude], {
      color: clusterColors[clusterIndex],
      fillColor: clusterColors[clusterIndex],
      fillOpacity: 0.75,
      radius: 8,
    }).addTo(map.value);
    markers.value.push(marker); 
  });
};

/**
 * Closes Rental Sidebar
 */
const closePopup = () => {
    isSidebarVisible.value = false;
};

/**
 * Zooms to Location
 * Emitted Function to Rental Sidebar
 * @param lat - Latitude
 * @param lng - Longitude
*/
const zoomToListing = (coords) => {
    map.value.setView([coords.lat, coords.lng], 16);
};
</script>

<style>
/* MAP */
#map {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
}

.rental-sidebar {
  position: absolute;
  top: 0%; 
  right: 0;
  width: 350px;
  height: calc(100vh);
  overflow-y: auto;
  background: white;
  box-shadow: -3px 0 15px rgba(0, 0, 0, 0.2);
  z-index: 999; 
  border-left: 1px solid #ddd;
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
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  text-align: center;
}

/* Title */
.filter-title {
  font-size: 1.5rem;
  color: black;
}

/* Radio Options */
.radio-options {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: 5px;
  padding-bottom: 5px;
}

/* Button Styling */
.filter-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  color: black;
  padding: 12px 15px;
  border-radius: 8px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

/* Hover Effect */
.filter-button:hover {
  background: #e0e0e0;
  transform: scale(1.02);
}

/* Active Selection */
.filter-button.active {
  background: #507cb6;
  color: white;
  border: 2px solid #0f5dc7;
  position: relative;
}

/* Active Hover */
.filter-button.active:hover {
  transform: scale(1.05);
}

/* Label inside button */
.filter-label {
  font-size: 1rem;
}

/* Checkmark Icon */
.checkmark {
  display: flex;
  align-items: center;
}

.icon {
  width: 20px;
  height: 20px;
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


.leaflet-popup-close-button {
  display: none;
}
</style>
