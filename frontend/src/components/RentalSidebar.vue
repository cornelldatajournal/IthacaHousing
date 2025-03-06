<template>
<div class="popup-container">
    <!-- Header -->
    <div class="popup-header">
        <div class="popup-title-container">
            <h3 class="popup-title">
                {{ listing.listingaddress }}, 
                <span v-if="listing.listingcity">{{ listing.listingcity }},</span> 
                {{ listing.listingzip }}
            </h3>
        </div>
        <button class="close-btn" @click="closePopup">✖</button>
    </div>

    <div class="popup-image-container">
        <!-- Left Arrow (Previous Image) -->
        <button v-if="listing.listingphotos && listing.listingphotos.length > 0" @click="prevImage" class="nav-arrow left-arrow">❮</button>

        <!-- Image Display -->
        <img 
        v-if="extractPhoto(listing.listingphotos).length > 0" 
        :src="extractPhoto(listing.listingphotos)[currentImageIndex].PhotoUrl" 
        alt="Listing Photo" 
        class="listing-image"
        >
        <!-- Right Arrow (Next Image) -->
        <button v-if="extractPhoto(listing.listingphotos).length > 1" @click="nextImage" class="nav-arrow right-arrow">❯</button>
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
    <div class="rent-diff" :class="{'text-red': ((listing.predictedrent-listing.rentamount)/listing.rentamount*100).toFixed(2)  < 0, 'text-green': ((listing.predictedrent-listing.rentamount)/listing.rentamount*100).toFixed(2)  > 0}">
        Percent Change: {{ ((listing.predictedrent-listing.rentamount)/listing.rentamount*100).toFixed(2) }}%
    </div>
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
            <td>Avg. Walking Time:</td>
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
            <td>Convenience:</td>
            <td>{{ listing.amenities_score ?? "N/A" }}/100</td>
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
    <strong>Amenities: </strong>
    <span class="amenities-list">
        {{ listing.amenities ? listing.amenities.replace(/[\[\]']/g, "") : "None Listed" }}
    </span>
    </div>

   

    <!-- Zoom Button -->
</div>
</template>

<script setup>
import { defineProps, defineEmits, ref, computed } from 'vue';

const props = defineProps({
    listing: Object,
});

const emit = defineEmits(['close', 'zoom']);

const closePopup = () => {
    emit('close');
};

const currentImageIndex = ref(0); // Holds the current index of the images in the gallery
const totalImages = computed(() => extractPhoto(props.listing.listingphotos).length); // Holds the number of images in the gallery

/**
 * Extracts and Processes JSON String to get photos.
 * @param {string} listingPhotosStr - JSON string of listing photos.
 * @returns {Array} - Parsed array of photo objects, or an empty array if invalid.
 */
 const extractPhoto = (listingPhotosStr) => {
    if (!listingPhotosStr) return []; // Ensure a valid input

    try {
        // Normalize and clean up the JSON string
        const cleanedStr = listingPhotosStr
            .replace(/'/g, '"')          
            .replace(/\bTrue\b/g, 'true')
            .replace(/\bFalse\b/g, 'false')
            .replace(/\bNone\b/g, 'null')
            .replace(/\\n/g, '')         
            .replace(/\\t/g, '')      
            .trim();                   

        // Parse JSON safely
        const listingPhotos = JSON.parse(cleanedStr);

        // Ensure it's an array and return, otherwise return an empty array
        return Array.isArray(listingPhotos) ? listingPhotos : [];

    } catch (error) {
        console.error("JSON Parsing Error:", error.message);
        return []; // Return an empty array on failure
    }
};


/**
 * Goes to Next Image in Carosel
 */
const nextImage = () => {
  if (currentImageIndex.value < totalImages.value - 1) {
    currentImageIndex.value++;
  } else {
    currentImageIndex.value = 0; 
  }
};

/**
 * Goes to Previous Image in Carosel
 */
const prevImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--;
  } else {
    currentImageIndex.value = totalImages.value - 1;
  }
};

</script>
  

<style scoped>
/* 📦 POPUP CONTAINER */
.popup-container {
    background: #ffffff;
    padding: 20px;
    width: 640px;
    height: 100vh;
    box-shadow: 0 5px 14px rgba(0, 0, 0, 0.12);
    border: 1px solid #ddd;
    z-index: 500;
    overflow: scroll;
}

/* 🔝 HEADER */
.popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #e5e7eb;
    padding: 16px;
    border-radius: 8px 8px 0 0;
}

/* Centered Title */
.popup-title-container {
    flex-grow: 1;
    text-align: center;
}

.popup-title {
    font-size: 1.3rem;
    color: #222;
    margin: 0;
}

/* Close Button */
.close-btn {
    background: none;
    border: none;
    font-size: 1rem;
    cursor: pointer;
    color: #888;
    transition: color 0.2s;
}

.close-btn:hover {
    color: #555;
}

/* Image Section */
.popup-image-container {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 10px;
}

.listing-image {
    width: 100%;
    max-height: 250px;
    object-fit: cover;
    border: 2px solid #e5e7eb;
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
    background: none;
    padding: 20px;
    border: 1px solid none;
    text-align: center;
    font-family: "Inter", sans-serif;
    align-items: center;
    border-top: 2px solid #e5e7eb;
    border-bottom: 2px solid #e5e7eb;
    margin-bottom: 20px;
}

.rent-box {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: none;
    padding: 10px;
    width: 100%;
    border: 2px solid #e5e7eb;
}

.rent-box strong {
    color: #374151;
}

.rent-box span {
    font-size: 1rem;
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
    font-size: 1rem;
    font-weight: bold;
    color: #374151;
    margin-top: 10px;
    background: none;
    padding: 10px;
    border: 2px solid #e5e7eb;
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
    padding-bottom: 14px;
    margin-top: 16px;
    font-size: 1rem;
    color: #444;
}

/* 🔍 ZOOM BUTTON */
.zoom-btn {
    width: 40px; /* Set fixed width */
    height: 40px; /* Set fixed height */
    background-color: #f5f5f5; /* Light background */
    border: none;
    border-radius: 50%; /* Make it circular */
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.2s ease-in-out;
}

/* Ensure the icon is centered */
.zoom-btn svg {
    width: 20px;
    height: 20px;
    color: #333;
}

/* Hover effect */
.zoom-btn:hover {
    background-color: #ddd;
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

.popup-image-container {
  position: relative;
  width: 100%;
  max-width: 600px; /* Adjust based on design */
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-radius: 12px;
}

.listing-image {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 12px;
  transition: opacity 0.3s ease-in-out;
}

/* 🔹 Modern Navigation Arrows */
.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.4);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}

.nav-arrow:hover {
  background: rgba(0, 0, 0, 0.7);
  transform: scale(1.1);
}

.left-arrow {
  left: 10px;
}

.right-arrow {
  right: 10px;
}

/* 🔹 Sleek Arrow Icons */
.arrow-icon {
  font-size: 22px;
  font-weight: bold;
  user-select: none;
}

</style>