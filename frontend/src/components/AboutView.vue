<template>
<NavBar />
<div class="info-section">
    <section class="hero">
        <div class="hero-content">
        <h1 class="hero-title">Explore Fair Rent in Ithaca</h1>
        <p class="hero-subtitle">
            Ithaca Insights is a live dashboard uncovering rental pricing inefficiencies across Tompkins County.
        </p>
        <li><router-link to="/rent" class="cta-button">View Map</router-link></li>
        </div>
    </section>

    <section class="team-section">
        <h2 class="team-title">Meet the Team</h2>
        <div class="team-grid">
        <div class="team-card">
            <div class="avatar-placeholder"></div>
            <h3 class="member-name">Arjun Maitra</h3>
            <p class="member-role">Data Scientist</p>
        </div>
        <div class="team-card">
            <div class="avatar-placeholder"></div>
            <h3 class="member-name">Steven Zhou</h3>
            <p class="member-role">Data Scientist</p>
        </div>
        <div class="team-card">
            <div class="avatar-placeholder"></div>
            <h3 class="member-name">Vivian Guo</h3>
            <p class="member-role">UI/UX, Researcher</p>
        </div>
        <div class="team-card">
            <div class="avatar-placeholder"></div>
            <h3 class="member-name">N/a</h3>
            <p class="member-role"></p>
        </div>
        </div>
    </section>
</div>
</template>
  
  
<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
</script>

<style scoped>
/* Layout */
.info-section {
  margin-top: 2%;
  width: 100vw;
  margin-left: auto;
  margin-right: auto;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center; 
}


/* Hero Section */
.hero {
  /* background: linear-gradient(135deg, #dbeafe 0%, #f0f4ff 100%); */
  padding: 3rem 5vw;
  text-align: center;
  align-items: center;
  
}

.hero-content {
  max-width: 720px;
  animation: fadeIn 1.5s ease-in-out;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 1rem;
  white-space: nowrap;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #374151;
  margin-bottom: 1.75rem;
  line-height: 1.6;
}

.cta-button {
  display: inline-block;
  padding: 12px 28px;
  font-size: 1.1rem;
  font-weight: 600;
  color: white;
  background: #1e3a8a;
  border-radius: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 6px 16px rgba(30, 58, 138, 0.3);
}

.cta-button:hover {
  transform: scale(1.05);
  background: #1d4ed8;
}

/* Team Section */
.team-section { 
  padding: 2rem 5vw 4rem;
  align-items: center;
  display: flex;
  flex-direction: column;
}

.team-title {
  font-size: 2rem;
  color: #1e3a8a;
  font-weight: 700;
  margin-bottom: 2rem;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* exactly 4 equal columns */
  gap: 2rem;
}

.team-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  text-align: left;
}

.avatar-placeholder {
  width: 100%;
  padding-top: 100%;
  background: #e0e7ff;
  border-radius: 50%;
  margin-bottom: 1rem;
}

.member-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e3a8a;
  margin-bottom: 0.25rem;
}

.member-role {
  font-size: 1rem;
  color: #4b5563;
}

/* Animation */
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
</style>
  