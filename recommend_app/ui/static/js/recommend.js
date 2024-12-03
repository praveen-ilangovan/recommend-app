// Register JS
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
        alert(`Error: ${errorData.message}`);
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
        alert(`Error: ${errorData.detail}`);
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
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  });
}

function editBoardData(element) {
  const row = element.closest("tr");

  // Hide the span and display the input field
  // Initialize the field with the current value
  const editNameField = row.cells[0].getElementsByTagName("input")[0];
  const currentNameField = row.cells[0].getElementsByTagName("span")[0];
  editNameField.style.display = "block";
  currentNameField.style.display = "none";
  editNameField.value = currentNameField.innerHTML;

  // Hide the span and display the checkbox
  // Initialize the checkbox with the current value
  const editPrivateField = row.cells[1].getElementsByTagName("input")[0];
  const currentPrivateField = row.cells[1].getElementsByTagName("span")[0];
  editPrivateField.style.display = "block";
  currentPrivateField.style.display = "none";
  editPrivateField.checked = currentPrivateField.innerHTML == "True";

  // Hide the edit button and Display the updateButton
  const updateButton = row.cells[2].getElementsByTagName("button")[1];
  element.style.display = "none";
  updateButton.style.display = "block";
}

async function updateBoardData(element, board_id) {
  const row = element.closest("tr");
  const editNameField = row.cells[0].getElementsByTagName("input")[0];
  const editPrivateField = row.cells[1].getElementsByTagName("input")[0];

  const payload = {
    name: editNameField.value,
    private: editPrivateField.checked,
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
