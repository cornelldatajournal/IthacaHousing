<template>
<NavBar />
<div class="info-section">
    <!--Hero Section MAKE BALANCE SMOOTHER MAKE WORDS ON EACH LINE EQUAL-->
    <section class="hero">
        <div class="hero-content">
          <div class="hero-text">
            <h1 class="hero-title">Explore Fair Rent in Ithaca</h1>
            <p class="hero-subtitle">
                Ithaca Insights is a live dashboard uncovering rental pricing inefficiencies across Tompkins County.
            </p>
          </div>
          <li><router-link to="/rent" class="cta-button">View Map</router-link></li>
        </div>
    </section>

    <!--Value Prop Section-->
    <section class="value-prop-section">
      <div class="value-prop-container">
        <h2 class="value-prop-heading">Why Ithaca Insights?</h2>
        <div class="value-prop-cards">

          <div class="value-card">
            <h3 class="value-title">Transparent Pricing</h3>
            <p class="value-text">
              We reveal overpriced listings by comparing market rent to actual listing data—empowering renters and informing city planners.
            </p>
          </div>

          <div class="value-card">
            <h3 class="value-title">Data-Driven Intelligence</h3>
            <p class="value-text">
              Backed by web scraping, regression models, and geospatial analysis, our dashboard transforms raw housing data into actionable insights.
            </p>
          </div>

          <div class="value-card">
            <h3 class="value-title">Accessible for All</h3>
            <p class="value-text">
              Built for students, landlords, and policymakers alike—our interface is intuitive, fast, and freely available to the public.
            </p>
          </div>

        </div>
      </div>
    </section>

    <!--Team Section-->
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
            <p class="member-role">Researcher</p>
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
  gap: 20px
}


/* Hero Section */
.hero {
  /* background: linear-gradient(135deg, #dbeafe 0%, #f0f4ff 100%); */
  padding: 3rem 5vw;
  text-align: center;
  align-items: center;
  margin-top: 2%;
  
}

.hero-content {
  max-width: 720px;
  animation: fadeIn 1.5s ease-in-out;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.hero-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  color: #1e3a8a;
  white-space: nowrap;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #374151;
  line-height: 1.6;
  max-width: 600px;
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

/* Value Prop Section */
.value-prop-section {
  padding: 20px 20px;
  font-family: 'DM Sans', sans-serif;
}

.value-prop-container {
  max-width: 1100px;
  margin: 0 auto;
}

.value-prop-heading {
  font-size: 2.75rem;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 3rem;
  text-align: center;

}

.value-prop-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
}

.value-card {
  background: #ffffff;
  padding: 30px 25px;
  border-radius: 12px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.06);
  width: 300px;
  transition: transform 0.3s ease;
}

.value-card:hover {
  transform: translateY(-6px);
}

.value-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e3a8a;
  margin-bottom: 1rem;
}

.value-text {
  font-size: 1.1rem;
  color: #4b5563;
  line-height: 1.6;
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
  