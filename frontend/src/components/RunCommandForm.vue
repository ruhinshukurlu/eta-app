<template>
  <div class="pb-20">
    <div class="mx-auto mt-10 w-1/2">
      <div class="flex flex-col space-y-6">
        <label for="command" class="block text-xl font-medium leading-6 text-gray-900">Enter commands to create / extend / close ETA</label>
        <div class="flex w-full space-x-2">
          <div class="w-2/3">
            <input id="command" v-model="command" name="command" type="text" class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" @keyup.enter="runCommand">
          </div>
          <div class="w-1/3">
            <button class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" @click="runCommand">Run Command</button>
          </div>
        </div>
        <div class="flex flex-col space-y-4 text-sm">
          <div class="flex items-center space-x-2">
            <span>Start Timer Structure : </span>
            <div class="rounded-md bg-gray-200 p-2">
              {{ startTimerExample }}
            </div>
          </div>

          <div class="flex items-center space-x-2">
            <span>Extend Timer Structure : </span>
            <div class="rounded-md bg-gray-200 p-2">
              {{ extendTimerExample }}
            </div>
          </div>

          <div class="flex items-center space-x-2">
            <span>Close Timer Structure : </span>
            <div class="rounded-md bg-gray-200 p-2">
              {{ closeTimerExample }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import {ref, defineEmits} from "vue";
import useNotifications from "../composables/useNotifications";

const {addNotification} = useNotifications();

// Setting variables
const command = ref("");
const startTimerExample = ref("<project>#<issue-num> at [today | tomorrow | MM-DD] HH:MM");
const extendTimerExample = ref("eta +<num>[m | h | d]");
const closeTimerExample = ref("eta done");

const emits = defineEmits(["refetchEtas"]);
const props = defineProps({openEta: {
  type: Object,
  default: () => {}
}});

// General method to run commands and define which command run
const runCommand = async () => {
  const createRegex = /^(\w+)#(\d+) at(?: (tomorrow|\d{2}-\d{2}))? (\d{2}:\d{2})$/;
  const updateRegex = /^eta \+(\d+)([mhd])$/;
  const doneRegex = /^eta done$/i;

  const createMatches = command.value.match(createRegex);
  const updateMatches = command.value.match(updateRegex);
  const doneMatches = command.value.match(doneRegex);

  if (createMatches) {
    createETA(createMatches);
  } else if (updateMatches) {
    updateETA(updateMatches);
  } else if (doneMatches) {
    closeETA();
  } else {
    addNotification({message: "Invalid command, please check the structure and examples!", type: "error"});
  }
};


const createETA = async (matches) => {
  const token = localStorage.getItem("token");

  const [, project_name, issue, expected_date, expected_time] = matches;
  let expected_at;

  if (expected_date === "tomorrow") {
    expected_at = new Date();
    expected_at.setDate(expected_at.getDate() + 1);
  } else if (expected_date) {
    const [month, day] = expected_date.split("-");
    expected_at = new Date(new Date().getFullYear(), parseInt(month) - 1, parseInt(day));
  } else {
    expected_at = new Date(); // Default to today if no date is provided
  }

  const input_time = new Date(`1970-01-01T${expected_time}`);
  expected_at.setHours(input_time.getHours());
  expected_at.setMinutes(input_time.getMinutes());

  const data = {
    project_name: project_name,
    issue: issue,
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
    command.value = "";
    addNotification({message: "Timer started successfully"});
    emits("refetchEtas"); // refetch updated data
  } else {
    for (const [key, value] of Object.entries(response)) {
      let error = `${key}: ${value}`;
      addNotification({message: error, type: "error"});
    }
  }
};


const updateETA = async (matches) => {
  if (!props.openEta) {
    addNotification({message: "You don't have any open ETA to extend!", type: "error"});
    return;
  }

  const token = localStorage.getItem("token");

  const [, amount, timeType] = matches;

  let expected_date = new Date(props.openEta.expected_at);

  if (timeType === "m") {
    expected_date.setMinutes(expected_date.getMinutes() + parseInt(amount));
  } else if (timeType === "h") {
    expected_date.setHours(expected_date.getHours() + parseInt(amount));
  } else {
    expected_date.setDate(expected_date.getDate() + parseInt(amount));
  }

  const data = {
    expected_at: expected_date,
    done_at: null
  };

  const apiResponse = await fetch(`/api/update-expectation/${props.openEta.id}/`, {
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
    emits("refetchEtas"); // refetch updated data
  } else {
    addNotification({message: "Something went wrong!", type: "error"});
  }
};

const closeETA = async () => {
  if (!props.openEta) {
    addNotification({message: "You don't have any open ETA to close!", type: "error"});
    return;
  }
  const token = localStorage.getItem("token");
  const data = {
    expected_at: props.openEta.expected_at,
    done_at: new Date()
  };

  const apiResponse = await fetch(`/api/update-expectation/${props.openEta.id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Token ${token}`
    },
    body: JSON.stringify(data),
  });

  const status = apiResponse.status;

  if (status === 200) {
    addNotification({message: "ETA closed successfully!"});
    emits("refetchEtas"); // refetch updated data
  } else {
    addNotification({message: "Something went wrong!", type: "error"});
  }
};

</script>
