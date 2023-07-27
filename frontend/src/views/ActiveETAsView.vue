<template>
  <div class="mx-auto w-4/5 py-20">
    <h1 class="mb-8 w-full border-b border-gray-300 pb-4 text-center text-3xl font-bold">All Active ETAs</h1>
    <ExpectationsLoading v-if="isLoading" />
    <div v-else class="mt-8 flow-root">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <table v-if="expectations.length !== 0" class="min-w-full divide-y divide-gray-300">
            <thead>
              <tr>
                <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-3">User</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Project</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Issue</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Started At</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Expected At</th>
              </tr>
            </thead>
            <tbody class="bg-white">
              <tr v-for="expectation in expectations" :key="expectation.id" class="even:bg-gray-50">
                <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-3">{{ expectation.user.username }}</td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ expectation.project.name }}</td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ expectation.issue }}</td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ convertDate(expectation.created_at) }}</td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ convertDate(expectation.expected_at) }}</td>
              </tr>
            </tbody>
          </table>
          <div v-else>
            <p class="text-center text-xl font-bold">No Active ETAs found in the system!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import {ref, onMounted} from "vue";
import {convertDate} from "../utils/index";
import ExpectationsLoading from "../components/ExpectationsLoading.vue";

const expectations = ref([]);
const isLoading = ref(true);

onMounted(async () => {
  const api_response = await fetch("/api/active-expectations");
  expectations.value = await api_response.json();
  isLoading.value = false;
});
</script>
