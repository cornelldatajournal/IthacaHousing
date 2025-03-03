<template>
  <NavBar />
  <div class="overflow-auto box-border m-0 p-0">
   
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
import { ref, onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { fetchListings } from "@/services/fetch";
import NavBar from "@/components/NavBar.vue";
import RentalSidebar from '@/components/RentalSidebar.vue';

const map = ref(null);
const isSidebarVisible = ref(false)
const selectedListing = ref(null);

/**
 * Gets the color of the dot based on price
 * @param diff -  Y - Y(hat), difference between actual and predicted
 */
function getColor(rent, predicted) {
    const percent_change = (predicted-rent)/rent
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

onMounted(async () => {
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

  const listings = await fetchListings();

  listings.forEach((listing) => {
    const color = getColor(listing.rentamount, listing.predictedrent);

    const marker = L.circleMarker([listing.latitude, listing.longitude], {
      color,
      fillColor: color,
      fillOpacity: 0.75,
      radius: 8,
    }).addTo(map.value);

    marker.on("click", () => {
        selectedListing.value = listing;
        isSidebarVisible.value = true
    });
  });
});

/**
 * Closes Rental Sidebar
 * Emitted Function to Rental Sidebar
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
/* Map Styles */
/* 🗺️ MAP */
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
  font-family: "Inter", sans-serif;
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
