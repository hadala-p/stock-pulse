<template>
  <MainLayout>
    <AppNavbar />
    <router-view />
  </MainLayout>
</template>

<script>
import MainLayout from './layouts/MainLayout.vue';
import AppNavbar from './components/AppNavbar.vue';
import { ref, provide, onMounted } from 'vue';

export default {
  name: 'App',
  components: {
    MainLayout,
    AppNavbar,
  },
  setup() {
    const isLoggedIn = ref(!!localStorage.getItem('token'));
    const nickname = ref(localStorage.getItem('nickname') || '');

    const updateLoginStatus = (status) => {
      isLoggedIn.value = status;
      if (!status) {
        nickname.value = '';
      }
    };


    const updateNickname = (newNickname) => {
      nickname.value = newNickname;
    };

    onMounted(() => {
      nickname.value = localStorage.getItem('nickname') || '';
    });

    provide('isLoggedIn', isLoggedIn);
    provide('updateLoginStatus', updateLoginStatus);
    provide('nickname', nickname);
    provide('updateNickname', updateNickname);

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
