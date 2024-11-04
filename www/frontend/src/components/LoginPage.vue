<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <h2 class="text-center mb-4">Logowanie</h2>
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="email" class="form-label">Adres Email</label>
            <input
                type="email"
                class="form-control"
                id="email"
                v-model="email"
                required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Hasło</label>
            <input
                type="password"
                class="form-control"
                id="password"
                v-model="password"
                required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">Zaloguj się</button>
        </form>
        <div class="text-center mt-3">
          <p>Nie posiadasz konta? <router-link to="/register">Zarejestruj się!</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    handleSubmit() {
      console.log('Email:', this.email);
      console.log('Hasło:', this.password);
    },
  },
};
</script>

<style scoped>

</style>
