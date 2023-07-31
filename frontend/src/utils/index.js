
export function convertDate(dateString) {
  if (!dateString) {
    // if datestring is null
    return "";
  }
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");

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
