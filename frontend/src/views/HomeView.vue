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
                  <td class="flex items-center space-x-2 px-3 py-4 text-sm text-gray-500">
                    <span>{{ convertDate(expectation.expected_at) }}</span>
                    <div v-if="!expectation.done_at" class="flex space-x-2">
                      <input id="amount" v-model="updated_amount" min="1" max="100" name="amount" type="number" class="block w-fit rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                      <select id="update_type" v-model="update_type" name="update_type" class="block w-fit rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6">
                        <option value="minute">Minute</option>
                        <option value="hour">Hour</option>
                        <option value="day">Day</option>
                      </select>
                      <button class="rounded-md border border-gray-300 p-2 text-black hover:bg-gray-300" @click="updateETA(expectation, 'extend')">
                        Extend ETA
                      </button>
                    </div>
                  </td>
                  <td class="px-3 py-4 text-sm text-gray-500">
                    <span>{{ convertDate(expectation.done_at) }}</span>
                    <button v-if="!expectation.done_at" class="rounded-md border border-green-700 bg-green-400 p-2 text-white hover:bg-green-500" @click="updateETA(expectation, 'done')">
                      Close ETA
                    </button>
                  </td>
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

    <CreateEtaForm @refetch-etas="fetchETAs" />
  </div>
</template>
<script setup>
import {ref, onMounted} from "vue";
import {convertDate} from "../utils/index";
import CreateEtaForm from "../components/CreateEtaForm.vue";
import useNotifications from "../composables/useNotifications";
import ExpectationsLoading from "../components/ExpectationsLoading.vue";

const {addNotification} = useNotifications();

// to get loading statement
const isLoading = ref(true);

// getting user past ETAs
const expectations = ref([]);

const fetchETAs = async () => {
  const token = localStorage.getItem("token");
  const api_response = await fetch("/api/user-expectations", {
    headers: {
      "Authorization": `Token ${token}`
    },
  });
  expectations.value = await api_response.json();
  isLoading.value = false;
};

onMounted(async () => {
  fetchETAs();
});

// update ETa | extend timer
const updated_amount = ref(1);
const update_type = ref("minute");

const updateETA = async (expectation, command) => {
  const token = localStorage.getItem("token");

  let data = {};

  if ( command === "done" ) {
    data = {
      expected_at: expectation.expected_at,
      done_at: new Date()
    };
  } else {
    let expected_date = new Date(expectation.expected_at);

    if (update_type.value === "minute") {
      expected_date.setMinutes(expected_date.getMinutes() + updated_amount.value);
    } else if (update_type.value === "hour") {
      expected_date.setHours(expected_date.getHours() + updated_amount.value);
    } else {
      expected_date.setDate(expected_date.getDate() + updated_amount.value);
    }

    data = {
      expected_at: expected_date,
      done_at: null
    };
  }

  const apiResponse = await fetch(`/api/update-expectation/${expectation.id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Token ${token}`
    },
    body: JSON.stringify(data),
  });

  const status = apiResponse.status;

  if (status === 200) {
    addNotification({message: "ETA timer updated successfully!"});
    fetchETAs(); // refetch updated data
  } else {
    addNotification({message: "Something went wrong!", type: "error"});
  }
};
</script>
