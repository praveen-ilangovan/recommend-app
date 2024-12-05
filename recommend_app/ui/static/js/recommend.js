/*
Register a new user
*/
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    if (data.password !== data.repeatPassword) {
      alert("Passwords do not match");
      return;
    }

    const payload = {
      email_address: data.emailAddress,
      first_name: data.firstName,
      last_name: data.lastName,
      user_name: data.userName,
      password: data.password,
    };

    try {
      const response = await fetch("/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        window.location.href = "/session/new";
      } else {
        // Handle error
        const errorData = await response.json();
        alert(`Error: ${errorData.detail.error}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

// Login JS
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const payload = new URLSearchParams();
    for (const [key, value] of formData.entries()) {
      payload.append(key, value);
    }

    try {
      const response = await fetch("/session/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: payload.toString(),
      });

      if (response.ok) {
        // Handle success (e.g., redirect to dashboard)
        const data = await response.json();
        window.location.href = "/me/";
      } else {
        // Handle error
        const errorData = await response.json();
        alert(`Error: ${errorData.detail.error}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

// Logout
async function logout() {
  try {
    const response = await fetch("/session/", {
      method: "DELETE",
    });

    if (response.ok) {
      window.location.href = "/session/new";
    } else {
      // Handle error
      const errorData = await response.json();
      alert(`Error: ${errorData.message}`);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
}

/*
  Users
*/

function editUserData(element) {
  // Hide the edit button and Display the update and cancel button
  const saveButton = document.getElementById("saveUserDataButton");
  const cancelButton = document.getElementById("cancelUserDataButton");
  element.style.display = "none";
  saveButton.style.display = "inline";
  cancelButton.style.display = "inline";

  // Hide the span and display the input field
  // Initialize the field with the current value
  const firstNameInputField = document.getElementById("firstNameInputField");
  const firstNameSpanField = document.getElementById("firstNameSpanField");
  firstNameInputField.style.display = "block";
  firstNameSpanField.style.display = "none";
  firstNameInputField.value = firstNameSpanField.innerHTML;

  // Hide the span and display the checkbox
  // Initialize the checkbox with the current value
  const lastNameInputField = document.getElementById("lastNameInputField");
  const lastNameSpanField = document.getElementById("lastNameSpanField");
  lastNameInputField.style.display = "block";
  lastNameSpanField.style.display = "none";
  lastNameInputField.value = lastNameSpanField.innerHTML;
}

async function updateUserData(user_id) {
  const payload = {
    first_name: document.getElementById("firstNameInputField").value,
    last_name: document.getElementById("lastNameInputField").value,
  };

  const url = "/users/" + user_id;

  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      window.location.href = "";
    } else {
      // Handle error
      const errorData = await response.json();
      alert(`Error: ${errorData.detail.error}`);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
}

/*
  Password
*/

function editPassword(element) {
  const newPasswordRow = document.getElementById("newPasswordRow");
  const repeatPasswordRow = document.getElementById("repeatPasswordRow");
  newPasswordRow.style.display = "inline";
  repeatPasswordRow.style.display = "inline";

  // Toggle the visibility of the buttons
  const saveButton = document.getElementById("savePasswordButton");
  const cancelButton = document.getElementById("cancelPasswordButton");
  element.style.display = "none";
  saveButton.style.display = "inline";
  cancelButton.style.display = "inline";
}

async function savePassword(element, user_id) {
  const div = element.closest("div");
  const table = div.parentElement.getElementsByTagName("table")[0];

  const newPassword = document.getElementById("newPasswordInputField").value;
  const repeatPassword = document.getElementById(
    "repeatPasswordInputField",
  ).value;

  if (newPassword !== repeatPassword) {
    alert("Passwords do not match");
    return;
  }

  const payload = {
    password: newPassword,
  };

  const url = "/users/" + user_id;

  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      window.location.href = "";
    } else {
      // Handle error
      const errorData = await response.json();
      alert(`Error: ${errorData.detail.error}`);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
}

/*
  Boards
*/

// Create Board JS
const createBoardForm = document.getElementById("createBoardForm");
if (createBoardForm) {
  createBoardForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    let private = false;
    if (data.private) {
      private = true;
    }

    const payload = {
      name: data.name,
      private: private,
    };

    try {
      const response = await fetch("/boards/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        window.location.href = "/me/";
      } else {
        // Handle error
        const errorData = await response.json();
        alert(`Error: ${errorData.detail.error}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

function editBoardData(element) {
  // Hide the edit button and Display the update and cancel button
  const updateButton = document.getElementById("saveBoardDataButton");
  const cancelButton = document.getElementBysId("cancelBoardDataButton");
  element.style.display = "none";
  updateButton.style.display = "inline";
  cancelButton.style.display = "inline";

  // Hide the span and display the input field
  // Initialize the field with the current value
  const boardNameInputField = document.getElementById("boardNameInputField");
  const boardNameSpanField = document.getElementById("boardNameSpanField");
  boardNameInputField.style.display = "block";
  boardNameSpanField.style.display = "none";
  boardNameInputField.value = boardNameSpanField.innerHTML;

  // Hide the span and display the checkbox
  // Initialize the checkbox with the current value
  const boardPrivateInputField = document.getElementById(
    "boardPrivateInputField",
  );
  const boardPrivateSpanField = document.getElementById(
    "boardPrivateSpanField",
  );
  boardPrivateInputField.style.display = "block";
  boardPrivateSpanField.style.display = "none";
  boardPrivateInputField.checked = boardPrivateSpanField.innerHTML == "True";
}

async function updateBoardData(board_id) {
  const payload = {
    name: document.getElementById("boardNameInputField").value,
    private: document.getElementById("boardPrivateInputField").checked,
  };

  const url = "/boards/" + board_id;

  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      window.location.href = "";
    } else {
      // Handle error
      const errorData = await response.json();
      alert(`Error: ${errorData.detail.error}`);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
}

async function deleteBoard(board_id) {
  const url = "/boards/" + board_id;

  try {
    const response = await fetch(url, {
      method: "DELETE",
    });

    if (response.ok) {
      window.location.href = "/me/";
    } else {
      // Handle error
      const errorData = await response.json();
      alert(`Error: ${errorData.message}`);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
}

/*
Cards
*/

// Create a card
const createCardForm = document.getElementById("createCardForm");
if (createCardForm) {
  createCardForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const board_id = data.board_id;
    const payload = {
      url: data.url,
      title: data.title,
      description: data.description,
      thumbnail: data.thumbnail,
    };

    const url = "/boards/" + board_id + "/cards";
    const redirect = "/boards/" + board_id;

    console.log(payload);

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        window.location.href = redirect;
      } else {
        // Handle error
        const errorData = await response.json();
        console.log(errorData);
        alert(`Error: ${errorData.detail.error}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

function editCardData(element) {
  // Hide the edit button and Display the update and cancel button
  const saveButton = document.getElementById("saveCardDataButton");
  const cancelButton = document.getElementById("cancelCardDataButton");
  element.style.display = "none";
  saveButton.style.display = "inline";
  cancelButton.style.display = "inline";

  // Hide the span and display the input field
  // Initialize the field with the current value
  const cardTitleInputField = document.getElementById("cardTitleInputField");
  const cardTitleSpanField = document.getElementById("cardTitleSpanField");
  cardTitleInputField.style.display = "block";
  cardTitleSpanField.style.display = "none";
  cardTitleInputField.value = cardTitleSpanField.innerHTML;

  // Hide the span and display the input field
  // Initialize the field with the current value
  const cardDescriptionInputField = document.getElementById(
    "cardDescriptionInputField",
  );
  const cardDescriptionSpanField = document.getElementById(
    "cardDescriptionSpanField",
  );
  cardDescriptionInputField.style.display = "block";
  cardDescriptionSpanField.style.display = "none";
  cardDescriptionInputField.value = cardDescriptionSpanField.innerHTML;

  // Hide the span and display the input field
  // Initialize the field with the current value
  const cardThumbnailInputField = document.getElementById(
    "cardThumbnailInputField",
  );
  const cardThumbnailSpanField = document.getElementById(
    "cardThumbnailSpanField",
  );
  cardThumbnailInputField.style.display = "block";
  cardThumbnailSpanField.style.display = "none";
  cardThumbnailInputField.value = cardThumbnailSpanField.innerHTML;
}

async function updateCardData(card_id) {
  const payload = {
    title: document.getElementById("cardTitleInputField").value,
    description: document.getElementById("cardDescriptionInputField").value,
    thumbnail: document.getElementById("cardThumbnailInputField").value,
  };

  const url = "/cards/" + card_id;

  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      window.location.href = "";
    } else {
      // Handle error
      const errorData = await response.json();
      alert(`Error: ${errorData.detail.error}`);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
}

async function deleteCard(card_id) {
  const url = "/cards/" + card_id;

  try {
    const response = await fetch(url, {
      method: "DELETE",
    });

    if (response.ok) {
      window.location.href = "/me/";
    } else {
      // Handle error
      const errorData = await response.json();
      alert(`Error: ${errorData.message}`);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
}
