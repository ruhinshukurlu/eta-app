<template>
  <div>
    <div class="mx-auto w-4/5 pt-20">
      <h1 class="mb-8 w-full text-center text-3xl font-bold">Past ETAs</h1>
      <ExpectationsLoading v-if="isLoading" />
      <div v-else class="mt-8 flow-root">
        <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <table v-if="expectations.length !== 0" class="min-w-full divide-y divide-gray-300">
              <thead>
                <tr>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Project</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Issue</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Started At</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Expected At</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Completed At</th>
                </tr>
              </thead>
              <tbody class="bg-white">
                <tr v-for="expectation in expectations" :key="expectation.id" class="even:bg-gray-50">
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ expectation.project.name }}</td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ expectation.issue }}</td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ convertDate(expectation.created_at) }}</td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ convertDate(expectation.expected_at) }}</td>
                  <td class="px-3 py-4 text-sm text-gray-500">{{ convertDate(expectation.done_at) }}</td>
                </tr>
              </tbody>
            </table>

            <div v-else>
              <p class="text-center text-xl font-bold">You haven't created any ETA yet!</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <RunCommandForm :open-eta="openExpectation" @refetch-etas="fetchETAs" />
  </div>
</template>
<script setup>
import {ref, onMounted} from "vue";
import {convertDate} from "../utils/index";
import RunCommandForm from "../components/RunCommandForm.vue";
import ExpectationsLoading from "../components/ExpectationsLoading.vue";

// to get loading statement
const isLoading = ref(true);

// getting user past ETAs
const expectations = ref([]);
const openExpectation = ref(null);

const fetchETAs = async () => {
  const token = localStorage.getItem("token");
  openExpectation.value = null;
  const api_response = await fetch("/api/user-expectations", {
    headers: {
      "Authorization": `Token ${token}`
    },
  });
  expectations.value = await api_response.json();
  expectations.value.forEach((eta) => {
    if (!eta.done_at) {
      openExpectation.value = eta;
    }
  });
  isLoading.value = false;
};

onMounted(async () => {
  fetchETAs();
});

</script>
