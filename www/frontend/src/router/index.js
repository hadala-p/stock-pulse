import { createRouter, createWebHashHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import PredictionsPage from '../components/PredictionsPage.vue';
import FavoritesPage from '../components/FavoritesPage.vue';

const routes = [
    {
        path: '/',
        name: 'HomePage',
        component: HomePage,
    },
    {
        path: '/login',
        name: 'LoginPage',
        component: LoginPage,
    },
    {
        path: '/register',
        name: 'RegisterPage',
        component: RegisterPage,
    },
    {
        path: '/predictions',
        name: 'PredictionsPage',
        component: PredictionsPage,
    },
    {
        path: '/favorites',
        name: 'FavoritesPage',
        component: FavoritesPage,
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
