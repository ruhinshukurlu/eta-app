<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div>
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <div class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Username</label>
          <div class="mt-2">
            <input id="username" v-model="username" required name="username" type="text" class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
          <div class="mt-2">
            <input id="password" v-model="password" required name="password" type="password" autocomplete="current-password" class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>

        <div>
          <button class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" @click="loginUser">
            Sign in
          </button>
        </div>
      </div>

      <p class="mt-10 text-center text-sm text-gray-500">
        You don't have an account?
        <router-link to="/register" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">
          Register now
        </router-link>
      </p>
    </div>
  </div>
</template>
<script setup>
import {ref} from "vue";
import useNotifications from "../composables/useNotifications";
import router from "../router/index";

const {addNotification} = useNotifications();

const username = ref("");
const password = ref("");

const loginUser = async () => {
  const data = {
    username: username.value,
    password: password.value,
  };

  const api_response = await fetch("/api/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const status = api_response.status;
  const response = await api_response.json();
  if (status === 200) {
    localStorage.setItem("token", response.token);
    localStorage.setItem("username", response.username);
    router.push("/");
  } else {
    addNotification({message: response.error, type: "error"});
  }
};
</script>
