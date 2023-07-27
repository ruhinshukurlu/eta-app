
export function convertDate(dateString) {
  if (!dateString) {
    // if datestring is null
    return "";
  }
  const date = new Date(dateString);
  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, "0");
  const day = String(date.getUTCDate()).padStart(2, "0");
  const hours = String(date.getUTCHours()).padStart(2, "0");
  const minutes = String(date.getUTCMinutes()).padStart(2, "0");

  return `${year}-${month}-${day} ${hours}:${minutes}`;
}


export function checkWhichDay(dateString) {
  const date = new Date(dateString);
  const today = new Date();
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  let result = "";

  if (today.toDateString() === date.toDateString()) {
    result = "";
  } else if (tomorrow.toDateString() === date.toDateString()) {
    result = "tomorrow";
  } else {
    result = dateString;
  }

  return result;
}
