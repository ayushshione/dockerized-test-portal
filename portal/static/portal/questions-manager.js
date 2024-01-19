function getCSRFToken() {
  var csrfToken = null;

  var cookies = document.cookie.split(";");
  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i].trim();
    if (cookie.startsWith("csrftoken=")) {
      csrfToken = cookie.substring("csrftoken=".length, cookie.length);
      break;
    }
  }

  return csrfToken;
}

const checkboxes = document.getElementsByName("question_check");
const selected_box = document.getElementById("selected-box");
const initial_text = selected_box.innerText;
const delete_button = document.getElementById("delete-btn");
let selected = 0;

delete_button.addEventListener("click", () => {
  const toDelete = [];
  checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      toDelete.push(checkbox.id);
    }
  });

  fetch(`/delete-questions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({
      test_id: test_id,
      to_delete: toDelete,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      location.reload()
    })
    .catch((error) => {
      // Handle errors
      console.error("There was a problem with the fetch operation:", error);
    });
});

checkboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    if (checkbox.checked == true) {
      if (delete_button.classList.contains("hidden")) {
        delete_button.classList.add("flex");
        delete_button.classList.remove("hidden");
      }
      selected++;
    } else {
      selected--;
    }

    if (selected <= 0) {
      selected_box.innerText = initial_text;
      if (delete_button.classList.contains("flex")) {
        delete_button.classList.add("hidden");
        delete_button.classList.remove("flex");
      }
    } else {
      selected_box.innerText = `${selected} SELECTED`;
    }
  });
});
