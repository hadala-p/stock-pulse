<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <router-link class="navbar-brand d-flex align-items-center" to="/" aria-label="Home">
        <img src="@/assets/logo.png" alt="Logo" class="me-2" width="30" height="30" />
        <span>Stock-Pulse</span>
      </router-link>

      <ul class="navbar-nav flex-row">
        <li class="nav-item mx-3">
          <router-link class="nav-link" to="/" aria-label="Dashboard">
            <i class="fas fa-chart-line fa-lg"></i>
          </router-link>
        </li>
        <li class="nav-item mx-3">
          <router-link class="nav-link" to="/predictions" aria-label="Predictions">
            <i class="fas fa-chart-pie fa-lg"></i>
          </router-link>
        </li>
        <li class="nav-item mx-3">
          <router-link class="nav-link" to="/favorites" aria-label="Favorites">
            <i class="fas fa-star fa-lg"></i>
          </router-link>
        </li>
      </ul>

      <div>
        <template v-if="isLoggedIn">
          <router-link class="nav-link text-white" to="/profile">
            <i class="fas fa-user me-1"></i> Profile
          </router-link>
          <button @click="logout" class="btn btn-link nav-link text-white">
            <i class="fas fa-sign-out-alt me-1"></i> Logout
          </button>
        </template>
        <template v-else>
          <router-link class="nav-link text-white" to="/login">
            <i class="fas fa-sign-in-alt me-1"></i> Sign in
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { inject } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'AppNavbar',
  setup() {
    const isLoggedIn = inject('isLoggedIn');
    const updateLoginStatus = inject('updateLoginStatus');
    const router = useRouter();

    const logout = () => {
      localStorage.removeItem('token');
      updateLoginStatus(false);
      router.push('/login');
    };

    return {
      isLoggedIn,
      logout,
    };
  },
};
</script>

<style>
/* Style for navigation icons */
.navbar-nav {
  flex-direction: row;
}

.nav-item .nav-link {
  color: #fff;
}

.nav-item .nav-link:hover {
  color: #ddd;
}

/* Style for the logotype */
.navbar-brand span {
  font-size: 1.25rem;
  font-weight: bold;
  color: #fff;
}
</style>
