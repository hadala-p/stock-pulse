<template>
  <div class="main-container d-flex flex-column min-vh-100">
    <AppNavbar />
    <div class="content-container flex-grow-1">
      <router-view />
    </div>
    <AppFooter />
  </div>
</template>

<script>
import AppNavbar from "@/components/AppNavbar.vue";
import AppFooter from '@/components/AppFooter.vue';


export default {
  components: {
    AppNavbar,
    AppFooter,
  },
};
</script>


<style>
.main-container {
  background-color: #f3faff;
}
</style>
