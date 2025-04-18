<template>
<NavBar />
<section class="body-container">
    <section class="about-description-container">
        <div class="about-description-content">
        <h1 class="about-description-title">About Ithaca Insights</h1>
        <p class="about-description-subtitle">We built this website to explore Ithaca, our home. The Cornell Data Journal started by examining the housing crisis and rental uncertainity affecting Cornell students. <br/> <br/>Next, we plan to study Ithaca’s urban growth: its past, present, and future.</p>
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
.about-description-container {
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
.about-description-content {
    max-width: 800px;
    background: #ffffff;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
    animation: fadeIn 1s ease-in-out;
}

/* 🖋️ Text Styles */
.about-description-title {
    font-size: 3rem;
    font-weight: bold;
    color: #151366;
    margin-bottom: 10px;
}

.about-description-subtitle {
    font-size: 1.4rem;
    color: #4b5563;
    margin-bottom: 20px;
}

.about-description-text {
    font-size: 1.1rem;
    color: #6b7280;
    margin-bottom: 30px;
    line-height: 1.5;
}

/* 🏷️ Badge */
.about-description-badge {
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

.credits-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #edf2f7 0%, #f7fafc 100%);
  font-family: 'DM Sans', sans-serif;
}

.credits-content {
  max-width: 800px;
  background: #ffffff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
  animation: fadeIn 1s ease-in-out;
  text-align: center;
}

.credits-title {
  font-size: 2rem;
  font-weight: 600;
  color: #151366;
  margin-bottom: 15px;
}

.credits-text {
  font-size: 1.2rem;
  color: #4b5563;
  line-height: 1.6;
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
    