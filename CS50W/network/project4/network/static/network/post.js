document.addEventListener("DOMContentLoaded", function () {
  // Set id of what's happening area
  if (document.querySelectorAll(".both_postform")[0]) {
    document
      .querySelectorAll(".both_postform")[0]
      .setAttribute("id", "popup_postform");
  }

  if (document.querySelectorAll(".both_postform")[1]) {
    document
      .querySelectorAll(".both_postform")[1]
      .setAttribute("id", "upper_postform");
  }

  // Prevent default submission of edit and like forms
  let forms = document.querySelectorAll(".edit_like");
  len_forms = forms.length;
  for (i = 0; i < len_forms; i++) {
    forms[i].addEventListener("submit", function (event) {
      event.preventDefault();
      console.log("change");
    });
  }

  // Set page numbers
  const totalPages = document.querySelector("#page_numbers").value;
  for (i = 1, len = totalPages; i <= len; i++) {
    const item = document.createElement("li");
    item.setAttribute("class", "content");
    item.innerHTML = `<a class="page-link content" href="?page=${[i]}">${[
      i,
    ]}</a>`;
    $("#page").append(item);
  }

  // Prevent default upper post submit
  document.querySelector("#home").addEventListener("click", () => {
    document
      .querySelector("#upper_post_form")
      .addEventListener("submit", function (event) {
        event.stopPropagation();
        // event.preventDefault();
      });
  });

  // Prevent default popup post submit
  document
    .querySelector("#popup_post_form")
    .addEventListener("submit", function (event) {
      event.stopPropagation();
    });

  // By default, load post composing form
  compose_post();
});

function compose_post() {
  
  // Clear post textareas
  if (document.querySelector(".both_postform")) {
    document.querySelector(".both_postform").value = "";
  }

  document.querySelector("#new_post").addEventListener("click", () => {
    document.querySelector(".both_postform").value = "";
  });

  // Submit the post
  submit_post();
}

function submit_post() {
  // Select upper post submit
  const upper_submit = document.querySelector("#upper_new_post");
  const upper_textarea = document.querySelectorAll(".both_postform")[1];
  if (upper_submit) {
    upper_submit.disabled = true;
  }

  // Upper submit false if no input
  if (document.querySelectorAll(".both_postform")[1]) {
    upper_textarea.onkeyup = () => {
      if (upper_textarea.value.length > 0) {
        upper_submit.disabled = false;
      } else {
        upper_submit.disabled = true;
      }
    };
  }

  // Select popup post submit
  const popup_submit = document.querySelector("#popup_new_post");
  const popup_textarea = document.querySelector(".both_postform");
  // console.log(popup_textarea);

  // Submit default disabled
  popup_submit.disabled = true;

  document.querySelector("#new_post").addEventListener("click", () => {
    // Popup submit false if no input
    popup_textarea.onkeyup = () => {
      if (popup_textarea.value.length > 0) {
        popup_submit.disabled = false;
      } else {
        popup_submit.disabled = true;
      }
    };
  });
}

// Csrf token by JS function
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

// Like post
function like(post_id, user_id) {
  const request = new Request(`/likes/${post_id}/${user_id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
    method: "POST",
    mode: "same-origin",
    body: JSON.stringify({
      post: post_id,
      user: user_id,
    }),
  })
    .then((response) => response.json())
    .then((likes) => {
      console.log(likes);
      like_count = 0;
      for (i = 0, len = likes.length; i < len; i++) {
        like_count++;
      }
      console.log(like_count);
      const count = document.querySelector(`#count${post_id}`);
      count.innerHTML = like_count;
    });
}

// Edit post
function edit(post_id) {
  document.querySelector(`#post_paragraph${post_id}`).style.display = "none";
  document.querySelector(`#post_button${post_id}`).style.display = "none";
  document.querySelector(`#edit_textarea${post_id}`).style.display = "block";
  document.querySelector(`#edit_button${post_id}`).style.display = "block";

  // Get edited post
  const post_after_edit = document.querySelector(`#edit_text${post_id}`);
  // console.log(post_after_edit.value);

  // Fetch post
  document
    .querySelector(`#edit_form${post_id}`)
    .addEventListener("submit", function (event) {
      console.log("edit submitted");

      const request = new Request(`/edit/${post_id}`, {
        headers: { "X-CSRFToken": csrftoken },
      });
      fetch(request, {
        method: "PUT",
        mode: "same-origin",
        body: JSON.stringify({
          content: post_after_edit.value,
        }),
      })
        .then(() => {
          document.querySelector(
            `#post_paragraph${post_id}`
          ).innerText = `${post_after_edit.value}`;
          document.querySelector(`#edit_button${post_id}`).style.display =
            "none";
          document.querySelector(`#edit_textarea${post_id}`).style.display =
            "none";
          document.querySelector(`#post_paragraph${post_id}`).style.display =
            "block";
          document.querySelector(`#post_button${post_id}`).style.display =
            "block";
        });
    });
}
