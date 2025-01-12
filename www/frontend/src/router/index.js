import { createRouter, createWebHashHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import LoginPage from '../views/LoginPage.vue';
import RegisterPage from '../views/RegisterPage.vue';
import PredictionsPage from '../views/PredictionsPage.vue';
import FavoritesPage from '../views/FavoritesPage.vue';
import UserProfile from '../views/UserProfile.vue';

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

