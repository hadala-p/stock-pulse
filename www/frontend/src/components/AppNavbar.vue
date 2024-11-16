<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <router-link class="navbar-brand d-flex align-items-center" to="/" aria-label="Home">
        <img src="@/assets/logo.png" alt="Logo" class="me-2" width="30" height="30" />
        <span>Stock-Pulse</span>
      </router-link>

      <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarContent"
          aria-controls="navbarContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav me-auto"></ul>

        <form class="d-flex mx-auto my-2 my-lg-0" @submit.prevent="handleSearch">
          <input
              class="form-control search-input"
              type="search"
              placeholder="Search"
              aria-label="Search"
              v-model="searchQuery"
          />
          <button class="btn btn-outline-light" type="submit">
            <i class="fas fa-search"></i>
          </button>
        </form>
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/login">
              <i class="fas fa-sign-in-alt me-1"></i> Sign in
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar',
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    handleSearch() {
      // Logic to handle search
      // TO DO: Implement search functionality
      console.log('Search query:', this.searchQuery);
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
