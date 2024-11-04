<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <h2 class="text-center mb-4">Rejestracja</h2>
        <form @submit.prevent="handleRegister">
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
            <label for="username" class="form-label">Nazwa Użytkownika</label>
            <input
                type="text"
                class="form-control"
                id="username"
                v-model="username"
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
          <div class="mb-3">
            <label for="confirmPassword" class="form-label">Potwierdź Hasło</label>
            <input
                type="password"
                class="form-control"
                id="confirmPassword"
                v-model="confirmPassword"
                required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">Zarejestruj się</button>
        </form>
        <div class="text-center mt-3">
          <p>Masz już konto? <router-link to="/login">Zaloguj się!</router-link></p>
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
        alert('Hasła nie są identyczne.');
        return;
      }
      if (this.password.length < 6) {
        alert('Hasło musi mieć co najmniej 6 znaków.');
        return;
      }
      console.log('Rejestracja udana');
      console.log('Email:', this.email);
      console.log('Nazwa Użytkownika:', this.username);
      console.log('Hasło:', this.password);
    },
  },
};
</script>

<style scoped>

</style>
