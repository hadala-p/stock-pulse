<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <h2 class="text-center mb-4">Sign in</h2>
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input
                type="email"
                class="form-control"
                id="email"
                v-model="email"
                required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
                type="password"
                class="form-control"
                id="password"
                v-model="password"
                required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">Sign in</button>
        </form>
        <div class="text-center mt-3">
          <p>Don't have an account? <router-link to="/register">Sign up!</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { inject } from 'vue';

export default {
  name: 'LoginPage',
  setup() {
    const updateLoginStatus = inject('updateLoginStatus');

    return {
      updateLoginStatus,
    };
  },
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await axios.post('/auth/login', {
          email: this.email,
          password: this.password,
        });

        if (response.data.status) {
          localStorage.setItem('token', response.data.result.token);
          this.updateLoginStatus(true);
          this.$router.push('/');
        } else {
          alert('Login failed: ' + response.data.error);
        }
      } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login.');
      }
    },
  },
};
</script>

<style scoped>

</style>
