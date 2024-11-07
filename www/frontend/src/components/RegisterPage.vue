<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <h2 class="text-center mb-4">Sign up</h2>
        <form @submit.prevent="handleRegister">
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
            <label for="username" class="form-label">NickName</label>
            <input
                type="text"
                class="form-control"
                id="username"
                v-model="username"
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
          <div class="mb-3">
            <label for="confirmPassword" class="form-label">Confirm Password</label>
            <input
                type="password"
                class="form-control"
                id="confirmPassword"
                v-model="confirmPassword"
                required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">Sign up</button>
        </form>
        <div class="text-center mt-3">
          <p>Have an account? <router-link to="/login">Sign in!</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterPage',
  data() {
    return {
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert('Passwords are not identical.');
        return;
      }
      if (this.password.length < 6) {
        alert('The password must have at least 6 characters.');
        return;
      }
      console.log('Registration successful');
      console.log('Email:', this.email);
      console.log('NickName:', this.username);
      console.log('Password:', this.password);
    },
  },
};
</script>

<style scoped>

</style>
