<template>
<NavBar />
<section class="body-container">
    <section class="coming-soon-container">
        <div class="coming-soon-content">
        <h1 class="coming-soon-title">Ithaca's Urban Growth</h1>
        <p class="coming-soon-subtitle">How will Ithaca grow in the future?</p>
        <p class="coming-soon-text">We're working hard to bring you advanced data, predictive insights, and interactive maps. Stay tuned!</p>
        <div class="coming-soon-badge">Coming Soon!</div>
        </div>
    </section>
</section>
</template>

<script setup>
import NavBar from "@/components/NavBar.vue";
</script>

<style scoped>
/* */
.body-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 95vw;
    height: 100vh; /* Full viewport height */
    overflow: hidden;
    background: none;
}

/* 🎨 Main Container */
.coming-soon-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50%;
    padding: 20px;
    background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
    font-family: 'DM Sans', sans-serif;
    text-align: center;

}


/* 📜 Content */
.coming-soon-content {
max-width: 800px;
background: #ffffff;
padding: 30px;
border-radius: 12px;
box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
animation: fadeIn 1s ease-in-out;
}

/* 🖋️ Text Styles */
.coming-soon-title {
font-size: 3rem;
font-weight: bold;
color: #151366;
margin-bottom: 10px;
}

.coming-soon-subtitle {
font-size: 1.4rem;
color: #4b5563;
margin-bottom: 20px;
}

.coming-soon-text {
font-size: 1.1rem;
color: #6b7280;
margin-bottom: 30px;
line-height: 1.5;
}

/* 🏷️ Badge */
.coming-soon-badge {
display: inline-block;
padding: 10px 20px;
font-size: 1.2rem;
font-weight: bold;
color: white;
background: #151366;
border-radius: 8px;
box-shadow: 0 4px 12px rgba(29, 78, 216, 0.4);
animation: pulse 2s infinite;
}

/* 🎥 Animations */
@keyframes fadeIn {
0% {
    opacity: 0;
    transform: translateY(20px);
}
100% {
    opacity: 1;
    transform: translateY(0);
}
}

@keyframes pulse {
0%, 100% {
    transform: scale(1);
}
50% {
    transform: scale(1.05);
}
}
</style>
    