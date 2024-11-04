import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

// Import Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

// Import głównego pliku CSS
import './App.css';

// Import Font Awesome
import '@fortawesome/fontawesome-free/css/all.min.css';

createApp(App).use(router).mount('#app');
