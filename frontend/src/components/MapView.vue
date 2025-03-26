<template>
  <NavBar />
  <div class="overflow-auto box-border m-0 p-0">
    <!-- Loading Spinner -->
    <div v-if="isLoading" class="loading-overlay">
        <div class="spinner"></div>
        <p>Loading data...</p>
      </div>
      <div class="filter-container">
        <!-- Tab Navigation -->
        <div class="tab-header">
          <button
            class="tab-button"
            :class="{ active: activeTab === 'Explore Ithaca' }"
            @click="activeTab = 'Explore Ithaca'"
          >
            Explore Ithaca
          </button>
          <button
            class="tab-button"
            :class="{ active: activeTab === 'Personal Taste' }"
            @click="activeTab = 'Personal Taste'"
          >
            Personal Taste
          </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content">
          <!-- Explore Ithaca Tab -->
          <div v-if="activeTab === 'Explore Ithaca'">
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

          <!-- Personal Taste Tab -->
          <div v-if="activeTab === 'Personal Taste'">
            <h3 class="filter-title">Personal Taste</h3>
            <div class="personal-filters">
              <label for="bed-filter" class="filter-label">Beds</label>
              <select id="bed-filter" v-model="selectedBeds" @change="updateBedFilter" class="filter-select">
                <option :value="0">N/A Beds</option>
                <option v-for="n in bedOptions" :key="n" :value="n">{{ n }} Beds</option>
              </select>

              <label for="bath-filter" class="filter-label">Baths</label>
              <select id="bath-filter" v-model="selectedBaths" @change="updateBathFilter" class="filter-select">
                <option :value="0">N/A Baths</option>
                <option v-for="n in bathOptions" :key="n" :value="n">{{ n }} Baths</option>
              </select>

              <div class="icon-buttons">
                <button 
                  @click="toggleWalk" 
                  :class="['icon-button', { active: activeFilters.walk !== null }]"
                >
                  🚶‍♂️ Walk
                </button>
                <button 
                  @click="toggleTransit" 
                  :class="['icon-button', { active: activeFilters.transit !== null }]"
                >
                  🚌 TCAT
                </button>
                <button 
                  @click="togglePets" 
                  :class="['icon-button', { active: activeFilters.pets !== null }]"
                >
                  🐶 Pets
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Map Container -->
      <div class="relative flex z-[0] border-b-2 border-black overflow-hidden">
        <RentalSidebar class="rental-sidebar" @close="closePopup" @zoom="zoomToListing" :listing="selectedListing" v-if="isSidebarVisible" />

        <div id="map"></div>

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
import { ref, onMounted, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { fetchListings, fetchTopTenListings, fetchBottomTenListings, fetchClusters, fetchHeatMap, fetchBedFilter, fetchBathFilter, fetchWalkFilter, fetchTransitFilter, fetchPetsFilter } from "@/services/fetch";
import NavBar from "@/components/NavBar.vue";
import RentalSidebar from "@/components/RentalSidebar.vue";
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from "@headlessui/vue";
import "leaflet.heat";

const map = ref(null); // Holds the ref for the map
const isSidebarVisible = ref(false); // Toggle state for whether the Rental Sidebar is visible or not
const selectedListing = ref(null); // Holds the prop state for the selected listing to pass to RentalSidebar
const markers = ref([]); // Store all markers
const allListings = ref([]); // Store all listings
const topTenListings = ref([]); // Store top 10 listings
const bottomTenListings = ref([]); // Store bottom 10 listings
const clusteredListings = ref([]); // Store Clustered Listings
const heatmapData = ref(null); // Stores the Heatmap Data
const heatmapLayer = ref(null); // Stores the Heatmap Layer
const activeTab = ref("Explore Ithaca"); // Default tab
let activeFilter = ref(null); // Tracks which filter is selected

const activeFilters = ref({ beds: null, baths: null, walk: null, transit: null, pets: null }); // Holds Bath and Bed Data for Dynamic Filtering
const filteredListings = ref([]); // Keeps track of the filtered listings
const selectedBeds = ref(0); // Number of Selected Beds
const bedOptions = [1, 2, 3, 4, 5]; // Adjust based on available data
const selectedBaths = ref(0); // Number of Selected Beds
const bathOptions = [1, 1.5, 2, 2.5, 3]; // Adjust based on available data

const isLoading = ref(true); // Add loading state

/**
 * Gets the color of the dot based on price
 * @param rent - Actual rent
 * @param predicted - Predicted rent
 */
function getColor(rent, predicted) {
    const percent_change = (predicted - rent) / rent;
    if (percent_change >= 0.30) return "#006400"; // Dark Green (Very Underpriced)
    if (percent_change >= 0.20) return "#008000"; // Green (Underpriced)
    if (percent_change >= 0.10) return "#32CD32";  // Lime Green (Slightly Underpriced)
    if (percent_change > 0) return "#90EE90";     // Light Green (Barely Underpriced)

    if (percent_change <= -0.30) return "#8B0000"; // Dark Red (Very Overpriced)
    if (percent_change <= -0.20) return "#FF0000"; // Red (Overpriced)
    if (percent_change <= -0.10) return "#FF6347";  // Tomato (Slightly Overpriced)
    if (percent_change < 0) return "#FFA07A";    // Light Salmon (Barely Overpriced)

    return "gray"; // Neutral (Fairly Priced)
}

/**
 * Add markers to the map
 * Only filters markers CURRENTLY on map using .some 
 */
function addMarkers(listings, filtered) {
    markers.value.forEach(marker => map.value.removeLayer(marker)); 
    markers.value = []; 

    if (heatmapLayer.value) {
      map.value.removeLayer(heatmapLayer.value); 
    }

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
      heatmapData.value = await fetchHeatMap();

      addMarkers(allListings.value, false); 
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
        addMarkers(allListings.value, false);
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
        addMarkers(allListings.value, false);
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
        addMarkers(allListings.value, false);
    } else {
        switchFilter("cluster");
        plotClustersOnMap();
    }
};

/**
 * Heatmap
 */
const plotHeatmap = () => {
  if (activeFilter.value === "heatmap") {
      activeFilter.value = "";
      addMarkers(allListings.value, false);
  } else {
      switchFilter("heatmap");
      heatmapLayer.value = L.heatLayer(heatmapData.value, {
          radius: 40, 
          blur: 10,   
          maxZoom: 17,
          minOpacity: 0.3, 
          maxOpacity: 0.9  
      }).addTo(map.value);
  }
};

/**
 * Updates the Bed Filter based on the number of beds
 */
const updateBedFilter = async () => {
  const bedData = await fetchBedFilter(selectedBeds.value);
  activeFilters.value.beds = bedData; 
  mergeFilters();
};


/**
 * Updates the Bed Filter based on the number of beds
 */
const updateBathFilter = async () => {
  const bathFilterInput = selectedBaths.value*2
  const bathData = await fetchBathFilter(bathFilterInput);
  activeFilters.value.baths = bathData; 
  mergeFilters(bathData, true);
};

/**
 * Toggles Walkability Filter based on walking time
 * */
const toggleWalk = async () => {
  if(!activeFilters.value.walk) {
    const walkData = await fetchWalkFilter();
    activeFilters.value.walk = walkData; 
    mergeFilters(walkData, true);
  }
  else {
    activeFilters.value.walk = null; 
    mergeFilters();
  }
};

/**
 * Toggles Walkability Filter based on walking time
 * */
 const toggleTransit = async () => {
  if(!activeFilters.value.transit) {
    const transit = await fetchTransitFilter();
    activeFilters.value.transit = transit; 
    mergeFilters(transit, true);
  }
  else {
    activeFilters.value.transit = null; 
    mergeFilters();
  }
};

/**
 * Toggles Walkability Filter based on walking time
 * */
 const togglePets = async () => {
  if(!activeFilters.value.pets) {
    const petsData = await fetchPetsFilter();
    activeFilters.value.pets = petsData; 
    mergeFilters(petsData, true);
  }
  else {
    activeFilters.value.pets = null; 
    mergeFilters();
  }
};



/**
 * Merges Bed and Bath Filters
 */
function mergeFilters() {
  let mergedListings = allListings.value; 

  if (activeFilters.value.beds) {
    mergedListings = mergedListings.filter(listing =>
      activeFilters.value.beds.some(bedListing =>
        bedListing.latitude === listing.latitude && bedListing.longitude === listing.longitude
      )
    );
  }

  if (activeFilters.value.baths) {
    mergedListings = mergedListings.filter(listing =>
      activeFilters.value.baths.some(bathListing =>
        bathListing.latitude === listing.latitude && bathListing.longitude === listing.longitude
      )
    );
  }

  if (activeFilters.value.walk) {
    mergedListings = mergedListings.filter(listing =>
      activeFilters.value.walk.some(walkListing =>
        walkListing.latitude === listing.latitude && walkListing.longitude === listing.longitude
      )
    );
  }

  if (activeFilters.value.transit) {
    mergedListings = mergedListings.filter(listing =>
      activeFilters.value.transit.some(transitListing =>
        transitListing.latitude === listing.latitude && transitListing.longitude === listing.longitude
      )
    );
  }

  if (activeFilters.value.pets) {
    mergedListings = mergedListings.filter(listing =>
      activeFilters.value.pets.some(petsListing =>
        petsListing.latitude === listing.latitude && petsListing.longitude === listing.longitude
      )
    );
  }

  filteredListings.value = mergedListings;
  addMarkers(filteredListings.value);
}

/**
 * Define Options For Filter
 */
const filterOptions = [
    { value: "topTen", label: "Best Bang For Your Buck", action: showTopTenListings },
    { value: "bottomTen", label: "Avoid These Listings", action: showBottomTenListings },
    { value: "heatmap", label: "Market Hotspots", action: plotHeatmap },
    { value: "cluster", label: "Rental Neighborhoods", action: showClusters },
];


/**
 * Handles switching between different filters without resetting to all markers
 */
 const switchFilter = (newFilter, newListings = null) => {
    markers.value.forEach(marker => map.value.removeLayer(marker)); 

    if (heatmapLayer.value) {
      map.value.removeLayer(heatmapLayer.value); 
    }

    activeFilter.value = newFilter;

    if (newListings) {
        addMarkers(newListings, false);
    } else if (newFilter === "cluster") {
        plotClustersOnMap();
    }
};

/**
 * Plot Clusters on Leaflet Map with Price-Based Opacity
 */
 const plotClustersOnMap = () => {
  if (!map.value) return;
  markers.value.forEach(marker => map.value.removeLayer(marker));

  const clusterColors = [
    "#D73027", // Deep Red (Expensive Urban Core)
    "#FC8D59", // Warm Coral (Mixed Residential-Commercial)
    "#FEE08B", // Yellow (Moderate Suburban)
    "#91CF60", // Soft Green (Affordable Residential)
    "#1A9850", // Deep Green (Outskirts, Lower Prices)
    "#74ADD1", // Soft Blue (Student Areas, Mid Prices)
    "#4575B4", // Strong Blue (Distant Residential)
    "#313695"  // Deep Purple (Luxury or Isolated Areas)
];

  const prices = clusteredListings.value.map(l => l.rentamount_scaled).filter(p => p !== undefined && p !== null);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);

  const getOpacityFromPrice = (price) => {
    const opacity = 0.5 + 0.5 * ((price - minPrice) / (maxPrice - minPrice)); 
    return opacity
  };

  clusteredListings.value.forEach((listing) => {
    const clusterIndex = listing.hierarchal_cluster % clusterColors.length;
    const fillOpacity = getOpacityFromPrice(listing.rentamount_scaled);

    const marker = L.circleMarker([listing.latitude, listing.longitude], {
      color: clusterColors[clusterIndex],
      fillColor: clusterColors[clusterIndex],
      fillOpacity: fillOpacity,
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

/* Radio Buttons */
.radio-options {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

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

.filter-button:hover {
  background: #e0e0e0;
}

.filter-button.active {
  background: #507cb6;
  color: white;
  border: 2px solid #0f5dc7;
}

.checkmark .icon {
  width: 16px;
  height: 16px;
}

/* Personal Filters */
.personal-filters {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-label {
  font-size: 1rem;
  color: #444;
  font-weight: 500;
  text-align: left;
}

.filter-select {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  background: #f8f8f8;
  color: #333;
  font-size: 1rem;
  appearance: none;
  cursor: pointer;
  outline: none;
}

.icon-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
}

.icon-button {
  flex: 1;
  margin: 0 4px;
  padding: 8px;
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.2s;
}

.icon-button.active {
  background-color: #507cb6; /* Blue highlight */
  color: white;
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
