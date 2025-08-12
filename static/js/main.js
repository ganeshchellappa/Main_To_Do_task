document.addEventListener("DOMContentLoaded", () => {
  const taskList = document.getElementById("task-list");
  const addTaskBtn = document.getElementById("add-task-btn");
  const newTaskInput = document.getElementById("new-task-input");

  // Add Task
  addTaskBtn.addEventListener("click", async () => {
    const taskText = newTaskInput.value.trim();
    if (!taskText) return alert("Please enter a task.");

    const res = await fetch("/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task: taskText }),
    });
    const data = await res.json();
    if (res.ok) {
      addTaskToDOM(data);
      newTaskInput.value = "";
    } else {
      alert(data.error || "Failed to add task.");
    }
  });

  // Add task item to DOM
  function addTaskToDOM(task) {
    const li = document.createElement("li");
    li.setAttribute("data-id", task.id);
    li.innerHTML = `
      <input type="checkbox" class="complete-checkbox" />
      <span class="task-desc">${task.task}</span>
      <select class="translate-language">
        <option value="">Translate to...</option>
        <option value="english">English</option>
        <option value="hindi">Hindi</option>
        <option value="spanish">Spanish</option>
        <option value="french">French</option>
        <option value="german">German</option>
      </select>
      <button class="translate-btn">Translate</button>
      <button class="delete-btn">Delete</button>
    `;
    taskList.appendChild(li);
  }

  // Delegate clicks for complete, delete, and translate buttons
  taskList.addEventListener("click", async (e) => {
    const li = e.target.closest("li");
    if (!li) return;
    const taskId = li.getAttribute("data-id");

    // Delete task
    if (e.target.classList.contains("delete-btn")) {
      const res = await fetch(`/tasks/${taskId}`, { method: "DELETE" });
      if (res.ok) {
        li.remove();
      } else {
        alert("Failed to delete task.");
      }
    }

    // Complete task
    if (e.target.classList.contains("complete-checkbox")) {
      if (e.target.checked) {
        const res = await fetch(`/tasks/${taskId}/complete`, { method: "POST" });
        if (res.ok) {
          li.classList.add("completed");
        } else {
          alert("Failed to complete task.");
          e.target.checked = false;
        }
      } else {
        // Optionally handle un-complete if API supports
      }
    }

    // Translate task
    if (e.target.classList.contains("translate-btn")) {
      const select = li.querySelector(".translate-language");
      const targetLang = select.value;

      if (!targetLang) {
        alert("Please select a language to translate.");
        return;
      }

      e.target.disabled = true;
      e.target.textContent = "Translating...";

      fetch(`/tasks/${taskId}/translate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target_lang: targetLang }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.translated_text) {
            li.querySelector(".task-desc").textContent = data.translated_text;
          } else if (data.error) {
            alert("Error: " + data.error);
          } else {
            alert("Translation failed");
          }
        })
        .catch(() => alert("Translation failed"))
        .finally(() => {
          e.target.disabled = false;
          e.target.textContent = "Translate";
        });
    }
  });
});
