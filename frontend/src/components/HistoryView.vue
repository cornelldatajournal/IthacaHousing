<template>
    <NavBar />

    <div class = "story-page">
        <section class="intro-section">
            <p class="subtitle">Today, Ithaca is regarded as a place of cultural richness.</p>
        </section>

        <section class="text-block">
        <p>From a well-loved farmer's market selling handmade goods from countless different countries, to events in the Commons featuring various cuisines and traditions, to students from all over the world taking classes together on Cornell's campus, our community is a blend of truly diverse global cultures. But in order to understand how Ithaca became what it is today, we have to travel into the past.
        </p>
        <p class="margin-adder">Let's take a look into a time capsule: one containing records from the 1920s, 30s, and 40s. These decades spanned events that impacted the global economy and caused societal shifts, which we will get the opportunity to observe through patterns in population and immigration. To begin, we turn to a pie chart showing the birthplace distribution of Ithaca residents throughout these earlier decades. 
        </p>
        </section>

        <!-- Graph Placeholder: Pie Chart - 1920 vs 1930 -->
        <section class="graph-section">
        <h3>Birthplace Origins of Ithaca Residents</h3>
        <BirthplaceChart />
        </section>

        <section class="text-block">
        <p>We can generally categorize this data by citizens being born in New York, and not being born in New York. Our data cannot give us details about whether or not an individual was born and raised in Ithaca specifically, only the general New York state. Darker colors, however, represent people who chose to move into, and reside in, Ithaca,
        </p>
        <p class="margin-adder">**Note: the 1940 data is not included here, because the census data is manually updated by HistoryForge, and the most recent version of the 40s data is missing many entries in both the “Place of Birth - Mother” and “Place of Birth - Father” columns.
        </p>
        <p class="margin-adder">From 1920 to 1930, we notice 4 primary trends:</p>
        <ul>
            <li>A decrease in people born in New York to New York natives</li>
            <li>An increase in second-generation immigrants/migrants</li>
            <li>An increase in internal migrants</li>
            <li>An increase in first-generation immigrants</li>
        </ul>
        <p class="margin-adder">
            Using historical context, we can explore these trends in relation to the larger world outside of Ithaca. 
        </p>
        <p>
            A decrease in New York born-and-raised families allows for us to assume that the growth in Ithaca's population between the two decades was primarily due to people from outside New York moving into the area, or the lasting effects of heightened immigration from the late 19th century to early 20th century. Even prior to the 1920s, Ithaca was a respectable and enjoyable place to raise a family, and so many second-generation immigrants or internal migrants settled, contributing to the population when they began having children of their own. 
        </p>
        <p class="margin-adder">
            The increase in population of internal migrants, born in the United States who moved to reside in Ithaca, is indicative of the 1920s being a time of economic expansion. The “Roaring Twenties”, as we know this phenomenon by, drove a distinct rise of the automobile industry, leading to greater mobility throughout the country as motor vehicle registrations nearly tripled between the years of 1920-1930. (https://www.railsand trails.com/AutoFacts/1930p15-100-8.jpg). 
        </p>
        </section>

        <!-- Map Placeholder: Highway Growth Maps -->
        <section class="text-block">
        <p>
            The following two maps illustrate the growth of highways within one decade, particularly the density of main roads in the Northeast. The ease of transportation would lead to an increase in travel, both to and from Ithaca. 
        </p>
        <div class="map-placeholder"><img src="/graphs/automobile1918.png"> </img></div>
        <div class="map-placeholder"><img src="/graphs/automobile1930.png"> </img></div>
        <p class="margin-adder"> 
            The population of immigrants, people who were born in another country but made the choice to relocate to the United States, remained stable between the two decades. While one might expect an increase, especially during such a time of economic growth, there were underlying policies that can help explain this trend. 
        </p>
        </section>

        <section class="text-block">
        <p>The Immigration Act of 1924 drastically limited immigration into the United States, based on quotas implemented with visas presented to a small percentage of a country's population (http://digitalexhibits.libraries.wsu.edu/exhibits/show/immigration-impacts-in-the-pac/item/7980). 
        </p>
        <p class="margin-adder">New immigration slowed down, and the country's foreign-born population began to decline. However, certain factors, such as most immigrants in Ithaca choosing to remain in the United States, and the proximity of academic institutions such as Cornell University, led to a relatively stable immigrant population between 1920 and 1930. 
        </p>
        <p class="margin-adder">
            With the extensive census data recorded, we can take an even closer look into this shift, or lack thereof: the specific breakdown of the immigrant population, and how the countries that they came from shifted despite the stagnancy caused by the new 1924 Act.
        </p>
        </section>

        <!-- Graph Placeholder: Country of Origin Bubbles -->
        <section class="graph-section">
        <h3>Immigrant Country of Origin Map</h3>
        <ImmigrantMap />
        <p class="margin-adder"> 
            This interactive map represents the many countries that immigrants in Ithaca originally came from, with bubble size corresponding to the number of people from each country. The legend on the side corresponds to the top 15 most common places of birth, outside of the US. Evidently, the majority of immigrants are from Europe, with the most coming from Italy and Ireland. 
        </p>
        </section>

        <section class="text-block">
        <div class="map-placeholder"><img src="/graphs/IrishImmigration.png"> </img></div>
        <p class="margin-adder">
          Between 1920 and 1930, we can observe a significant decrease in the immigrant population from Ireland, and a concurrent increase in the immigrant population from Italy. This could be due to a multitude of reasons, but placing it in historical context, it's likely a combination of the effects of the Great Depression on general mobility, and the Immigration Act of 1924. 
        </p>
        <p class="margin-adder">
          Irish immigration to the United States experienced an all time low in the 1930s and 1940s, as depicted in the bar chart to the left, and as reflected in the visible decrease of Irish immigrants residing in Ithaca during that time.  They were a population group disproportionately targeted by the Immigration Act of 1924, and its effects became visible in their gradually decreasing numbers. 
        </p>
        <div class="map-placeholder"><img src="/graphs/ItalianImmigration.png"> </img></div>
        <p class="margin-adder">We also notice a sizable increase in the Italian immigrant population between 1920 and 1930, likely following the massive surge in total Italian immigrants coming to the United States in 1920. This surge would not have been very noticeable until the 1930 census, so despite there being an Act passed during this decade, the effects of the Act aren't displayed until quite a few years later. 
        </p>
        <div class="map-placeholder"><img src="/graphs/ChineseImmigration.png"> </img></div>
        <p class="margin-adder">The hardest pattern to explain would be the increase in Chinese residents in Ithaca from 1920 to 1940, despite the Immigration Act most directly excluding Asian countries via quotas. However, since Ithaca is also so heavily associated with its proximity to institutions like Cornell University, the increase in Chinese immigration is likely due to students being accepted to study in US schools. In 1931, the Overseas Chinese Affairs Committee of the Nationalist Government was established, which justifies the slight but gradual increase in the number of Chinese immigrants over the course of the two decades (https://www.proquest.com/ dissertations-theses/cultural-journey-experiences-chinese-students /docview/304296509/se-2?accountid=10267)
        </p>
        <p class="margin-adder">
            No matter their reasons for coming to the United States, the question of where to begin their lives in a completely unfamiliar city, let alone country, is one that all new Ithacans had to face. For most immigrants, their answer wouldn't be about occupation or rent, it would come down to a sense of belonging. When surrounded by completely new people, languages, customs, and cultures, people will always be drawn to the familiar. Most immigrants naturally settled in areas with other immigrants of their home country, if only to hear their native language being spoken in passing, or to smell a childhood favorite dish on the way home from work. 
        </p>
        </section>

        <!-- Map Placeholder: Enclave Maps -->
        <section class="text-block">
        <p>Today, we have a name for these naturally formed cultural neighborhoods: ethnic enclaves. We see these formations in every major city, with countless different groups of people in similar situations. New York City alone, for example, has its Little Italy, Chinatown, Ukrainian Village, Little Saigon, Koreatown, and many more. It's no surprise that enclaves had formed in Ithaca as well with the growth of the immigrant population throughout the 20th century, and we can observe these enclaves to a small-scale extent through data.
        </p>
        <EthnicEnclavesMap class="margin-adder" />
        <p class="margin-adder">
            This series of maps depicts the living locations of the eight most common countries of origin, including China because of its listing as its own race in the census. An Italian neighborhood quickly emerged in the northwest, becoming stronger as more and more immigrants of the same background arrived. Near current day Collegetown, we also watch the formation of a cluster of Chinese immigrants, which we can reasonably predict would only continue to grow as regulations begin to ease up. The emergence of these cultural neighborhoods is essential to the diverse community fostered in Ithaca, which remains a century later, although exact locations and such may have shifted. 

        </p>
        <p class="margin-adder">Looking back on Ithaca's demographic past, we begin to understand how diversity is built generation by generation: decades of immigration leading to cultural traditions being passed on and ideas being spread. In the present day, we have the privilege of being able to stroll through the Commons, try the countless different cultured restaurants on every single street, and remember that each of them is a reminder of someone's journey to get here. 
        </p>
        </section>
    </div>
</template>
  

<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import BirthplaceChart from '@/components/charts/BirthplaceChart.vue';
import ImmigrantMap from '@/components/charts/ImmigrantMap.vue';
import EthnicEnclavesMap from "./charts/EthnicEnclavesMap.vue";

</script>

<style scoped>
.story-page {
  font-family: 'Georgia', serif;
  background: linear-gradient(to bottom, #fefaf5, #f8efe2);
  padding: 4rem 5vw;
  color: #2c2c2c;
  width: 80vw;
  margin: 10%;
  line-height: 1.8;
  font-size: 1.1rem;
  margin-top: 60px;
}

.margin-adder {
  margin-top: 2%;
}

.subtitle {
  font-size: 1.5rem;
  color: #6a4e3d;
  font-weight: 600;
  margin-bottom: 2rem;
  text-align: center;
}

.section-title {
  font-size: 1.6rem;
  color: #4b2e1f;
  border-left: 6px solid #a98274;
  padding-left: 1rem;
  margin-bottom: 1.5rem;
  font-weight: bold;
}

.text-block {
  margin-bottom: 3rem;
  background: rgba(255, 255, 255, 0.75);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

.styled-list {
  margin-left: 1rem;
  padding-left: 1rem;
  list-style-type: disc;
  color: #4b2e1f;
}

.graph-section, .map-section {
  margin: 4rem 0;
  background-color: #fff9f5;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.graph-placeholder, .map-placeholder {
  border: 3px dashed #c7b8aa;
  border-radius: 12px;
  padding: 4rem;
  text-align: center;
  background-color: #fcf7f1;
  margin-top: 1rem;
  font-size: 1rem;
  font-style: italic;
  color: #9c7e66;
}

.map-placeholder img {
  width: 100%;
  height: auto;
  display: block;
}

</style>

  