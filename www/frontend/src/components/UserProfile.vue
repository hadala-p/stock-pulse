<template>
  <div class="container my-5">
    <h1>Hi! {{ nickname }}</h1>
    <p>Welcome to your profile page!</p>
  </div>
</template>

<script>
import { inject } from 'vue';

export default {
  name: 'UserProfile',
  setup() {
    const nickname = inject('nickname');

    return {
      nickname,
    };
  },
};
</script>

<style scoped>

</style>
