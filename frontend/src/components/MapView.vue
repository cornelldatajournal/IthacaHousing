<template>
  <NavBar />
  <div class="overflow-auto box-border m-0 p-0">
    <!-- Map Container -->
    <div class="relative flex z-[0] border-b-2 border-black overflow-hidden">
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

const map = ref(null);

/**
 * Gets the color of the dot based on price
 * @param diff -  Y - Y(hat), difference between actual and predicted
 */
function getColor(diff) {
    diff = diff * -1;
    if (diff >= 300) return "#8B0000"; // Dark Red (Very Overpriced)
    if (diff >= 150) return "#FF0000"; // Red (Overpriced)
    if (diff >= 50) return "#FF6347";  // Tomato (Slightly Overpriced)
    if (diff > 0) return "#FFA07A";    // Light Salmon (Barely Overpriced)

    if (diff <= -300) return "#006400"; // Dark Green (Very Underpriced)
    if (diff <= -150) return "#008000"; // Green (Underpriced)
    if (diff <= -50) return "#32CD32";  // Lime Green (Slightly Underpriced)
    if (diff < 0) return "#90EE90";     // Light Green (Barely Underpriced)

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
    const color = getColor(listing.differenceinfairvalue);

    const marker = L.circleMarker([listing.latitude, listing.longitude], {
      color,
      fillColor: color,
      fillOpacity: 0.75,
      radius: 8,
    }).addTo(map.value);

    marker.on("click", () => {
      const popupContent = `
       <div class="popup-container">
    <!-- Header -->
    <div class="popup-header">
        <h3 class="popup-title">${listing.listingaddress}, ${listing.listingcity}, ${listing.listingzip}</h3>
        <button class="close-btn" onclick="document.querySelector('.leaflet-popup-close-button').click()">✖</button>
    </div>

    <!-- Main Content (2-Column Layout) -->
    <div class="popup-content grid grid-cols-2 gap-4">
        <!-- Left Column (Transit & Walking Info) -->
        <div class="popup-left">
            <table class="info-table">
                <tr>
                    <td><i class="fas fa-bus text-blue-500"></i></td>
                    <td>Transit Score:</td>
                    <td>${listing.transit_score ?? "N/A"}</td>
                </tr>
                <tr>
                    <td><i class="fas fa-walking text-green-500"></i></td>
                    <td>Arts Quad:</td>
                    <td>${listing.ag_quad_time.toFixed(2) ?? "N/A"}</td>
                </tr>
                <tr>
                    <td><i class="fas fa-walking text-green-500"></i></td>
                    <td>Ag Quad:</td>
                    <td>${listing.arts_quad_time.toFixed(2) ?? "N/A"}</td>
                </tr>
                <tr>
                    <td><i class="fas fa-walking text-green-500"></i></td>
                    <td>Uris Hall:</td>
                    <td>${listing.uris_hall_time.toFixed(2) ?? "N/A"}</td>
                </tr>
                <tr>
                    <td><i class="fas fa-shield-alt text-yellow-500"></i></td>
                    <td>Safety:</td>
                    <td>${listing.overallsafetyratingpct ?? "Not Provided"}%</td>
                </tr>
            </table>
        </div>

        <!-- Right Column (Bedrooms, Pets, Amenities) -->
        <div class="popup-right">
            <table class="info-table">
                <tr>
                    <td><i class="fas fa-bed text-indigo-500"></i></td>
                    <td>Bedrooms:</td>
                    <td>${listing.bedrooms}</td>
                </tr>
                <tr>
                    <td><i class="fas fa-toilet text-purple-500"></i></td>
                    <td>Bathrooms:</td>
                    <td>${listing.bathrooms}</td>
                </tr>
                <tr>
                    <td><i class="fas fa-paw text-yellow-600"></i></td>
                    <td>Pets:</td>
                    <td>${listing.pets === "Yes" ? "Allowed" : "Not Allowed"}</td>
                </tr>
                <tr>
                    <td><i class="fas fa-home text-indigo-600"></i></td>
                    <td>Housing Type:</td>
                    <td>${listing.housingtype ?? "N/A"}</td>
                </tr>
            </table>
        </div>
    </div>

    <!-- Description -->
    <div class="popup-description">${listing.shortdescription}</div>

    <!-- Amenities Section -->
    <div class="popup-amenities">
        <strong>Amenities:</strong>
        <span class="amenities-list">${listing.amenities ? listing.amenities.replace(/[\[\]']/g, "") : "None Listed"}</span>
    </div>

    <!-- Rental Information (2-Column, 2-Row Layout) -->
    <div class="rent-section">
        <div class="rent-row">
            <div class="rent-box"><strong>Rent:</strong> $${listing.rentamount.toFixed(2)}</div>
            <div class="rent-box"><strong>Predicted Rent:</strong> <span class="text-green">$${listing.predictedrent.toFixed(2)}</span></div>
        </div>
        <div class="rent-row">
            <div class="rent-diff ${listing.differenceinfairvalue * -1 > 0 ? 'text-red' : 'text-green'}">
                <strong>Difference:</strong> $${listing.differenceinfairvalue.toFixed(2)}
            </div>
        </div>
    </div>

    <!-- Zoom Button -->
    <button class="zoom-btn" onclick="window.zoomToListing(${listing.latitude}, ${listing.longitude})">
        🔍 Zoom to Location
    </button>
</div>

      `;

      marker.bindPopup(popupContent, { className: "custom-popup" }).openPopup();
    });
  });

  window.zoomToListing = (lat, lng) => {
    map.value.setView([lat, lng], 16);
  };
});
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

/* 📦 POPUP CONTAINER */
.popup-container {
    background: #ffffff;
    padding: 20px;
    width: 640px;
    border-radius: 14px;
    box-shadow: 0 5px 14px rgba(0, 0, 0, 0.12);
    border: 1px solid #ddd;
}

/* 🔝 HEADER */
.popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 12px;
    margin-bottom: 16px;
}

.popup-title {
    font-size: 1.4rem;
    font-weight: bold;
    color: #222;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.3rem;
    cursor: pointer;
    color: #888;
    transition: color 0.2s ease-in-out;
}

.close-btn:hover {
    color: black;
}

/* 📊 MAIN GRID LAYOUT */
.popup-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-bottom: 20px;
}

/* 📌 LEFT & RIGHT SECTIONS */
.popup-left,
.popup-right {
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 1rem;
    color: #444;
}

.popup-left p,
.popup-right p {
    display: flex;
    align-items: center;
    gap: 10px;
}

/* 💰 RENT INFO BOX */
.rent-section {
    display: flex;
    flex-direction: column;
    align-items: center;   /* Centers the content */
    justify-content: center; /* Centers vertically */
    gap: 8px;               /* Spacing between elements */
    background: #f8fafc;
    margin-top: 20px;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #ccc;
    text-align: center;     /* Centers the text */
}


.rent-row {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.rent-box {
    width: 48%;
}

.rent-diff {
    width: 100%;
    text-align: center;
    font-weight: bold;
}

/* 🌡️ COLOR FOR RENT DIFFERENCE */
.text-red {
    color: #dc2626;
}

.text-green {
    color: #16a34a;
}

/* 📜 FULL-WIDTH SECTIONS */
.full-width {
    grid-column: span 2;
    width: 100%;
}

/* 📝 DESCRIPTION */
.popup-description {
    font-size: 1rem;
    color: #555;
    border-top: 2px solid #e5e7eb;
    padding-top: 14px;
    margin-top: 16px;
}


/* 📌 AMENITIES SECTION */
.popup-amenities {
    border-top: 2px solid #e5e7eb;
    padding-top: 14px;
    margin-top: 16px;
    font-size: 1rem;
    color: #444;
}

/* 🔍 ZOOM BUTTON */
.zoom-btn {
    width: 100%;
    margin-top: 18px;
    padding: 14px;
    text-align: center;
    font-size: 1rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    transition: background 0.2s ease-in-out;
}

.zoom-btn:hover {
    background: #0056b3;
}

.leaflet-popup-content-wrapper {
    background: none;
    width: 100%;
    box-shadow: none;
}

.leaflet-popup-tip {
  background-color: blue;
}

.info-table {
    width: 100%;
    border-collapse: collapse;
}

.info-table td {
    padding: 4px 8px;
    vertical-align: middle;
    color: #444;
}

.info-table i {
    font-size: 1.2rem;
}

/* 🔵 LEGEND STYLING */
.legend {
  position: absolute;
  bottom: 30px;
  right: 30px;
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
