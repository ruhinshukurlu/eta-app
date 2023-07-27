<template>
  <div class="pb-20">
    <div>
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Create new ETA</h2>
    </div>

    <div class="mx-auto mt-10 w-1/2">
      <div class="space-y-6">
        <div class="grid w-full grid-cols-4 space-x-2">
          <div>
            <label for="project" class="block text-sm font-medium leading-6 text-gray-900">Project Name</label>
            <div class="mt-2">
              <input id="project" v-model="project_name" name="project" type="text" class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
          </div>

          <div>
            <label for="issue" class="block text-sm font-medium leading-6 text-gray-900">Issue</label>
            <div class="mt-2">
              <input id="issue" v-model="issue" name="issue" type="text" class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
          </div>

          <div>
            <label for="date" class="block text-sm font-medium leading-6 text-gray-900">Date</label>
            <div class="mt-2">
              <input id="date" v-model="expected_date" name="date" type="date" class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
          </div>

          <div>
            <label for="time" class="block text-sm font-medium leading-6 text-gray-900">Time</label>
            <div class="mt-2">
              <input id="time" v-model="expected_time" name="time" type="time" class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
          </div>
        </div>

        <div v-if="project_name" class="w-full rounded-md bg-zinc-100 p-2 text-sm font-bold">
          {{ project_name }}#{{ issue }} at {{ checkWhichDay(expected_date) }} {{ expected_time }}
        </div>
        <div>
          <button class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" @click="createETA">Create ETA</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import {ref, defineEmits} from "vue";
import {checkWhichDay} from "../utils/index";
import useNotifications from "../composables/useNotifications";

const {addNotification} = useNotifications();

// Setting variables
const project_name = ref("");
const issue = ref("");
const expected_date = ref("");
const expected_time = ref("");
const emits = defineEmits(["refetchEtas"]);

const createETA = async () => {
  const token = localStorage.getItem("token");
  // combining expected date and time
  const expected_at = new Date(expected_date.value);
  const input_time = new Date(`1970-01-01T${expected_time.value}`);
  expected_at.setHours(input_time.getHours());
  expected_at.setMinutes(input_time.getMinutes());

  const data = {
    project_name: project_name.value,
    issue: issue.value,
    expected_at: expected_at,
  };

  const api_response = await fetch("/api/create-expectation/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Token ${token}`
    },
    body: JSON.stringify(data),
  });
  const response = await api_response.json();
  const status = api_response.status;
  if (status === 201) {
    addNotification({message: "Timer started successfully"});
    emits("refetchEtas"); // refetch updated data
  } else {
    for (const [key, value] of Object.entries(response)) {
      let error = `${key}: ${value}`;
      addNotification({message: error, type: "error"});
    }
  }
};
</script>
