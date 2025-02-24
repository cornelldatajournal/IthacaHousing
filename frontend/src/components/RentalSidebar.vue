<template>
<div class="popup-container">
    <!-- Header -->
    <div class="popup-header">
    <h3 class="popup-title">
        {{ listing.listingaddress }}, {{ listing.listingcity }}, {{ listing.listingzip }}
    </h3>
    <button class="close-btn" @click="closePopup">✖</button>
    </div>

    <!-- Main Content (2-Column Layout) -->
    <div class="popup-content grid grid-cols-2 gap-4">
    <!-- Left Column (Transit & Walking Info) -->
    <div class="popup-left">
        <table class="info-table">
        <tr>
            <td><i class="fa-solid fa-bus text-blue-500"></i></td>
            <td>Transit Score:</td>
            <td>{{ listing.transit_score ?? "N/A" }}</td>
        </tr>
        <tr>
            <td><i class="fa-solid fa-person-walking text-green-500"></i></td>
            <td>Arts Quad:</td>
            <td>{{ (listing.ag_quad_time/60).toFixed(0) ?? "N/A" }} min</td>
        </tr>
        <tr>
            <td><i class="fa-solid fa-person-walking text-green-500"></i></td>
            <td>Ag Quad:</td>
            <td>{{ (listing.arts_quad_time/60).toFixed(0) ?? "N/A" }} min</td>
        </tr>
        <tr>
            <td><i class="fa-solid fa-person-walking text-green-500"></i></td>
            <td>Uris Hall:</td>
            <td>{{ (listing.uris_hall_time/60).toFixed(0) ?? "N/A" }} min</td>
        </tr>
        <tr>
            <td><i class="fa-solid fa-person-walking text-yellow-500"></i></td>
            <td>Average Walking Time:</td>
            <td>{{ (listing.avg_walking_time/60).toFixed(0) ?? "N/A" }} min</td>
        </tr>
        </table>
    </div>

    <!-- Right Column (Bedrooms, Pets, Amenities) -->
    <div class="popup-right">
        <table class="info-table">
        <tr>
            <td><i class="fa-solid fa-bed text-indigo-500"></i></td>
            <td>Bedrooms:</td>
            <td>{{ listing.bedrooms }}</td>
        </tr>
        <tr>
            <td><i class="fa-solid fa-toilet text-purple-500"></i></td>
            <td>Bathrooms:</td>
            <td>{{ listing.bathrooms }}</td>
        </tr>
        <tr>
            <td><i class="fa fa-paw text-yellow-600"></i></td>
            <td>Pets:</td>
            <td>{{ listing.pets === "Yes" ? "Allowed" : "Not Allowed" }}</td>
        </tr>
        <tr>
            <td><i class="fa fa-home text-indigo-600"></i></td>
            <td>Housing Type:</td>
            <td>{{ listing.housingtype ?? "N/A" }}</td>
        </tr>
        <tr>
            <td><i class="fa-solid fa-shield-halved text-yellow-500"></i></td>
            <td>Safety:</td>
            <td>{{ listing.overallsafetyratingpct ?? "N/A" }}%</td>
        </tr>
        </table>
    </div>
    </div>

    <!-- Description -->
    <div class="popup-description">
    {{ listing.shortdescription }}
    </div>

    <!-- Amenities Section -->
    <div class="popup-amenities">
    <strong>Amenities:</strong>
    <span class="amenities-list">
        {{ listing.amenities ? listing.amenities.replace(/[\[\]']/g, "") : "None Listed" }}
    </span>
    </div>

    <!-- Rental Information -->
    <div class="rent-section">
    <div class="rent-box">
        <strong>Rent:</strong>
        <span>${{ listing.rentamount.toFixed(2) }}</span>
    </div>
    <div class="rent-box">
        <strong>Predicted Rent:</strong>
        <span :class="{'text-green': listing.differenceinfairvalue < 0, 'text-red': listing.differenceinfairvalue > 0}">
        ${{ listing.predictedrent.toFixed(2) }}
        </span>
    </div>
    <div class="rent-diff" :class="{'text-green': listing.differenceinfairvalue < 0, 'text-red': listing.differenceinfairvalue > 0}">
        Difference: ${{ Math.abs(listing.differenceinfairvalue).toFixed(2) }}
    </div>
    </div>

    <!-- Zoom Button -->
    <button class="zoom-btn" @click="zoomToLocation">
    🔍 Zoom to Location
    </button>
</div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
    listing: Object,
});

const emit = defineEmits(['close', 'zoom']);

const closePopup = () => {
    emit('close');
};

const zoomToLocation = () => {
    emit('zoom', { lat: props.listing.latitude, lng: props.listing.longitude });
};
</script>
  

<style scoped>
/* 📦 POPUP CONTAINER */
.popup-container {
    background: #ffffff;
    padding: 20px;
    width: 640px;
    height: 100%;
    box-shadow: 0 5px 14px rgba(0, 0, 0, 0.12);
    border: 1px solid #ddd;
    z-index: 500;
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

/* SIDEBAR POPUP */
.popup-sidebar {
  position: fixed;
  top: 60px;
  right: 30px;
  width: auto;
  max-height: 90vh;
  overflow-y: auto;
  background: white;
  box-shadow: -3px 0 15px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  padding: 20px;
  border-left: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.popup-sidebar {
  display: flex;
}

.close-sidebar {
  background: none;
  border: none;
  font-size: 1.3rem;
  cursor: pointer;
  color: #888;
  align-self: flex-end;
  transition: color 0.2s ease-in-out;
}

.close-sidebar:hover {
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
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    background: #ffffff;
    margin-top: 20px;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
    text-align: center;
    font-family: "Inter", sans-serif;
    align-items: center;
}

.rent-box {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: #f9fafb;
    padding: 10px;
    border-radius: 8px;
    width: 100%;
}

.rent-box strong {
    font-size: 1.1rem;
    color: #374151;
}

.rent-box span {
    font-size: 1.4rem;
    font-weight: bold;
    margin-top: 5px;
    color: #111827;
}

.text-green {
    color: #16a34a;
}

.text-red {
    color: #dc2626;
}

.rent-diff {
    grid-column: span 2;
    font-size: 1.2rem;
    font-weight: bold;
    color: #374151;
    margin-top: 10px;
    background: #f1f5f9;
    padding: 10px;
    border-radius: 8px;
}

.rent-diff.text-red {
    color: #dc2626;
}

.rent-diff.text-green {
    color: #16a34a;
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
    background: #151366;
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

</style>