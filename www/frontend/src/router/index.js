import { createRouter, createWebHashHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import PredictionsPage from '../components/PredictionsPage.vue';
import FavoritesPage from '../components/FavoritesPage.vue';
import UserProfile from '../components/UserProfile.vue';

const routes = [
    { path: '/', name: 'HomePage', component: HomePage },
    { path: '/login', name: 'LoginPage', component: LoginPage },
    { path: '/register', name: 'RegisterPage', component: RegisterPage },
    { path: '/predictions', name: 'PredictionsPage', component: PredictionsPage },
    {
        path: '/favorites',
        name: 'FavoritesPage',
        component: FavoritesPage,
        meta: { requiresAuth: true },
    },
    { path: '/profile', name: 'UserProfile', component: UserProfile, meta: { requiresAuth: true } },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const isLoggedIn = !!localStorage.getItem('token');

    if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
        next('/login');
    } else {
        next();
    }
});

export default router;

