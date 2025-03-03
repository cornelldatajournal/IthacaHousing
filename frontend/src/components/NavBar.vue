<template>
<nav class="navbar-container">
    <div class="navbar-inner">
        <!-- Logo and Brand (Aligned to the far left) -->
        <div class="navbar-brand">
            <img src="@/assets/CDJLogo.png" alt="Logo" class="navbar-logo" />
            <div class="navbar-title">
            <router-link to="/" class="navbar-name">Ithaca Insights</router-link>
            <span class="navbar-subtitle">by Cornell Data Journal</span>
            </div>
        </div>

        <!-- Navigation Menu -->
        <ul class="navbar-menu">
            <li><router-link to="/" active-class="active-link">Rental Valuation</router-link></li>
            <li><router-link to="/history" active-class="active-link">Time Capsule</router-link></li>
            <li><a href="https://cornelldatajournal.org/" target="_blank" active-class="active-link">Cornell Data Journal</a></li>
            <li><router-link to="/about" active-class="active-link">About</router-link></li>
        </ul>
    </div>
</nav>
</template>

<style scoped>
/* Navbar Container */
.navbar-container {
    background: rgba(255, 255, 255, 0.9);  /* Translucent white */
    backdrop-filter: blur(12px);            /* Frosted glass effect */
    -webkit-backdrop-filter: blur(12px);    /* For Safari support */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding: 8px 20px;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
}

/* Inner Flex Container */
.navbar-inner {
display: flex;
align-items: center;
max-width: 100%;
margin: 0 auto;
}

.navbar-brand {
    display: flex;
    align-items: center; 
    gap: 0px; 
}

/* Logo */
.navbar-logo {
    width: 40px;
    height: auto;
}

/* Title and Subtitle Container */
.navbar-title {
    display: flex;
    flex-direction: column; 
    gap: 0px;
    line-height: 1.2; 
}

/* Main Title */
.navbar-name {
    font-size: 1.1rem;
    font-weight: bold;
    color: #151366;
    text-decoration: none;
    transition: color 0.2s ease-in-out;
}

/* Subtitle */
.navbar-subtitle {
    font-size: 0.9rem;
    color: #666;
    font-weight: normal;
}


/* Menu Links */
.navbar-menu {
display: flex;
gap: 25px;
list-style: none;
}

.navbar-menu li {
font-size: 0.95rem;
}

.navbar-menu a {
text-decoration: none;
color: #374151;
transition: color 0.2s ease-in-out;
padding: 2px 0;
display: inline-block;
border-bottom: 2px solid transparent;
}

.navbar-menu a:hover {
color: #1d4ed8;
}

.active-link {
color: #1d4ed8;
font-weight: bold;
border-bottom: 2px solid #1d4ed8;
}
</style>
  