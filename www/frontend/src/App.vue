<template>
  <MainLayout>
    <AppNavbar />
    <router-view />
  </MainLayout>
</template>

<script>
import MainLayout from './layouts/MainLayout.vue';
import AppNavbar from './components/AppNavbar.vue';
import { ref, provide } from 'vue';

export default {
  name: 'App',
  components: {
    MainLayout,
    AppNavbar,
  },
  setup() {
    const isLoggedIn = ref(!!localStorage.getItem('token'));

    const updateLoginStatus = (status) => {
      isLoggedIn.value = status;
    };

    provide('isLoggedIn', isLoggedIn);
    provide('updateLoginStatus', updateLoginStatus);

    return {};
  },
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}
</style>
