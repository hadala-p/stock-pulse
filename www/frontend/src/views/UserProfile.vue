<template>
  <div class="container my-5 text-center">
    <div class="mb-4">
      <div class="position-relative d-inline-block">
        <img :src="imageUrl" class="rounded-circle" alt="Profile" style="width: 150px; height: 150px; object-fit: cover;">
        <div class="edit-overlay position-absolute d-flex align-items-center justify-content-center">
          <span class="text-white d-flex align-items-center">
            <i class="fas fa-pencil-alt me-2"></i>Edit
          </span>
        </div>
        <input type="file" @change="onFileChange" class="position-absolute file-input">
      </div>
    </div>
    <h1>Hi! {{ nickname }}</h1>
    <p>Welcome to your profile page!</p>
    <div class="mt-5 d-flex flex-column align-items-center">
      <div class="w-100 mb-3 text-center">
        <button @click="showEmailForm = !showEmailForm" class="btn btn-success" style="width: 33%;">Change Email</button>
        <transition name="slide">
          <form v-if="showEmailForm" @submit.prevent="changeEmail" style="max-width:400px; margin:0 auto;" class="mt-3">
            <div class="mb-3 text-start">
              <label>Current Email</label>
              <input type="text" class="form-control" v-model="currentEmail" disabled>
            </div>
            <div class="mb-3 text-start">
              <label>New Email</label>
              <input type="email" class="form-control" v-model="newEmail">
            </div>
            <button class="btn btn-primary w-100">Save</button>
          </form>
        </transition>
      </div>
      <div class="w-100 mb-3 text-center">
        <button @click="showPasswordForm = !showPasswordForm" class="btn btn-success" style="width: 33%;">Change Password</button>
        <transition name="slide">
          <form v-if="showPasswordForm" @submit.prevent="changePassword" style="max-width:400px; margin:0 auto;" class="mt-3">
            <div class="mb-3 text-start">
              <label>Current Password</label>
              <input type="password" class="form-control" v-model="currentPassword">
            </div>
            <div class="mb-3 text-start">
              <label>New Password</label>
              <input type="password" class="form-control" v-model="newPassword">
            </div>
            <div class="mb-3 text-start">
              <label>Repeat New Password</label>
              <input type="password" class="form-control" v-model="repeatNewPassword">
            </div>
            <button class="btn btn-primary w-100">Save</button>
          </form>
        </transition>
      </div>
      <div class="w-100 text-center">
        <button @click="goToFavourites" class="btn btn-success" style="width: 33%;">Go to Favourites</button>
      </div>
    </div>
  </div>
</template>

<script>
import { inject, ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'UserProfile',
  setup() {
    const router = useRouter();
    const nickname = inject('nickname');
    const currentEmail = ref('example@example.com');
    const newEmail = ref('');
    const currentPassword = ref('');
    const newPassword = ref('');
    const repeatNewPassword = ref('');
    const imageUrl = ref('https://via.placeholder.com/150');
    const showEmailForm = ref(false);
    const showPasswordForm = ref(false);

    const onFileChange = e => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = ev => { imageUrl.value = ev.target.result; };
      reader.readAsDataURL(file);
    };

    const changeEmail = () => {
      if (newEmail.value.trim()) {
        currentEmail.value = newEmail.value.trim();
        newEmail.value = '';
        showEmailForm.value = false;
      }
    };

    const changePassword = () => {
      if (newPassword.value && newPassword.value === repeatNewPassword.value) {
        currentPassword.value = '';
        newPassword.value = '';
        repeatNewPassword.value = '';
        showPasswordForm.value = false;
      }
    };

    const goToFavourites = () => {
      router.push('/favourites');
    };

    return {
      nickname,
      currentEmail,
      newEmail,
      currentPassword,
      newPassword,
      repeatNewPassword,
      imageUrl,
      onFileChange,
      changeEmail,
      changePassword,
      showEmailForm,
      showPasswordForm,
      goToFavourites
    };
  },
};
</script>

<style scoped>
.position-relative {
  position: relative;
}

.file-input {
  opacity: 0;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.edit-overlay {
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 16px;
  font-weight: bold;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.position-relative:hover .edit-overlay {
  opacity: 1;
}
</style>
