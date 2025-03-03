import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { library, dom } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from '@fortawesome/free-solid-svg-icons'
import { createHead } from '@vueuse/head';

library.add(fas)
dom.watch();

const app = createApp(App)
const head = createHead();
app.use(head);

app.use(createPinia())
app.use(router)

app.component("font-awesome-icon", FontAwesomeIcon)

app.mount('#app')
