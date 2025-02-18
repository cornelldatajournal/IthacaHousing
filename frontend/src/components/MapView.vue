<template>
  <div class="overflow-auto box-border m-0 p-0">
    <!-- Map Container -->
    <div class="relative flex z-[0] border-b-2 border-black overflow-hidden">
      <div id="map"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { fetchListings } from "@/services/fetch";

const map = ref(null);

const getColor = (diff) => diff > 0 ? "red" : diff < 0 ? "green" : "gray";

onMounted(async () => {
  map.value = L.map("map", {
    center: [42.4, -76.5],
    zoom: 13,
    maxZoom: 20,
  });

  L.tileLayer('https://tile.jawg.io/jawg-streets/{z}/{x}/{y}{r}.png?access-token=pSUjHs1tEnhDqSIJpBV3miDFcODgE5a8MEyjIAmHPPMCZicbKrH3Z1O0mbhtTQTR', {
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
          <div class="popup-header">
            <h3 class="popup-title">${listing.listingaddress}</h3>
            <button class="close-btn" onclick="document.querySelector('.leaflet-popup-close-button').click()">✖</button>
          </div>

          <div class="popup-content">
            <div class="popup-section">
              <p class="popup-detail"><i class="fas fa-map-marker-alt"></i> <strong>${listing.listingcity}, ${listing.listingzip}</strong></p>
              <p class="popup-detail"><i class="fas fa-bed"></i> <strong>Bedrooms:</strong> ${listing.bedrooms}</p>
              <p class="popup-detail"><i class="fas fa-bath"></i> <strong>Bathrooms:</strong> ${listing.bathrooms}</p>
            </div>

            <div class="popup-section rent-section">
              <p class="popup-detail"><i class="fas fa-dollar-sign"></i> <strong>Rent:</strong> <span class="text-blue">$${listing.rentamount.toFixed(2)}</span></p>
              <p class="popup-detail"><i class="fas fa-chart-line"></i> <strong>Predicted Rent:</strong> <span class="text-green">$${listing.predictedrent.toFixed(2)}</span></p>
              <p class="popup-diff ${listing.differenceinfairvalue > 0 ? 'text-red' : 'text-green'}">
                <strong>Difference:</strong> 
                <span class="popup-diff-amount">$${listing.differenceinfairvalue.toFixed(2)}</span>
              </p>
            </div>

            <div class="popup-section">
              <p class="popup-description">${listing.shortdescription}</p>
            </div>

            <div class="popup-extra">
              <div class="popup-row">
                <div class="popup-badge"><i class="fas fa-bus"></i> Transit Score: <span>${listing.transit_score ?? "N/A"}</span></div>
                <div class="popup-badge"><i class="fas fa-shield-alt"></i> Safety: <span>${listing.overallsafetyratingpct ?? "N/A"}%</span></div>
              </div>
              <div class="popup-row">
                <div class="popup-badge"><i class="fas fa-paw"></i> Pets: <span>${listing.pets ?? "Not Specified"}</span></div>
                <div class="popup-badge"><i class="fas fa-home"></i> Housing Type: <span>${listing.housingtype ?? "N/A"}</span></div>
              </div>
            </div>

            <!-- Amenities -->
            <div class="popup-amenities">
              <strong>Amenities:</strong> 
              <span class="amenities-list">${listing.amenities ? listing.amenities.replace(/[\[\]']/g, "") : "None Listed"}</span>
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
#map {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
}

/* ✅ Custom Popup Styles */
.popup-container {
  font-family: "Inter", sans-serif;
  padding: 12px;
  max-width: 300px;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.popup-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: gray;
}

.popup-detail {
  font-size: 0.9rem;
  color: #444;
  margin: 5px 0;
}

.popup-diff {
  font-size: 0.9rem;
  font-weight: bold;
}

.text-red {
  color: red;
}

.text-green {
  color: green;
}

.popup-description {
  font-size: 0.85rem;
  color: #666;
  margin-top: 10px;
}

.zoom-btn {
  display: block;
  width: 100%;
  margin-top: 10px;
  padding: 8px;
  text-align: center;
  font-size: 0.9rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.zoom-btn:hover {
  background: #0056b3;
}

/* Leaflet Custom Popup */
.custom-popup .leaflet-popup-content-wrapper {
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
