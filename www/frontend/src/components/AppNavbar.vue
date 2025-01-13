<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <router-link aria-label="Home" class="navbar-brand d-flex align-items-center" to="/">
        <img alt="Logo" class="me-2" height="30" src="@/assets/logo.png" width="30"/>
        <span>Stock-Pulse</span>
      </router-link>

      <button
          aria-controls="navbarContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
          class="navbar-toggler"
          data-bs-target="#navbarContent"
          data-bs-toggle="collapse"
          type="button"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div id="navbarContent" class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto"></ul>
        <form
            v-if="route.name !== 'RegisterPage' && route.name !== 'LoginPage'"
            class="d-flex mx-auto my-2 my-lg-0"
            @submit.prevent="handleSearch"
        >
          <button
              aria-label="Favorites"
              class="btn btn-link text-white me-2"
              @click="goToFavorites"
              type="button"
          >
            <i class="fas fa-star"></i>
          </button>
          <input
              v-model="searchQuery"
              @input="handleSearch"
              aria-label="Search"
              class="form-control search-input"
              placeholder="Search"
              type="search"
          />
        </form>

        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <template v-if="isLoggedIn">
            <li class="nav-item">
              <router-link class="nav-link text-white" to="/profile">
                <i class="fas fa-user me-1"></i> {{ nickname }}
              </router-link>
            </li>
            <li class="nav-item">
              <button class="btn btn-link nav-link text-white" @click="logout">
                <i class="fas fa-sign-out-alt me-1"></i> Logout
              </button>
            </li>
          </template>
          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link text-white" to="/login">
                <i class="fas fa-sign-in-alt me-1"></i> Sign in
              </router-link>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { inject } from 'vue';
import {useRoute, useRouter} from 'vue-router';
import { EventBus } from '../EventBus';

export default {
  name: 'AppNavbar',
  setup() {
    const isLoggedIn = inject('isLoggedIn');
    const updateLoginStatus = inject('updateLoginStatus');
    const nickname = inject('nickname');
    const router = useRouter();
    const route = useRoute();

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('nickname');
      updateLoginStatus(false);
      router.push('/login');
    };

    const goToFavorites = () => {
      router.push('/favorites');
    };

    return {
      isLoggedIn,
      logout,
      nickname,
      route,
      goToFavorites,
    };
  },
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    handleSearch() {
      EventBus.emit('search', this.searchQuery);
    },
  },
};
</script>

<style scoped>
/* Logo styling */
.navbar-brand span {
  font-size: 1.25rem;
  font-weight: bold;
  color: #fff;
}

/* Search bar styling */
.search-input {
  width: 10rem;
  transition: width 0.3s ease;
}

.search-input:focus {
  width: 30rem;
}
</style>
